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
    Você é um agente de automação de e-mails altamente preciso. Sua tarefa é analisar o texto fornecido e retornar um objeto JSON com três chaves: "classification", "email_subject" e "auto_response".

    Siga estas regras estritamente:

    1.  **Análise do Texto:** Primeiro, determine se o texto parece ser um e-mail. Textos muito curtos, sem contexto, saudações ou um corpo de mensagem claro, não devem ser considerados e-mails.

    2.  **Classificação:**
        - Se o texto for um e-mail que exige uma ação ou resposta específica, classifique como **"Produtivo"**.
        - Se o texto for um e-mail meramente informativo, um agradecimento ou um aviso, classifique como **"Improdutivo"**.
        - Se o texto não parecer um e-mail (conforme a regra 1), classifique como **"Não é um e-mail"**.

    3.  **Extração do Assunto:**
        - Se for "Produtivo" ou "Improdutivo", extraia o assunto principal do texto.
        - Se for "Não é um e-mail", use o valor "Texto não corresponde a um e-mail".

    4.  **Geração de Resposta Automática:**
        - Para "Produtivo": "Recebemos sua mensagem e agradecemos o contato. Nossa equipe analisará sua solicitação e retornará em até 48 horas úteis."
        - Para "Improdutivo": "Agradecemos sua mensagem. A informação foi devidamente recebida e registrada."
        - Para "Não é um e-mail": "O conteúdo fornecido não foi identificado como um e-mail e não será processado."

    **TEXTO PARA ANÁLISE:**
    ---
    {text_content}
    ---
    
    **Formato da Saída:** Responda apenas e exclusivamente com um único objeto JSON válido, seguindo este formato. Não inclua texto ou explicações antes ou depois do JSON.
    {{"classification": "...", "email_subject": "...", "auto_response": "..."}}
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
