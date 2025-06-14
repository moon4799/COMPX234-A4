import sys, socket, time

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
    # 省略前面的参数检查与读取文件列表逻辑
    pass
