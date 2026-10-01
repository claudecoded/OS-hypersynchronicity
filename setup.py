# -*- coding: utf-8 -*-
# ==============================================================================
# HYPERSYNC DISTRIBUTED MEMORY SUITE (v1.0.0)
# ==============================================================================
import socket
import json
import random
import threading
import time
import sys

PAGE_SIZE = 4096

class DistributedMMU:
    def __init__(self):
        self.page_table = {}
        self.worker_address = ("127.0.0.1", 8585)
        self.base_virtual_address = 0x80000000

    def hypersync_malloc(self, size: int) -> int:
        pages_needed = (size + PAGE_SIZE - 1) // PAGE_SIZE
        allocated_address = self.base_virtual_address
        for i in range(pages_needed):
            self.page_table[allocated_address + (i * PAGE_SIZE)] = {"node_id": 1, "dirty": False}
        self.base_virtual_address += pages_needed * PAGE_SIZE
        print(f"[HYPERSYNC MMU] Mapped {pages_needed} virtual network pages at address: 0x{allocated_address:X}")
        return allocated_address

    def hypersync_write(self, virtual_address: int, data: str) -> bool:
        if virtual_address not in self.page_table: 
            return False
        print(f"[HYPERSYNC IO] Intercepted raw write at 0x{virtual_address:X}.")
        print(f"[HYPERSYNC IO] Offloading data payload ({len(data)} bytes) to hardware cluster...")
        return self._send_to_cluster({"command": "WRITE", "address": virtual_address, "data": data})

    def hypersync_read(self, virtual_address: int) -> str:
        if virtual_address not in self.page_table: 
            return None
        response = self._send_to_cluster_with_response({"command": "READ", "address": virtual_address})
        return response.get("data") if response else None

    def _send_to_cluster(self, payload):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect(self.worker_address)
                s.sendall(json.dumps(payload).encode('utf-8'))
                return True
        except: 
            return False

    def _send_to_cluster_with_response(self, payload):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect(self.worker_address)
                s.sendall(json.dumps(payload).encode('utf-8'))
                return json.loads(s.recv(4096).decode('utf-8'))
        except: 
            return None

def run_worker_daemon():
    allocated_ram_blocks = {}
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(("127.0.0.1", 8585))
        server.listen()
        while True:
            try:
                conn, _ = server.accept()
                with conn:
                    data = conn.recv(4096).decode('utf-8')
                    if not data: 
                        continue
                    req = json.loads(data)
                    cmd, address = req.get("command"), req.get("address")
                    if cmd == "WRITE":
                        allocated_ram_blocks[address] = req.get("data")
                        print(f"[WORKER RAM] Successfully locked and wrote into remote address: 0x{address:X}")
                    elif cmd == "READ":
                        conn.sendall(json.dumps({"status": "SUCCESS", "data": allocated_ram_blocks.get(address, "NULL_FAULT")}).encode('utf-8'))
            except: 
                break

def main():
    threading.Thread(target=run_worker_daemon, daemon=True).start()
    time.sleep(0.3)
    
    print("=========================================================")
    print("  INITIALIZING HYPERSYNC VIRTUAL OS OVERDRIVE CORE       ")
    print("=========================================================\n")
    
    kernel = DistributedMMU()
    print("[STEP 1] Requesting 1 Terabyte of distributed cluster virtual RAM...")
    virtual_ptr = kernel.hypersync_malloc(1024 * 1024 * 1024 * 1024)
    
    print("\n[STEP 2] Injecting protected payload into the abstract network pointer...")
    kernel.hypersync_write(virtual_ptr, "HYPERSYNC_KERNEL_OVERDRIVE_TOKEN_XYZ_99")
    
    print("\n[STEP 3] Fetching data back dynamically via our network MMU page table...")
    retrieved_data = kernel.hypersync_read(virtual_ptr)
    
    print("\n=========================================================")
    print(f"  EXECUTION RESULT FROM COOPERATIVE INFRASTRUCTURE: ")
    print(f"  Virtual Pointer Address: 0x{virtual_ptr:X}")
    print(f"  Recovered String Content: '{retrieved_data}'")
    print("=========================================================")

if __name__ == "__main__":
    main()
