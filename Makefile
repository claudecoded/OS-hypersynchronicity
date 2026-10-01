# HyperSync Multi-Language Build System Configuration
CC = gcc
CARGO = cargo
CFLAGS = -Wall -Wextra -O2
LIBS = -L./target/release -lhypersync_core -lpthread -ldl -lrt

all: build-core compile-example

build-core:
	@echo "[BUILD] Compiling Rust Core Engine as Static Native Library..."
	$(CARGO) build --release

compile-example:
	@echo "[BUILD] Linking C Client application with HyperSync Core Subsystem..."
	$(CC) $(CFLAGS) examples/client_app.c -o client_app $(LIBS)

clean:
	@echo "[CLEAN] Purging build artifacts..."
	$(CARGO) clean
	rm -f client_app
