# Discord2.0
Discord visto pelos olhos de um bot

Este projeto foi desenvolvido como apenas uma brincadeira, não como uma maneira de abusar da API do discord.

O projeto consiste em um bot que ultiliza a API do discord para mandar informações para um segundo programa, que mostrará elas em uma UI parecida ao Discord, sendo possível apenas ler e mandar mensagens em canais de texto.

Foi utilizado a biblioteca PyQt6 juntamente com o Qt Designer para a criação da UI.

A comunicação entre os 2 arquivos é feita por um servidor local

![image](https://user-images.githubusercontent.com/94933775/153419030-57009821-8d7e-4e66-bfc8-c8b655553c60.png)


Para rodar o programa, primeiro deve-se criar um bot em: https://discord.com/developers/applications

Depois insira o Token dele na ultima linha do arquinho bot_main.py

Rode este mesmo arquivo e espere a mensage "Bot ready!" e depois rode o arquivo bot_ui_main.py

Aperte o botão "get servers" para obter a lista de servidores onde o bot faz parte.

Clique no servidor onde poderá ser visto a lista dos canais e dos membros, selecione um canal de texto e irá aparecer as 30 ultimas mensagens dele.

Para recarregar o canal clique no canal de texto novamente.


(este projeto não está totalmente finalizado e pode apresentar alguns bugs e falhas de segurança)
