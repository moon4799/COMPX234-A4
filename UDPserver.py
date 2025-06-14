import sys, socket, os

if __name__ == "__main__":
    port = int(sys.argv[1])
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(("", port))
    print("[Server] Listening for DOWNLOAD requests...")

    while True:
        data, client_addr = server_socket.recvfrom(1024)
        message = data.decode().strip()
        if message.startswith("DOWNLOAD"):
            parts = message.split()
            if len(parts) != 2:
                continue
            filename = parts[1]
            if not os.path.isfile(filename):
                err_msg = f"ERR {filename} NOT_FOUND"
                server_socket.sendto(err_msg.encode(), client_addr)
                continue
            file_size = os.path.getsize(filename)
            port_data = 50000 + os.getpid() % 1000
            ok_msg = f"OK {filename} SIZE {file_size} PORT {port_data}"
            server_socket.sendto(ok_msg.encode(), client_addr)
