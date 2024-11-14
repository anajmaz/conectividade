import socket
import threading

HOST = '0.0.0.0'
PORTA = 9999

def recebe_dados(cliente, endereco, clientes):
    nome = cliente.recv(50).decode()
    print(f"Conexão bem sucedida com {nome} via endereço: {endereco[0]}:{endereco[1]}")
    clientes[nome] = cliente
    broadcast(clientes, f" {nome} se juntou ao chat")
    while True:
        try:
            mensagem = cliente.recv(1024).decode()
            if mensagem == "<sair>":
                broadcast(clientes , f"_____{nome} ABANDONOU O CHAT_____")
                cliente.close()
            elif mensagem == "<unicast>":
                unicast(clientes , cliente , nome)
            else:    
                print(f"Cliente >> {mensagem}")
                broadcast(clientes, f"{nome}: {mensagem}")
        except:
            print("Erro ao receber mensagem... fechando")
            cliente.close()
            return


def broadcast(clientes , msg):
    for cliente in clientes.values():
        try:
            cliente.sendall(msg.encode())
        except:
            print("_____FALHA AO ENVIAR BROADCAST_____")


def unicast(clientes , emissor , nome):
    emissor.sendall("_____PRA QUEM VOCE DESEJA ENVIAR UNICAST_____".encode())
    nome_destino = emissor.recv(1024).decode()
    emissor.sendall("_____ESCREVA A MENSAGEM DO UNICAST_____".encode())
    mensagem = emissor.recv(1024).decode()
    try:
        clientes[nome_destino].sendall(f"{nome}: {mensagem}".encode())
        emissor.sendall("_____UNICAST ENVIADO COM SUCESSO_____".encode())
    except:
        emissor.sendall("_____FALHA AO ENVIAR UNICAST_____".encode())






endereco = (HOST , PORTA)
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind(endereco)
print(f"_____SERVIDOR INICIADO EM {HOST}:{PORTA} E AGUARDA CONEXOES_____")
servidor.listen(1)
clientes = {}

while True:
    cliente, endereco = servidor.accept()
    print(f"_____NOVA CONEXAO NO ENDERECO {endereco[0]}:{endereco[1]}")
    thread_cliente = threading.Thread(target=recebe_dados, args=(cliente, endereco, clientes))
    thread_cliente.start()