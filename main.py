import uvicorn
from app import app # Importa a instância 'app' do módulo api

# Bloco de Execução
if __name__ == "__main__":
    # ESSENCIAL: 'api:app' é a referência ao objeto FastAPI dentro do módulo api.py
    # Usamos o reload=True para desenvolvimento.
    uvicorn.run("api:app", host="127.0.0.1", port=8000, reload=True)