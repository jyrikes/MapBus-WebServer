# Projeto MapBus

Bem-vindo ao repositório do projeto MapBus! Este é um sistema de monitoramento de rotas e horários de ônibus desenvolvido como parte da disciplina de Projeto 2 do curso de Engenharia da Computação da UABJ-UFRPE.

## Descrição do Projeto

O MapBus é um sistema web baseado em Python Flask que permite aos usuários acompanhar as rotas e horários dos ônibus em tempo real. Ele oferece recursos como:

- Visualização de mapas com rotas de ônibus.
- Informações sobre horários de chegada e partida.
- Inserção de novas rotas nos sistema 

## Como Usar a API

### Pré-requisitos

Antes de começar, certifique-se de ter os seguintes requisitos instalados:

- Python 
- Flask 


### Instalação

1. Clone este repositório em sua máquina local:

   ```bash
   git@github.com:jyrikes/MapBus-WebServer.git
   ```
2. Instale o requirements.txt
   ``` bash
      pip install -r requirements.txt
   
### Link servidor 
   ```bash
   https://transporteuabj.pythonanywhere.com
```
### Rotas da API
1./user
  > Get and Set
```bash
    Localizacao{
            horario*	string
            title: Horario
            latitude*	number
            title: Latitude
            longitude*	number
            title: Longitude
            rota_id*	integer
            title: Rota Id
}
```
2. /server
  > Get and set
```bash  	
Response body
Download
Rota{
  horario*: string,
  nome_ponto*: string,
  rota_id: INTEGER
}
```

