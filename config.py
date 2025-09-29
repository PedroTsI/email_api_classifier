import os
from dotenv import load_dotenv
from google import genai

# Carrega variáveis do .env
load_dotenv()

# Configuração da Chave de API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    print("\nERRO: A variável de ambiente GEMINI_API_KEY não foi encontrada!")
    print("Crie um arquivo .env na mesma pasta com GEMINI_API_KEY=\"SUA_CHAVE_AQUI\"\n")

# Inicialização do Cliente Gemini
try:
    client = genai.Client(api_key=GEMINI_API_KEY)
except Exception:
    client = None # O cliente pode ser None se a chave falhar, e isso será tratado no ai_service.py

# Verifica a disponibilidade do pypdf (para File Processor)
try:
    import pypdf
except ImportError:
    pypdf = None
