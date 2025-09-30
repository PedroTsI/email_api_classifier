import json
from google.genai import types
from config import client, GEMINI_API_KEY # Importa o cliente e a chave do config

def classify_text_with_gemini(text_content: str) -> dict:
    """Usa o modelo Gemini para classificar, extrair o assunto e gerar uma resposta."""
    if not GEMINI_API_KEY or client is None:
        return {
            "classification": "Erro de Configuração (Chave API ausente)", 
            "email_subject": "N/A",
            "auto_response": "Erro de configuração da API."
        }
        
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
    
    Responda apenas com um objeto JSON, seguindo este formato EXATO, caso o texto seja muito pequeno e não tenha conteudo, informe que o texto não se trata de um Email:
    {{"classification": "Produtivo" ou "Improdutivo", "email_subject": "O assunto extraído", "auto_response": "A resposta automática gerada"}}
    """

    try:
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )
        print("prompt efetuado com sucesso")
        
        json_data = json.loads(response.text)
        
        return json_data
        
    except Exception as e:
        print(f"Erro ao chamar a API do Gemini: {e}")
        return {
            "classification": "Erro de Classificação", 
            "email_subject": "Falha na extração",
            "auto_response": "Não foi possível gerar a resposta automática devido a um erro interno."
        }
