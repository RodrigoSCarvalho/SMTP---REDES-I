# Algumas bibliotecas
from socket import *
import os
import re
import sys
import time
serverPort = 12000  # PORTA CONECTADA

serverSocket = socket(AF_INET, SOCK_STREAM)  # SOCKET TCP

# CONSTANTES DE ERRO
ERRO_DE_SINTAXE = '500 Syntax error, command unrecognized'
ERRO_DE_ENDERECO = '550 Address unknown'


def TrataHelo(connectionSocket):  # Verifica se tem erros na declaração do HELO
    while 1:
        # Recebe helo do socket client
        helo = connectionSocket.recv(1024).decode()
        helo = helo.split(' ')  # Divide pelo espaço
        if len(helo) == 2:  # O helo tem que ter 2 posições helo + domínio
            if helo[0] == 'HELO' and helo[1] != ' ':
                global dominioRemetente
                # Guarda a informação de domínio do remetente
                dominioRemetente = helo[1]
                heloOk = ('250 Hello '+dominioRemetente +
                          ', pleased to meet you')
                # Envia a mensagem de apresentação
                connectionSocket.send(heloOk.encode())
                break  # Se chegou aqui não tem erro, sai do while
            else:
                print(ERRO_DE_SINTAXE)
                connectionSocket.send(ERRO_DE_SINTAXE.encode())

        else:  # Se o helo nao tiver exatamento 2 palavras enviaremos a mensagem de erro e esperamos por um novo helo
            print(ERRO_DE_SINTAXE)
            connectionSocket.send(ERRO_DE_SINTAXE.encode())


# Tratamento de remetente "MAIL FROM: x" e resolução de erros
def TrataRemetente(connectionSocket):
    while 1:

        # Recebe  o "MAIL FROM: X" do client
        remetente = connectionSocket.recv(1024).decode()
        # Divide a mensagem recebida pelos espaços
        tokensMailFrom = remetente.split(' ')

        if len(tokensMailFrom) == 3:  # Formato de mensagem de remetente tem que ser de 3 posições
            # Divide a terceira posição recebida por "MAIL FROM: x" pelo @ para que se possa comparar com o dominio do remetente
            remetente = tokensMailFrom[2].split('@')
            # Compara se os comandos estão corretos
            if tokensMailFrom[0] == 'MAIL' and tokensMailFrom[1] == 'FROM:':
                if dominioRemetente in remetente:  # Verifica se os dominios coincidem
                    contato = ('250 '+tokensMailFrom[2]+'... Sender ok')
                    print(contato)
                    # Envia mensagem confirmando sender
                    connectionSocket.send(contato.encode())
                    break  # Não teve erro, sai do while e passa para a proxima etapa
                else:  # Trata e envia mensagem de erro caso o erro seja no endereço
                    print(ERRO_DE_ENDERECO)
                    connectionSocket.send(ERRO_DE_ENDERECO.encode())
        else:  # trata e envia mensagem de erro caso o erro aconteceu em algum comando
            print(ERRO_DE_SINTAXE)
            connectionSocket.send(ERRO_DE_SINTAXE.encode())


def TrataReceptor(connectionSocket):  # Tratar erros e confirmar o receptor "RCPT TO: x"
    while 1:
        # Recebe a mensagem informando o receptor
        receptor = connectionSocket.recv(1024).decode()
        global tokensMailTo
        tokensMailTo = receptor.split(' ')  # Divide a mensagem pelo espaço
        if len(tokensMailTo) == 3:  # Mensagem deve ter 3 posições
            global mailRCPT
            # MailRCPT irá receber o dominio informado pelo client
            mailRCPT = tokensMailTo[2]
            # Confere se os comandos estão corretos
            if tokensMailTo[0] == "RCPT" and tokensMailTo[1] == "TO:":
                if mailRCPT in contatos:  # Se o destinatário informado pelo client existir no nosso arquivo inicial
                    mensagemDeContato = ('250 '+mailRCPT+' ... Recipient ok')
                    print(mensagemDeContato)
                    # Envia mensagem de confirmação
                    connectionSocket.send(mensagemDeContato.encode())
                    # Não tivemos erros, sai do while, segue para a proxima etapa.
                    break
                else:  # Erro no destinatário informado
                    print(ERRO_DE_ENDERECO)
                    connectionSocket.send(ERRO_DE_ENDERECO.encode())

        else:  # Erro em algum comando
            print(ERRO_DE_SINTAXE)
            connectionSocket.send(ERRO_DE_SINTAXE.encode())


