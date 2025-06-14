import sys

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python3 UDPclient.py <hostname> <port> <filelist>")
        sys.exit(1)
    host, port, filelist = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    print(f"[Client] Connecting to {host}:{port}, using file list {filelist}")
