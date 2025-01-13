import boto3

# Inicializa o cliente de tradução
translate = boto3.client('translate', region_name='us-east-1')

def traduzir_nome(nome, source_language='en', target_language='pt'):
    """Traduz o nome do item de inglês para português."""
    try:
        response = translate.translate_text(
            Text=nome,
            SourceLanguageCode=source_language,
            TargetLanguageCode=target_language
        )
        return response['TranslatedText']
    except Exception as e:
        print(f"Erro ao traduzir: {e}")
        return nome