def TrataMensagem(connectionSocket):  # Trata a mensagem e a data
    while 1:
        data = connectionSocket.recv(1024).decode()
        if data == "DATA" or data == "data":  # Verifica se foi passado corretamente o comando DATA
            podeEnviar = "354 Start mail input; End with '.'"
            # Envia mensagem de confirmação
            connectionSocket.send(podeEnviar.encode())
            # Sem erro no comando, sai do while e passa para a próxima etapa.
            break
        else:  # Erro no comando DATA
            print(ERRO_DE_SINTAXE)
            connectionSocket.send(ERRO_DE_SINTAXE.encode())

    # Abre a caixa de mensagem do destinatário
    with open(tokensMailTo[2]+".txt", 'a') as mail:
        print("Esperando a mensagem \n")
        while 1:
            mensagem = connectionSocket.recv(
                1024).decode()  # Recebe a mensagem
            # Se receber o . encerraremos a mensagem
            if mensagem[0] == '.' and len(mensagem):
                print("Encerrando a mensagem \r\n")
                mail.write('\r\n')
                break  # Fecha a mensagem

            mail.write(mensagem+'\n')  # Escreve a mensagem na caixa
        mensagemEnviada = ('250 Message accepted for delivery')
        # Envia mensagem de confirmação de mensagem entregue.
        connectionSocket.send(mensagemEnviada.encode())


serverSocket.bind(('localhost', serverPort))

serverSocket.listen(1)  # Escuta uma conexão
print('O servidor esta online...\n')
contatos = []  # Vetor para os endereçoes de e-mail informados no arquivo de entrada

# Ler o arquivo
try:
    argumentos = sys.argv  # arquivo passado como parâmetro na inicialização do Server
    nomeArquivo = argumentos[1]
    with open(nomeArquivo, 'r') as file:  # Abrimos o arquivo
        for data in file.readlines():
            linha = str(data).strip('\n')  # dividimos pelo \n
            # a cada linha será acrescentado em nosso vetor de contato os domínios informados no arquivo
            contatos.append(linha)

            name = str(data)
            # tira-se o \n para a criação das caixas de entrada
            name = name.rstrip('\n')
            # Criar arquivos dos usuários
            # criamos um .txt para cada usuário informado no arquivo
            arquivo = open(name+".txt", 'a')
            arquivo.writelines('')
            arquivo.close

except Exception:  # Erro
    print("Arquivo não existe ou não está no formato esperado. \n")
    serverSocket.close()

# Pegamos o domínio do endereço de contato / todos os endereços devem pertencer ao mesmo domínio/servidor de e-mail
pegarDominio = contatos[0]
pegarDominio = str(pegarDominio).split('@')
dominio = pegarDominio[1]


# Iniciar o programa
while 1:
    # Aguardando o endereço
    print("Aguardando conexão...\n")
    connectionSocket, addr = serverSocket.accept()

    handshaking = ('220 '+dominio)  # O Servidor irá se apresentar
    print(handshaking+'\n')
    connectionSocket.send(handshaking.encode())

    while 1:

        print("Aguardando Helo...\n\r")

        TrataHelo(connectionSocket)

        print("Aguardando remetente...\r\n")

        TrataRemetente(connectionSocket)

        print("Aguardando receptor...\r\n")
        TrataReceptor(connectionSocket)

        TrataMensagem(connectionSocket)

        quitou = connectionSocket.recv(1024).decode()

        if quitou == 'QUIT':  # Caso o client envie o comando QUIT o Servidor enviará uma mensagem de despida e aguardará por uma nova conexão
            print('Encerrando conexão \r\n')
            despedida = ('221 '+dominio+' closing connection')
            connectionSocket.send(despedida.encode())
            break
        # Caso não envie QUIT o Client pode enviar um novo e-mail na mesma conexão.

connectionSocket.close()


serverSocket.close()
