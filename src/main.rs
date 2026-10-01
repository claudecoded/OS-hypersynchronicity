use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::env;
use std::sync::Arc;
use tokio::io::{AsyncReadExt, AsyncWriteExt};
use tokio::net::{TcpListener, TcpStream};
use tokio::sync::Mutex;

#[derive(Serialize, Deserialize, Debug)]
enum MemoryCommand {
    Write { address: usize, data: Vec<u8> },
    Read { address: usize },
}

#[derive(Serialize, Deserialize, Debug)]
enum MemoryResponse {
    Ack,
    Data(Vec<u8>),
    Error(String),
}

// Simulated remote memory storage for Worker Node
struct WorkerNode {
    storage: HashMap<usize, Vec<u8>>,
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 {
        println!("Usage:");
        println!("  As Master: hypersync-dsm master <worker_ip:port>");
        println!("  As Worker: hypersync-dsm worker <port>");
        return Ok();
    }

    let mode = &args[1];

    if mode == "worker" {
        let port = args.get(2).expect("Please provide a port for the worker");
        run_worker(port).await?;
    } else if mode == "master" {
        let worker_addr = args.get(2).expect("Please provide worker address");
        run_master(worker_addr).await?;
    }

    Ok(())
}

async fn run_worker(port: &str) -> Result<(), Box<dyn std::error::Error>> {
    let addr = format!("0.0.0.0:{}", port);
    let listener = TcpListener::bind(&addr).await?;
    println!("[WORKER] Shared Memory Worker listening on {}", addr);

    let storage = Arc::new(Mutex::new(HashMap::<usize, Vec<u8>>::new()));

    loop {
        let (mut socket, _) = listener.accept().await?;
        let storage_clone = Arc::clone(&storage);

        tokio::spawn(async move {
            let mut buffer = [0; 1024];
            while let Ok(n) = socket.read(&mut buffer).await {
                if n == 0 { break; }

                let cmd: MemoryCommand = match serde_json::from_slice(&buffer[..n]) {
                    Ok(c) => c,
                    Err(_) => continue,
                };

                let response = match cmd {
                    MemoryCommand::Write { address, data } => {
                        let mut mem = storage_clone.lock().await;
                        println!("[WORKER] Writing {} bytes to virtual address Ox{:X}", data.len(), address);
                        mem.insert(address, data);
                        MemoryResponse::Ack
                    }
                    MemoryCommand::Read { address } => {
                        let mem = storage_clone.lock().await;
                        if let Some(data) = mem.get(&address) {
                            println!("[WORKER] Reading virtual address Ox{:X}", address);
                            MemoryResponse::Data(data.clone())
                        } else {
                            MemoryResponse::Error("Address fault".to_string())
                        }
                    }
                };

                let resp_bytes = serde_json::to_vec(&response).unwrap();
                let _ = socket.write_all(&resp_bytes).await;
            }
        });
    }
}

async fn run_master(worker_addr: &str) -> Result<(), Box<dyn std::error::Error>> {
    println!("[MASTER] Connecting to remote memory provider at {}...", worker_addr);
    let mut stream = TcpStream::connect(worker_addr).await?;
    println!("[MASTER] Virtual Memory Pool Connected successfully.");

    // Demo Scenario: Writing large data to simulated virtual remote memory address
    let virtual_address = 0x7FFF0001;
    let payload = b"HyperSynchronicity Shared Kernel Memory Payload".to_vec();

    println!("[MASTER] Offloading data to virtual memory address Ox{:X}", virtual_address);
    let write_cmd = MemoryCommand::Write { address: virtual_address, data: payload };
    let cmd_bytes = serde_json::to_vec(&write_cmd)?;
    stream.write_all(&cmd_bytes).await?;

    let mut buffer = [0; 1024];
    let n = stream.read(&mut buffer).await?;
    let resp: MemoryResponse = serde_json::from_slice(&buffer[..n])?;
    println!("[MASTER] Worker response: {:?}", resp);

    // Demo Scenario: Reading it back
    println!("[MASTER] Fetching data from virtual memory address Ox{:X}", virtual_address);
    let read_cmd = MemoryCommand::Read { address: virtual_address };
    let cmd_bytes = serde_json::to_vec(&read_cmd)?;
    stream.write_all(&cmd_bytes).await?;

    let n = stream.read(&mut buffer).await?;
    let resp: MemoryResponse = serde_json::from_slice(&buffer[..n])?;
    
    if let MemoryResponse::Data(data) = resp {
        println!("[MASTER] Successfully read data: '{}'", String::from_utf8_lossy(&data));
    }

    Ok(())
}
