# main.py

import os
import io
import json

# ESSENCIAL: Para carregar a chave de API do arquivo .env
from dotenv import load_dotenv 

from fastapi import FastAPI, UploadFile, HTTPException, File
from google import genai
from google.genai import types

# --- Configuração do Leitor de PDF ---
try:
    import pypdf
except ImportError:
    pypdf = None

# -------------------------------------------------------------
# 1. CARREGA O ARQUIVO .ENV
# -------------------------------------------------------------
load_dotenv()

# --- Configuração do Gemini ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    print("\nERRO: A variável de ambiente GEMINI_API_KEY não foi encontrada!")
    print("Crie um arquivo .env na mesma pasta com GEMINI_API_KEY=\"SUA_CHAVE_AQUI\"\n")

try:
    client = genai.Client(api_key=GEMINI_API_KEY)
except Exception as e:
    pass


# --- Funções Auxiliares de Processamento de Arquivo ---

def extract_text_from_file(file: UploadFile) -> str:
    """Extrai o texto do arquivo, suportando .txt e .pdf."""
    file_extension = file.filename.split('.')[-1].lower()
    
    if file_extension == 'txt':
        try:
            return file.file.read().decode("utf-8")
        except UnicodeDecodeError:
            file.file.seek(0)
            return file.file.read().decode("iso-8859-1")

    elif file_extension == 'pdf':
        if pypdf is None:
            raise HTTPException(status_code=500, detail="Biblioteca 'pypdf' não instalada para processar PDFs.")
        
        try:
            pdf_bytes = file.file.read()
            pdf_file = io.BytesIO(pdf_bytes)
            
            reader = pypdf.PdfReader(pdf_file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Erro ao processar PDF: {e}")

    else:
        raise HTTPException(status_code=400, detail="Formato de arquivo não suportado. Use .txt ou .pdf.")


# --- Função Principal de Classificação e Geração de Resposta (Agente de IA) ---

def classify_text_with_gemini(text_content: str) -> dict:
    """Usa o modelo Gemini para classificar, extrair o assunto e gerar uma resposta."""
    if not GEMINI_API_KEY:
        return {
            "classification": "Erro de Configuração (Chave API ausente)", 
            "email_subject": "N/A",
            "auto_response": "Erro de configuração da API."
        }
        
    # O prompt define a lógica de extração, classificação e geração de resposta
    prompt = f"""
    Você é um agente de automação de e-mails. Sua tarefa é analisar o texto fornecido e fazer três coisas:
    
    1.  **Classificar** o texto em: **Produtivo** (exige ação/resposta específica) ou **Improdutivo** (agradecimento, informativo).
    2.  **Extrair o Assunto** do e-mail.
    3.  **Gerar uma Resposta Automática** (auto_response) com base na classificação.
        - Se Produtivo: Confirme o recebimento e informe que a equipe responderá em até 48h úteis.
        - Se Improdutivo: Agradeça a mensagem e confirme que a informação foi registrada/recebida.

    **TEXTO PARA ANÁLISE:**
    ---
    {text_content}
    ---
    
    Responda apenas com um objeto JSON, seguindo este formato EXATO:
    {{"classification": "Produtivo" ou "Improdutivo", "email_subject": "O assunto extraído", "auto_response": "A resposta automática gerada"}}
    """

    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )
        
        json_data = json.loads(response.text)
        
        return json_data
        
    except Exception as e:
        print(f"Erro ao chamar a API do Gemini: {e}")
        return {
            "classification": "Erro de Classificação", 
            "email_subject": "Falha na extração",
            "auto_response": "Não foi possível gerar a resposta automática devido a um erro interno."
        }

# --- Criação do Endpoint da API ---

app = FastAPI(
    title="API de Classificação e Automação de E-mail por IA",
    description="Endpoint para classificar conteúdo de arquivos e gerar uma resposta automática."
)

@app.post("/classify_file")
async def classify_file(file: UploadFile = File(...)):
    """
    Recebe um arquivo (.txt ou .pdf), extrai o texto e retorna sua classificação, assunto e resposta automática.
    """
    
    file_content = extract_text_from_file(file)
    ia_result = classify_text_with_gemini(file_content)
    
    classification = ia_result.get("classification")
    email_subject = ia_result.get("email_subject")
    auto_response = ia_result.get("auto_response")

    if classification in ["Erro de Classificação", "Erro de Configuração (Chave API ausente)"]:
        status_code = 500
        detail = f"Falha na automação pela IA: {auto_response}"
        if classification == "Erro de Configuração (Chave API ausente)":
            detail = "Falha de configuração: A Chave de API do Gemini não foi carregada. Verifique seu arquivo .env."
        
        raise HTTPException(status_code=status_code, detail=detail)

    return {
        "status": "success",
        "filename": file.filename,
        "classification": classification,
        "email_subject": email_subject,
        "auto_response": auto_response
    }

# --- Bloco de Execução ---
# Útil para rodar com 'python main.py'
if __name__ == "__main__":
    import uvicorn
    # ESSENCIAL: main:app é a referência ao objeto FastAPI
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)