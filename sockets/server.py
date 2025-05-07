import socket
import threading

HEADER = 64 # Tells the server how big the incoming message is
PORT = 9999
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def handle_client(conn, addr):
  print(f"[NEW CONNECTION] {addr} connected.")

  connected = True
  while connected:
    msg_length = conn.recv(HEADER).decode(FORMAT) # Blocking, therefore it should run in a thread
    if msg_length:
      msg_length = int(msg_length) # Cast to int
      msg = conn.recv(msg_length).decode(FORMAT)
      if msg == DISCONNECT_MESSAGE:
        connected = False
      print(f"[{addr}] {msg}")
      conn.send("Message received".encode(FORMAT))
  
  conn.close() # Cleanly disconnect


def start():
  server.listen()
  print(f"[LISTENING] Server is listening on {SERVER}")
  while True:
    conn, addr = server.accept() # Blocks execution until a connection occurs
    thread = threading.Thread(target=handle_client, args=(conn, addr))
    thread.start()
    print(f"[ACTIVE CONNECTIONS] {threading.active_count() -1}")


print("Starting Server")
start()

