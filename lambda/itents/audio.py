
import re

def audio_intent(session_attributes, slots, iten_aconfirmar,itens_proibidos):
    audio = slots.get('audio')

    if audio is None:
        return {
            "sessionState": {
                "dialogAction": {
                    "type": "ElicitSlot",
                    "slotToElicit": "audio",
                    "intent": {"name": "EnviarAudio", "slots": slots}
                },
                "intent": {"name": "EnviarAudio", "state": "InProgress"},
                "sessionAttributes": session_attributes,
            },
            "messages": [{"contentType": "PlainText", "content": "Por favor, envie o áudio."}]
        }
    else:
        audio = audio['value']['interpretedValue']
        conversao = audio
        
        # Extrai e filtra as palavras não vazias
        itens = [palavra for palavra in re.split(r"[,\s\.]+", conversao) if palavra]
        print(f'lista {itens}')
        
        # Verifica se algum dos itens transcritos está na lista de proibidos
        itens_proibidos_encontrados = [item for item in itens if item.lower() in itens_proibidos]
        iten_aconfirmar_tratado = ", ".join(iten_aconfirmar)
        if itens_proibidos_encontrados:
            itens_proibidos_texto = ", ".join(itens_proibidos_encontrados)
            return {
                "sessionState": {
                    "dialogAction": {
                        "type": "ElicitSlot",
                        "slotToElicit": "audio",
                        "intent": {"name": "EnviarAudio", "slots": slots}
                    },
                    "intent": {"name": "EnviarAudio", "state": "InProgress"},
                    "sessionAttributes": session_attributes,
                },
                "messages": [{"contentType": "PlainText", "content": f"Os itens '{itens_proibidos_texto}' não são permitidos. Por favor, envie outro áudio sem esses itens."}]
            }
    
    # Se nenhum item proibido foi encontrado, continua com a confirmação
    iten_aconfirmar.extend(itens)
    iten_aconfirmar_tratado = ", ".join(iten_aconfirmar)
    return {
        "sessionState": {
            "dialogAction": {
                "type": "ElicitSlot",
                "slotToElicit": "confirmacao",
                "intent": {"name": "Confirmacoes", "slots": slots}
            },
            "intent": {"name": "Confirmacoes", "state": "InProgress"},
            "sessionAttributes": session_attributes,
        },
        "messages": [{"contentType": "PlainText", "content": f"Encontrei {iten_aconfirmar_tratado}. Isso está correto? (Sim ou Não)"}]
    }

