#include <stdio.h>
#include <string.h>
#include "../Include/hypersync.h"

int main() {
    printf("[APP] Initializing HyperSync User-Space Kernel Integration...\n");

    // Requesting a giant allocation block that maps to the cluster
    // In a fully built kernel module, this bypasses local system RAM limits
    size_t massive_allocation = 1024 * 1024; // 1 Megabyte block example
    char* virtual_ram_ptr = (char*)hypersync_malloc(massive_allocation);

    if (virtual_ram_ptr == NULL) {
        printf("[ERROR] Failed to interface with HyperSync Distributed Pool.\n");
        return 1;
    }

    // Creating local payload data
    char secret_data[] = "System Overdrive Active: Pushing data directly to Remote Nodes.";
    
    printf("[APP] Executing memory offload using custom MMU Interceptor.\n");
    // Writing data directly through our custom subsystem
    int status = hypersync_write(virtual_ram_ptr, secret_data, strlen(secret_data));

    if (status == 0) {
        printf("[SUCCESS] Memory written transparently to remote cluster nodes!\n");
    } else {
        printf("[FAULT] Segmentation fault equivalent: Virtual Page not found in cluster.\n");
    }

    return 0;
}
