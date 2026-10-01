#ifndef HYPERSYNC_H
#define HYPERSYNC_H

#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

/**
 * Allocates a block of memory dynamically offloaded to the distributed hardware pool.
 * Returns a virtual pointer that bypasses local OS RAM restrictions.
 */
void* hypersync_malloc(size_t size);

/**
 * Synchronizes local buffer data directly into the remote clustered virtual memory pointer.
 */
int hypersync_write(void* ptr, const void* buffer, size_t size);

#ifdef __cplusplus
}
#endif

#endif // HYPERSYNC_H
