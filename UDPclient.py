import sys, socket, time, base64

def send_and_receive(sock, message, server_address, retries=5):
    timeout = 0.5
    for attempt in range(retries):
        try:
            sock.sendto(message.encode(), server_address)
            sock.settimeout(timeout)
            response, _ = sock.recvfrom(2048)
            return response.decode()
        except socket.timeout:
            print(f"[Client] Timeout waiting for response. Retrying {attempt+1}/{retries}...")
            timeout *= 2
    return None

if __name__ == "__main__":
    host, port, filelist = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    with open(filelist, 'r') as f:
        filenames = [line.strip() for line in f if line.strip()]

    client_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    for filename in filenames:
        msg = f"DOWNLOAD {filename}"
        response = send_and_receive(client_sock, msg, (host, port))
        if not response:
            print(f"[Client] No response for {filename}")
            continue
        parts = response.split()
        if parts[0] == "ERR":
            print(f"[Client] File {filename} not found on server.")
            continue
        size = int(parts[4])
        data_port = int(parts[6])

        f = open(filename, "wb")
        offset = 0
        while offset < size:
            chunk_end = min(offset + 999, size - 1)
            file_req = f"FILE {filename} GET START {offset} END {chunk_end}"
            resp = send_and_receive(client_sock, file_req, (host, data_port))
            if not resp:
                print(f"[Client] Failed to receive data for {filename} at offset {offset}")
                break
            resp_parts = resp.split("DATA")
            header, encoded_data = resp_parts[0], resp_parts[1].strip()
            binary = base64.b64decode(encoded_data)
            f.seek(offset)
            f.write(binary)
            print("*", end="", flush=True)
            offset = chunk_end + 1
        close_msg = f"FILE {filename} CLOSE"
        final = send_and_receive(client_sock, close_msg, (host, data_port))
        if final and final.startswith("FILE"):
            print(f"\n[Client] Finished downloading {filename}")
        f.close()
