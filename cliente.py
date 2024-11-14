import socket
import threading

HOST = '192.168.70.188'
PORTA = 9999

def enviar_msg(servidor):
    while True:
        try:
            msg = input("MENSAGEM: ")
            servidor.sendall(msg.encode())
        except:
            print("_____FALHA AO ENVIAR MENSAGEM_____")

def recebe_msg(servidor):
    while True:
        try:
            mensagem = servidor.recv(1024).decode()
            print(f"{mensagem}")
        except:
            print("_____ERRO AO RECEBER MENSAGEM DO SERVIDOR_____ ")
            servidor.close()
            return


cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect((HOST, PORTA))
nome = input("___INFORME SEU NOME: ")
cliente.sendall(nome.encode())
print("_____CHAT INICIADO_____")
print("COMANDOS")
print(" <sair> : PARA SAIR DO CHAT")
print("PARA FAZER UNICAST:")
print("1-DIGITAR <unicast>")
print("2-DIGITAR O NOME DO CLIENTE PARA O QUAL VOCE DESEJA ENVIAR A MENSAGEM")
print("3-DIGITAR A MENSAGEM")
print("________________________________________________________________")
print("")


thread_recebe = threading.Thread(target=recebe_msg, args=(cliente,))
thread_recebe.start()

thread_enviar = threading.Thread(target=enviar_msg, args=(cliente,))
thread_enviar.start()
