# 🚀 FastAPI Application

Este projeto é uma API desenvolvida em **Python** utilizando o framework **FastAPI**.

## 📋 Pré-requisitos

Antes de começar, certifique-se de ter instalado:

- [Python 3.9+](https://www.python.org/downloads/)
- [pip](https://pip.pypa.io/en/stable/installation/)

## ⚙️ Instalação

1. Clone este repositório:
   ```bash
   git clone https://github.com/seu-usuario/seu-repositorio.git
   cd seu-repositorio

2. Instale as dependencias 
    ```bash
    pip install -r requirements.txt

3. Crie um Arquivo .env
    
    Crie um arquivo .env e adicione a variavel GEMINI_API_KEY e adicione a chave da API do Gemini, neste formato
    GEMINI_API_KEY="SUA_CHAVE" 

4. Rodar aplicação
    ```bash
    python3 main.py

5. Testar aplicação

    Para testar aplicação utilize Insomnia ou Postman
    Crie uma requisição POST com URL = http://127.0.0.1:8000/classify_file
    No Body adicione uma variavel com nome "file" e adicione o arquivo .txt ou .pdf e envie a requisição