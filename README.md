# SMTP - REDES I

A ideia do programa é simular um sistema de envio de e-mails SMTP.

Para iniciar deve-se rodar primeiramente o Server.py de preferencia pelo cmd, passe por paramêtro um arquivo .txt contendo os endereços de e-mails dos usuários do servidor.
Exemplo: Server.py filename.txt. Nesse arquivo txt será lido linha por linha e criado um arquivo.txt para cada endereço de e-mail contido nas linhas do arquivo.


O programa está rodando na porta 12000

Após iniciado o servidor de forma correta será apresentado uma mensagem aguardando conexão. Agora é a hora de abrir o Client.py, pode ser direto pelo executável disponível.
Ao abrir o Client.py será impresso na tela do client uma mensagem de conexão do servidor informando o domínio e o servidor estará aguardando o comando HELO.

No client o usuário deverá informar o domínio de seu endereço de e-mail. Exemplo: "HELO gmail.com"
Caso o usuário envie o comando de HELO incorretamente o programa ficará em loop até que seja enviado corretamente.

Não ocorrendo erro na etapa anterior, o servidor enviará uma mensagem de boas vindas e aguardará o remetente do e-mail.
Será impresso na tela do client a mensagem recebida e ele poderá enviar o comando de remetente no formato: "MAIL TO: remetente@gmail".
Caso ocorra um erro em algum comando, o client receberá uma mensagem de erro de sintaxe. O domínio do endereço deverá ser o mesmo que o informado anteriormente, caso contrário será enviado uma mensagem de erro de endereço e deverá ser enviado novamente o comando.

Estando tudo correto, o servidor enviará uma mensagem de sucesso e agurdará por um comando de receptor.
Na tela do usuário client será exibido a mensagem e estará disponível o envio do comando do receptor. Como no modelo: "RCPT TO: endereco@domínio". Note que o endereço informado deverá estar contido no arquivo.txt informado na inicialização do servidor. Caso contrário será recebido uma mensagem de erro de endereço, e caso ocorra o erro nos comandos SMTP será recebido uma mensagem de erro de sintaxe, e será necessário enviar um novo comando de receptor.

Na nova etapa, o client receberá uma mensagem de confirmação do receptor e esperará o envio de um comando DATA. Caso ocorra erro no envio do comando DATA por parte do client será recebido uma mensagem de erro e um novo DATA deverá ser entregue.

Após o recebimento correto do comando DATA o servidor irá abrir o arquivo do receptor e enviará um comando de aguardo de mensagem. Com isso, o client poderá escrever as mensagens desejadas encerrando com um '.' único em um linha separada. 

Recebendo esse '.' o servidor deverá informar que o e-mail foi entregue. O client terá a opção de enviar um comando 'QUIT', caso enviado será recebido uma mensagem de despedida entregue pelo servidor, e fechará a conexão. No servidor será aguardado uma nova conexão de client. Se não for enviado um 'QUIT' servidor e client continuarão conectados e o usuário poderá iniciar um novo processo de envio de e-mail SMTP.




Tela do client após encerramento de conexão:

![image](https://user-images.githubusercontent.com/72170590/113429163-74e9bd00-93ae-11eb-8b32-e87bcadff2fd.png)


Tela do server após encerramento de conexão do client:

![image](https://user-images.githubusercontent.com/72170590/113429383-d27e0980-93ae-11eb-87a6-3e6dd3478fa3.png)
