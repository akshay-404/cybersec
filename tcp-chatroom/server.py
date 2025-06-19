import socket
import threading
import json

def ipv4():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ipv4addr = s.getsockname()[0]
    s.close()
    return ipv4addr

ADDR = ("127.0.0.1", 12345)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
server.listen()

clients, nicknames = [], []
lock = threading.Lock()

def jsontotext(jsondata):
    try:
        data = json.loads(jsondata)
        return data['msg'], data['cli']
    except (json.JSONDecodeError, KeyError):
        return '',''
    
def texttojson(msg, cli):
    try:
        return json.dumps({'msg': msg, 'cli': cli})
    except TypeError:
        return ''

def broadcast(data, bool=False):
    msg, cli = jsontotext(data.decode())
    print(f'[BROADCAST] {cli}: {msg}')
    with lock:
        for client in clients:
            try:
                client.send(data)
            except Exception as e:
                if not bool:
                    print(f"[ERROR] Error broadcasting to {nicknames[clients.index(client)]} : {e}")

def handle_client(client, addr):
    print(f"[CONN] Connected with {addr}")
    
    client.send(texttojson('x01', 'SERVER').encode())
    data = client.recv(1024).decode()
    nickname, _ = jsontotext(data)
    with lock:
        if nickname == '':
            client.send(texttojson('e01', 'SERVER').encode())
            print(f"[ERROR] Nickname is empty or invalid.")
            print(f"[DISCONN] Connection with {addr} closed.")
            client.close()
            return
        elif nickname in nicknames:
            client.send(texttojson('e02', 'SERVER').encode())
            print(f"[ERROR] Nickname '{nickname}' already taken by another client.")
            print(f"[DISCONN] Connection with {addr} closed.")
            client.close()
            return
        else:
            nicknames.append(nickname)
            clients.append(client)

    print(f"[CONN] Nickname of {addr} : {nickname}")
    client.send(texttojson('x02', 'SERVER').encode())
    data = client.recv(1024).decode()
    hndshk, _ = jsontotext(data)
    if hndshk != 'x03':
        print(f"[ERROR] Handshake failed for {addr}. Expected 'x03', got '{hndshk}'")
        client.close()
        return
    broadcast(texttojson(f"{nickname} has joined the chat!", 'SERVER').encode())
    
    while True:
        try:
            msg = client.recv(1024)
            if not msg:
                break
            try:
                msgtext, _ = jsontotext(msg.decode())
                if msgtext.strip().lower() == 'exit':
                    print(f"[DISCONN] {nickname} has requested to exit.")
                    broadcast(texttojson(f"{nickname} requested exit.", 'SERVER').encode(), True)
                    break
            except Exception:
                pass
            broadcast(msg)
        except Exception as e:
                print(f"[ERROR] Error receiving message from {nickname} : {e}")
                break
        
    with lock:
        if client in clients:
            idx = clients.index(client)
            clients.pop(idx)
            nicknames.pop(idx)
    
    print(f"[DISCONN] {nickname} has left the chat.")
    broadcast(texttojson(f"{nickname} has left the chat.", 'SERVER').encode())

    client.close()
    print(f"[DISCONN] Connection with {addr} closed.")
    return

if __name__ == "__main__":

    print(f"[START] Server is running at {ADDR[0]}:{ADDR[1]}")
    while True:
        try:
            conn, addr = server.accept()
            client_thread = threading.Thread(target=handle_client, args=(conn,addr))
            client_thread.start()
            print(f"[CONN] Active connection : {threading.active_count()-1}")

        except KeyboardInterrupt:
            print("\n[STOP] Server is shutting down...")
            for client in clients:
                client.close()
            server.close()
            exit()
