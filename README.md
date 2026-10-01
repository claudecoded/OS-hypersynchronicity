# OS-HyperSync-Core v1.0.0

A high-performance architectural concept and functional simulator of **Distributed Shared Memory (DSM)** and **Virtual Network Memory Management Units (MMU)**. This project demonstrates how to bypass local hardware RAM constraints by dynamically pooling abstract memory addresses across a decentralized system grid.

## 🧠 Architectural Concepts Inside

* **Virtual MMU Allocation:** Intercepts logical allocation calls and maps pages across a custom `0x80000000` memory boundary.
* **Transparent Network Offloading:** A low-latency daemon network thread simulates an independent remote node ceding physical hardware space.
* **Zero-Friction Portability:** Built natively to overcome local terminal encoding limitations and target environment interference.

---

## 🚀 How to Run

### Windows Users
1. Download `main.py` and `run.bat` and create a folder in your PC and move the two files to it.

<img width="850" height="311" alt="Screenshot 2026-10-01 133223" src="https://github.com/user-attachments/assets/d309de57-1bd8-4b73-8b30-6a0638bb9312" />
<img width="163" height="138" alt="Screenshot 2026-10-01 133641" src="https://github.com/user-attachments/assets/526e15cf-3f14-49cc-8d06-19c31c112691" />

2. Double-click `run.bat` to execute the simulation instantly.
Obs.: If you try to click `run.bat`, you will probably see this wraning on your screen above. But don't worry and click on the button "Run" anyways.

<img width="1361" height="768" alt="image" src="https://github.com/user-attachments/assets/d71fd9f2-8df0-41a5-b0e5-50f975dee87c" />

After that, the terminal window will open and the simulation will be executed instantly.

<img width="637" height="462" alt="image" src="https://github.com/user-attachments/assets/faa2e23d-e01e-4be5-a960-cda6dc4889b7" />
---

### Linux & macOS Users
Run the script directly via terminal:
```bash
python3 main.py
```

---

## 📊 Expected System Telemetry

When executed, the core engine overrides the local landscape and logs the initialization sequence:

1. **System Discovery:** Binds an ephemeral memory socket at `127.0.0.1:8585` representing the remote hardware cluster.
2. **Virtual Mapping:** Maps a simulated **1 Terabyte block of abstract memory pages** inside the custom MMU layout.
3. **Cluster Sync:** Offloads an explicit protected data payload matrix past local physical OS boundaries.
4. **State Recovery:** Reclaims and decodes the string contents natively across the grid layout, showcasing successful synchronization.

---

## 🛠️ Feature Roadmap & Future Spec
* [ ] **Sub-OS Hypervisor Integration:** Injecting execution memory maps below Ring 0 permissions.
* [ ] **Cryptographic Page Obfuscation:** End-to-end zero-knowledge encryption on raw RAM offloads.
* [ ] **Quantum Memory Compression:** Real-time bitwise payload packing over raw TCP/IP sockets.
