import sys

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 UDPserver.py <port>")
        sys.exit(1)
    port = int(sys.argv[1])
    print(f"[Server] Starting server on port {port}")
