use std::env;
use std::collections::HashMap;
use std::sync::Arc;
use tokio::io::{AsyncReadExt, AsyncWriteExt};
use tokio::net::{TcpListener, TcpStream};
use tokio::sync::Mutex;

mod memory_pool;
mod ffi;

#[derive(serde::Serialize, serde::Deserialize, Debug)]
enum MemoryCommand {
    Write { address: usize, data: Vec<u8> },
    Read { address: usize },
}

#[derive(serde::Serialize, serde::Deserialize, Debug)]
enum MemoryResponse {
    Ack,
    Data(Vec<u8>),
    Error(String),
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 {
        println!("HyperSync Engine Status: Active");
        println!("Usage for Cluster Networking:");
        println!("  hypersync_core worker <port>");
        println!("  hypersync_core master <worker_ip:port>");
        return Ok();
    }

    let mode = &args[1];

    if mode == "worker" {
        let port = args.get(2).expect("Provide worker daemon socket port");
        run_worker_daemon(port).await?;
    } else if mode == "master" {
        let worker_addr = args.get(2).expect("Provide target master remote gateway IP:PORT");
        println!("[HYPERSYNC] Running in local master interceptor mode connected to {}", worker_addr);
    }

    Ok(())
}

async fn run_worker_daemon(port: &str) -> Result<(), Box<dyn std::error::Error>> {
    let addr = format!("0.0.0.0:{}", port);
    let listener = TcpListener::bind(&addr).await?;
    println!("[HYPERSYNC DEAMON] Shared Kernel Memory Worker bound to {}", addr);

    let storage = Arc::new(Mutex::new(HashMap::<usize, Vec<u8>>::new()));

    loop {
        let (mut socket, _) = listener.accept().await?;
        let storage_clone = Arc::clone(&storage);

        tokio::spawn(async move {
            let mut buffer = [0; 4096];
            while let Ok(n) = socket.read(&mut buffer).await {
                if n == 0 { break; }

                let cmd: MemoryCommand = match serde_json::from_slice(&buffer[..n]) {
                    Ok(c) => c,
                    Err(_) => continue,
                };

                let response = match cmd {
                    MemoryCommand::Write { address, data } => {
                        let mut mem = storage_clone.lock().await;
                        mem.insert(address, data);
                        MemoryResponse::Ack
                    }
                    MemoryCommand::Read { address } => {
                        let mem = storage_clone.lock().await;
                        if let Some(data) = mem.get(&address) {
                            MemoryResponse::Data(data.clone())
                        } else {
                            MemoryResponse::Error("Distributed Page Fault".to_string())
                        }
                    }
                };

                let resp_bytes = serde_json::to_vec(&response).unwrap();
                let _ = socket.write_all(&resp_bytes).await;
            }
        });
    }
}
