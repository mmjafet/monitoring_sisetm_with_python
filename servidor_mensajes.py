import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
from plantilla import create_button, centrar_frame_principal

clients = []

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

def start_server(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = get_local_ip()
    server_socket.bind((host, port))
    server_socket.listen(5)

    text_area.insert(tk.END, f"Conéctate a la IP: {host} y el puerto: {port}...\n")

    while True:
        client_socket, addr = server_socket.accept()
        clients.append((client_socket, addr))
        text_area.insert(tk.END, f"Conexión establecida con {addr}\n")
        threading.Thread(target=handle_client, args=(client_socket, addr)).start()

def handle_client(client_socket, addr):
    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            message = f"Mensaje de {addr}: {data.decode()}\n"
            text_area.insert(tk.END, message)
            text_area.see(tk.END)
            broadcast_message(data, addr)
    except Exception as e:
        text_area.insert(tk.END, f"Error con {addr}: {e}\n")
    finally:
        client_socket.close()
        clients.remove((client_socket, addr))
        text_area.insert(tk.END, f"Cerrando conexión con {addr}\n")

def broadcast_message(message, sender_addr):
    for client, addr in clients:
        if addr != sender_addr:
            try:
                formatted_message = message.decode() if sender_addr is None else f"Cliente {sender_addr}: {message.decode()}"
                client.sendall(formatted_message.encode())
            except Exception as e:
                text_area.insert(tk.END, f"Error enviando mensaje: {e}\n")

def start_server_thread():
    threading.Thread(target=start_server, args=(port,), daemon=True).start()
    text_area.insert(tk.END, "Servidor iniciado...\n")

def send_message():
    message = message_entry.get()
    if message:
        broadcast_message(message.encode(), None)
        text_area.insert(tk.END, f"Tú: {message}\n")
        text_area.see(tk.END)
        message_entry.delete(0, tk.END)

root = tk.Tk()
root.title("Servidor de Chat")
root.configure(bg="#0f1440")

label = tk.Label(root, text="Servidor de mensajes", font=("Arial", 18, "bold"), fg="#cdd4ea", bg="#0f1440")
label.pack(pady=(10, 5))

text_area = scrolledtext.ScrolledText(root, width=50, height=20, font=("Sans-Serif", 12, "bold"),
                                      fg="#0f1440", bg="#cdd4ea")
text_area.pack(padx=20, pady=20)

message_frame = tk.Frame(root, bg="#0f1440")
message_frame.pack(padx=10, pady=10)

message_entry = tk.Entry(message_frame, width=40, font=("Sans-Serif", 12, "bold"), fg="#ffffff", bg="#636cb4")
message_entry.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

send_button = create_button(message_frame, ">", send_message)
send_button.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

port = 12345

start_button = create_button(root, "Iniciar Servidor", start_server_thread)
start_button.pack(pady=10)

centrar_frame_principal(root)
root.mainloop()
