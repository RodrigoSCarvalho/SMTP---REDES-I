from socket import *
import time

serverName = 'localhost'
serverPort = 12000  # Porta onde é feita a conexão conectado.

fecha = False

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

# Recebe a mensagem de domínio do Servidor
handshaking = clientSocket.recv(1024).decode()

while fecha == False:
    helo = input(handshaking+'\n\r')  # Escreve o comando HELO

    while 1:
        clientSocket.send(helo.encode())  # Envia o Helo
        # Recebe mensagem do Servidor se foi aceito ou mensagem de erro
        boaVindas = clientSocket.recv(1024).decode()
        if boaVindas[0] == '2':  # Se começar com 2 não teve erro pode seguir
            break
        else:
            # Se houve o erro enviamos de novo o HELO
            helo = input(boaVindas+'\n\r')

# ************************ REMETENTE ******************************

    # Mostra a mensagem de aceito e enviamos o remetente
    remetente = input(boaVindas+'\n\r')

    while 1:
        # Enviamos a mensagem de remetente MAIL FROM: name
        clientSocket.send(remetente.encode())
        # Recebemos mensagem de confirmação ou erro do Servidor
        remetenteAceito = clientSocket.recv(1024).decode()
        if remetenteAceito[0] == '2':  # Se começar com 2 não teve erro

            break
        else:
            # Se teve erro podemos enviar uma nova mensagem com o remetente
            remetente = input(remetenteAceito+'\n\r')


# ************************ RECEPTOR ********************************

    # Mostra que o remetente foi aceito e enviamos o receptor RCPT TO: name
    receptor = input(remetenteAceito+'\n\r')
    while 1:

        clientSocket.send(receptor.encode())  # Envia a mensagem
        # Recebemos o retorno do Servidor
        receptorAceito = clientSocket.recv(1024).decode()
        if receptorAceito[0] == '2':  # Se incia com 2 é que está tudo certo
            break
        else:
            # Se tiver erro podemos enviar um novo comando para informar o receptor
            receptor = input(receptorAceito+'\n\r')

# ************************** DATA *********************************

    # Printa a mensagem de confirmação e escrevemos o comando DATA
    data = input(receptorAceito+'\n\r')
    while 1:
        clientSocket.send(data.encode())  # Enviamos DATA
        # Recebemos a confirmação do Servidor
        confirmData = clientSocket.recv(1024).decode()
        if confirmData[0] == '3':  # Se começar com 3, podemos começar a escrever a mensagem em sí
            break
        else:
            # Caso haja erro podemos enviar de novo o comando DATA
            data = input(confirmData+'\r\n')

    print(confirmData)

    while 1:
        mensagem = input()  # Escrevemos a mensagem
        clientSocket.send(mensagem.encode())
        mensagem = str(mensagem)
        # Se a mensagem for um . sozinho em uma linha encerramos a mensagem
        if mensagem[0] == '.' and len(mensagem) == 1:
            break

    # Recebos uma mensagem de confirmação de e-mail enviado
    encerraMensagem = clientSocket.recv(1024).decode()

    # Mostra a mensagem e temos a opção de enviar QUIT para encerrar a conexão
    quitando = input(encerraMensagem+'\n\r')
    clientSocket.send(quitando.encode())  # Enviamos a mensagem
    if quitando == 'QUIT':  # Se decidirmos por encerrar
        # Receberemos uma mensagem de despedida
        despedida = clientSocket.recv(1024).decode()
        print(despedida)
        # 2 segundos para poder ver a mensagem e não encerrar automáticamente
        time.sleep(2)
        fecha = True  # FIM do programa

    # Caso não seja enviado QUIT temos a opção de começar um novo envio de e-mail

clientSocket.close()
