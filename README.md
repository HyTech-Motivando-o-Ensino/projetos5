
### **Linguagens e ferramentas utilizadas**

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)

</br>

# Como executar o projeto

## Clonar o projeto

```bash
$ git clone https://github.com/HyTech-Motivando-o-Ensino/projetos5.git folder
$ cd folder
```

## Subir o container MySQL

> Executar o comando docker-compose.
```bash
$ docker-compose up --build
```
> Ou executar o comando Make.
```bash
$ make up
```

# Troubleshooting

## :warning: Máquinas Windows

É necessário modificar a terminação de linha do arquivo startup_script.sh
(CRLF para LF) para que ele seja reconhecido pelo container.


# Outros comandos

> Resetar o banco de dados
```bash
$ docker-compose down -v
```

> Resetar o banco de dados (Make)
```bash
$ make down-reset
```

Esse comando irá remover os containers e seus volumes, após isso é só executar o comando de subir os containers novamente.
