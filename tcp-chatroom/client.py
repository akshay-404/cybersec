import socket
import threading
import json
import sys
import readline

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
    
def display(msg, cli):
    buffer = readline.get_line_buffer()
    sys.stdout.write('\r\033[K')
    print(f'{cli}: {msg}')
    sys.stdout.write(f'You: {buffer}')
    sys.stdout.flush()

def receiveMsg():
    while True:
        try:
            msg, cli = jsontotext(client.recv(1024).decode())
            if msg:
                if cli == nickname:
                    pass
                else:
                    display(msg, cli)
        except Exception as e:
            print(f"Error receiving message: {e}")
            break

def sendMsg():
    while True:
        sys.stdout.write('You: ')
        sys.stdout.flush()
        msg = input()
        if msg.strip().lower() == 'exit':
            try:
                client.send(texttojson(msg, nickname).encode())
            except Exception as e:
                print(f"Failed to send message : {e}")
            client.close()
            print(f'Disconnected from server.')
            break
        try:
            client.send(texttojson(msg, nickname).encode())
        except Exception as e:
            print(f"Failed to send message : {e}")

try:
    HOST = input("Enter server IP address: ")
    PORT = int(input("Enter server port: "))
    ADDR = (HOST, PORT)

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)

    print(f"Connected to server at {HOST}:{PORT}")

    hndshk, cli = jsontotext(client.recv(1024).decode())
    if hndshk == 'x01' and cli == 'SERVER':
        sys.stdout.flush()
        nickname = input("Enter your nickname: ")
        client.send(texttojson(nickname, 'client').encode())
    else:
        print("Handshake failed. Server did not respond as expected.")
        exit(1)

    hndshk, cli = jsontotext(client.recv(1024).decode())
    if hndshk == 'x02' and cli == 'SERVER':
        client.send(texttojson("x03", nickname).encode())
        print(f'Joined chat as {nickname}')
    elif hndshk == 'e01' and cli == 'SERVER':
        print(f'Nickname is empty or invalid. Please try again.')
        exit(2)
    elif hndshk == 'e02' and cli == 'SERVER':
        print(f'Nickname \'{nickname}\' is already taken.')
        exit(3)
    else:
        print("Handshake failed. Server did not respond as expected.")
        exit(4)

except Exception as e:
    print(f"Could not connect to server: {e}")
    exit(5)

threading.Thread(target=receiveMsg, daemon=True).start()
sendMsg()
