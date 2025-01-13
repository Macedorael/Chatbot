import requests
import os


api_key = os.getenv("KEYCHAT")

# URL da API da OpenAI
url = "https://api.openai.com/v1/chat/completions"

def generate_recipe(itens_confirmados,kcal):
    # Criar o prompt explicando que o modelo é uma nutricionista
    prompt = f"""
        Você é uma nutricionista e precisa criar uma receita de baixa caloria utilizando o alimento: {itens_confirmados}, 
        Não posso ter uma refeição maior de {kcal}kcal, 
        estou de dieta e tenho que manter o foco. 
        Inclua a descrição dos ingredientes com suas quantidades de forma natural, mencionando tanto o peso em gramas 
        quanto as medidas caseiras, como colheres, xícaras, etc., para facilitar o preparo. 
        Garanta que não haja repetição de ingredientes e, no final, forneça o valor total de calorias do prato.
        Quero que a resposta fique no formato de lista.
        Não podendo passar de 300 tokens 
        Quero que faça uma receita somente com os ingredientes passado {itens_confirmados}
        MUITO IMPORTANTE QUE NAO PASSE DAS CALORIAS {kcal}
    """
    
    # Dados que serão enviados para a API
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    # Corpo da requisição para o modelo GPT-4
    data = {
        "model": "gpt-4",  # Utilizando o modelo GPT-4
        "messages": [
            {"role": "system", "content": "Você é uma nutricionista experiente."},  # Definindo o papel do assistente
            {"role": "user", "content": prompt}  # Passando o prompt do usuário
        ],
        "max_tokens": 300,  # Limite de tokens para controlar o tamanho da resposta
        "temperature": 0.7  # Temperatura para controlar a criatividade da resposta
    }

    # Fazendo a requisição POST para a API da OpenAI
    response = requests.post(url, headers=headers, json=data)

    # Verificando se a requisição foi bem-sucedida
    if response.status_code == 200:
        result = response.json()
        return result['choices'][0]['message']['content'].strip()
    else:
        return f"Erro na requisição: {response.status_code}, {response.text}"