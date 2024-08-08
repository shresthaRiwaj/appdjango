import socket
import threading

def handle_client(client_socket, filename):
    try:
        with open(filename, 'rb') as file:
            content = file.read()
            response = f"HTTP/1.1 200 OK\r\nContent-Length: {len(content)}\r\n\r\n{content}"
    except FileNotFoundError:
        response = "HTTP/1.1 404 Not Found\r\n\r\nFile Not Found"

    client_socket.send(response.encode('utf-8'))
    client_socket.close()

def run_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('127.0.0.1', 8080))
    server.listen(5)

    print("[+] Listening on port 8080")

    while True:
        client_socket, addr = server.accept()
        print(f"[+] Accepted connection from {addr[0]}:{addr[1]}")
        threading.Thread(target=handle_client, args=(client_socket, "serverinfo.txt")).start()

def run_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 8080))

    filename = "serverinfo.txt"
    request = f"GET /{filename} HTTP/1.1\r\nHost: 127.0.0.1:8080\r\n\r\n"
    client.send(request.encode('utf-8'))

    response = client.recv(4096).decode('utf-8')
    headers, content = response.split('\r\n\r\n', 1)

    print(f"Content received from server:\n{content}") if "200 OK" in headers else print(f"Error: {headers}")

    client.close()

if __name__ == "__main__":
    threading.Thread(target=run_server).start()
    import time; time.sleep(1)
    run_client()
