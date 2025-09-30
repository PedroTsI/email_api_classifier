from fastapi import FastAPI, UploadFile, HTTPException, File
from file_processor import extract_text_from_file
from ai_service import classify_text_with_gemini

# Criação do Endpoint da API
app = FastAPI(
    title="API de Classificação e Automação de E-mail por IA",
    description="Endpoint para classificar conteúdo de arquivos e gerar uma resposta automática."
)

@app.post("/classify_file")
async def classify_file(file: UploadFile = File(...)):
    """
    Recebe um arquivo (.txt ou .pdf), extrai o texto e retorna sua classificação, assunto e resposta automática.
    """
    
    # 1. Extração de Conteúdo (SRP: file_processor)
    file_content = extract_text_from_file(file)
    
    # 2. Processamento e Geração (SRP: ai_service)
    ia_result = classify_text_with_gemini(file_content)
    
    classification = ia_result.get("classification")
    email_subject = ia_result.get("email_subject")
    auto_response = ia_result.get("auto_response")

    # Tratamento de Erro
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
