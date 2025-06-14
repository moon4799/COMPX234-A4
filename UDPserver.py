import sys, socket, os, threading, base64

def handle_client_thread(filename, data_port, client_addr):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("", data_port))
    print(f"[Server] Handling {filename} on port {data_port}")
    with open(filename, "rb") as f:
        while True:
            try:
                data, addr = sock.recvfrom(2048)
                msg = data.decode().strip()
                parts = msg.split()
                if parts[0] == "FILE" and parts[2] == "CLOSE":
                    sock.sendto(f"FILE {filename} CLOSE_OK".encode(), addr)
                    break
                if parts[0] == "FILE" and parts[2] == "GET":
                    start = int(parts[4])
                    end = int(parts[6])
                    f.seek(start)
                    chunk = f.read(end - start + 1)
                    encoded = base64.b64encode(chunk).decode()
                    reply = f"FILE {filename} OK START {start} END {end} DATA {encoded}"
                    sock.sendto(reply.encode(), addr)
            except Exception as e:
                print("[Server] Error:", e)
                break
    sock.close()
