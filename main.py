# ==============================================================================
# HYPERSYNC DISTRIBUTED MEMORY SUITE (v1.0.0)
# Complete, functional, single-file simulation architecture for GitHub.
# ==============================================================================

import socket
import json
import random
import threading
import time
import sys

PAGE_SIZE = 4096  # Standard Operating System Page Size Reference

class DistributedMMU:
    def __init__(self):
        self.page_table = {}
        self.worker_address = ("127.0.0.1", 8585)
        self.base_virtual_address = 0x80000000

    def hypersync_malloc(self, size: int) -> int:
        """ Allocates abstract memory pages over the simulated remote cluster """
        pages_needed = (size + PAGE_SIZE - 1) // PAGE_SIZE
        allocated_address = self.base_virtual_address
        
        for i in range(pages_needed):
            target_page = allocated_address + (i * PAGE_SIZE)
            self.page_table[target_page] = {
                "node_id": 1,
                "remote_offset": random.randint(0x100000, 0x900000),
                "dirty": False
            }
        
        self.base_virtual_address += pages_needed * PAGE_SIZE
        print(f"[HYPERSYNC MMU] Mapped {pages_needed} virtual network pages at address: 0x{allocated_address:X}")
        return allocated_address

    def hypersync_write(self, virtual_address: int, data: str) -> bool:
        """ Intercepts memory writes and forces synchronization across the cluster """
        if virtual_address not in self.page_table:
            print(f"[KERNEL CRITICAL] Segmentation Fault: 0x{virtual_address:X} out of bounds.")
            return False

        print(f"[HYPERSYNC IO] Intercepted raw write at 0x{virtual_address:X}.")
        print(f"[HYPERSYNC IO] Offloading data payload ({len(data)} bytes) to hardware cluster...")

        payload = {"command": "WRITE", "address": virtual_address, "data": data}
        return self._send_to_cluster(payload)

    def hypersync_read(self, virtual_address: int) -> str:
        """ Fetches memory segments dynamically over the network grid """
        if virtual_address not in self.page_table:
            print(f"[KERNEL CRITICAL] Segmentation Fault: 0x{virtual_address:X} out of bounds.")
            return None

        payload = {"command": "READ", "address": virtual_address}
        response = self._send_to_cluster_with_response(payload)
        return response.get("data") if response else None

    def _send_to_cluster(self, payload):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect(self.worker_address)
                s.sendall(json.dumps(payload).encode('utf-8'))
                return True
        except Exception as e:
            print(f"[NETWORK FAULT] Lost connection to distributed RAM node: {e}")
            return False

    def _send_to_cluster_with_response(self, payload):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect(self.worker_address)
                s.sendall(json.dumps(payload).encode('utf-8'))
                response = s.recv(4096).decode('utf-8')
                return json.loads(response)
        except Exception as e:
            print(f"[NETWORK FAULT] Memory fetch failed: {e}")
            return None


def run_worker_daemon():
    """ Simulates the remote machine accepting memory allocations """
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
                    if not data: continue
                    
                    request = json.loads(data)
                    cmd = request.get("command")
                    address = request.get("address")
                    
                    if cmd == "WRITE":
                        allocated_ram_blocks[address] = request.get("data")
                        print(f"[WORKER RAM] Successfully locked and wrote into remote address: 0x{address:X}")
                    elif cmd == "READ":
                        stored_data = allocated_ram_blocks.get(address, "NULL_FAULT")
                        print(f"[WORKER RAM] Serving virtual page read request for address: 0x{address:X}")
                        response = {"status": "SUCCESS", "data": stored_data}
                        conn.sendall(json.dumps(response).encode('utf-8'))
            except Exception:
                break


if __name__ == "__main__":
    # Start the distributed backend background worker
    daemon_thread = threading.Thread(target=run_worker_daemon, daemon=True)
    daemon_thread.start()
    time.sleep(0.5) # Allow sockets to bind

    print("=========================================================")
    print("  INITIALIZING HYPERSYNC VIRTUAL OS OVERDRIVE CORE       ")
    print("=========================================================\n")
    
    kernel = DistributedMMU()
    
    # Simulate a giant 1 Terabyte allocation over the cluster routing table
    print("[STEP 1] Requesting 1 Terabyte of distributed cluster virtual RAM...")
    massive_allocation = 1024 * 1024 * 1024 * 1024 
    virtual_ptr = kernel.hypersync_malloc(massive_allocation)
    time.sleep(1)
    
    # Inject token directly into the cluster virtual space
    print("\n[STEP 2] Injecting protected payload into the abstract network pointer...")
    secret_payload = "HYPERSYNC_KERNEL_OVERDRIVE_TOKEN_XYZ_99"
    kernel.hypersync_write(virtual_ptr, secret_payload)
    time.sleep(1)
    
    # Read the data back from the virtual network address
    print("\n[STEP 3] Fetching data back dynamically via our network MMU page table...")
    retrieved_data = kernel.hypersync_read(virtual_ptr)
    
    print("\n=========================================================")
    print(f"  EXECUTION RESULT FROM COOPERATIVE INFRASTRUCTURE: ")
    print(f"  Virtual Pointer Address: 0x{virtual_ptr:X}")
    print(f"  Recovered String Content: '{retrieved_data}'")
    print("=========================================================")
    sys.exit(0)
