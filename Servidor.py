import socket

def start_server(host, puerto):
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind((host, puerto))
    servidor.listen(2)
    print('Servidor iniciado en', host, ':', puerto)
    print('Esperando conexiones...')
    while True:
        cliente, direccion = servidor.accept()
        print('Conexión establecida desde:', direccion)
        mensaje = cliente.recv(1024).decode().strip()
        read_log(mensaje)
        print("Recibido:", mensaje)
        if mensaje == "stop":
            cliente.close()
            servidor.close()
            print("Servidor detenido")

def read_log(msg):
    archivo = open("d:/Snake_LAN/log.txt", "w")
    archivo.write(msg)
    archivo.close()

if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    host = s.getsockname()[0]
    puerto = 7800
    s.close()
    start_server(host, puerto)

else:
    print("Inicializado como módulo")