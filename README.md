
A ideia do programa é simular um sistema de envio de e-mails SMTP. 
O programa está rodando na porta 12000
Para iniciar deve-se rodar primeiramente o Server.py, de preferência pelo cmd, passe por parâmetro um arquivo ‘.txt’ que contenha os endereços de e-mails dos usuários do servidor. Exemplo: “Server.py filename.txt”. A partir desse arquivo de texto lido linha por linha, será criado um arquivo.txt para cada endereço de e-mail contido nas linhas do arquivo. É bom salientar que os endereços de e-mails devem ser de mesmo domínio para fazer sentido com a mensagem exibida no momento em que a conexão é feita, e cada um em uma linha, para que a leitura seja feita de maneira correta. Caso ocorra algum erro nessa etapa, o servidor exibirá uma mensagem de erro e fechará instantaneamente. 
Após iniciado o servidor sem erros, será apresentado uma mensagem “Aguardando conexão...”. Agora é hora de abrir o ‘Client.py’, podendo ser direto pelo executável, se disponível. Ao abrir o ‘Client.py’ será impresso na tela uma mensagem de conexão provida pelo servidor, informando o domínio do servidor. O servidor estará aguardando o comando ‘HELO’.
No cliente, o usuário deverá informar o domínio de seu endereço de e-mail. Exemplo: "HELO gmail.com". Caso o usuário envie o comando de ‘HELO’ incorretamente o programa ficará em um loop até que o envio do comando seja enviado corretamente.
Não ocorrendo erro na etapa anterior, o servidor enviará uma mensagem de boas-vindas e aguardará o remetente do e-mail. Será impresso na tela do client.py a mensagem recebida, e ele poderá enviar o comando de remetente seguindo o formato: "MAIL TO: remetente@gmail". Caso ocorra um erro em algum comando, o Client.py receberá uma mensagem de erro de sintaxe. Vide que o domínio do endereço deverá ser o mesmo que o informado anteriormente, caso contrário será enviado uma mensagem de erro de endereço e deverá ser enviado novamente o comando.
Estando tudo correto, o servidor enviará uma mensagem de sucesso e aguardará por um comando de receptor. Na tela do usuário cliente será exibido esta mensagem e estará disponível o envio do comando do receptor, como no modelo: "RCPT TO: endereco@domínio". Note que o endereço informado deverá estar contido no arquivo.txt informado na inicialização do servidor. Caso contrário será recebido uma mensagem de erro de endereço. Caso ocorra erro nos comandos SMTP será recebido uma mensagem de erro de sintaxe, em ambos casos de erro será necessário enviar um novo comando de receptor.
Na nova etapa, o Client.py receberá uma mensagem do servidor confirmando que o receptor está ok e o servidor estará no aguardo do envio de um comando ‘DATA’. Caso ocorra erro no envio do comando ‘DATA’ será recebido uma mensagem de erro e um novo ‘DATA’ deverá ser entregue.
 Após o recebimento correto do comando ‘DATA’ o servidor irá abrir o arquivo do receptor e enviará um comando de aguardo de mensagem. Com isso, o cliente poderá escrever livremente a mensagem desejadas encerrando com um '.' único em uma linha separada. Recebendo esse '.' o servidor deverá informar que o e-mail foi entregue com sucesso. 
Recebendo a mensagem de confirmação o Client terá a opção de enviar um comando 'QUIT', caso enviado será recebido uma mensagem de despedida entregue pelo servidor, e encerrará a conexão. No servidor será aguardado uma nova conexão de Client.py. Se não for enviado um 'QUIT' servidor e cliente continuarão conectados 



Tela do Client.py após encerramento de conexão:

![image](https://user-images.githubusercontent.com/72170590/113429163-74e9bd00-93ae-11eb-8b32-e87bcadff2fd.png)


Tela do Server.py após encerramento de conexão com o Client.py:

![image](https://user-images.githubusercontent.com/72170590/113429383-d27e0980-93ae-11eb-87a6-3e6dd3478fa3.png)
