import re

def texto_intent(session_attributes, slots, iten_aconfirmar,itens_proibidos):
    if itens is None:
            return {
                "sessionState": {
                    "dialogAction": {
                        "type": "ElicitSlot",
                        "slotToElicit": "itens",
                        "intent": {"name": "Texto", "slots": slots}
                    },
                    "intent": {"name": "Texto", "state": "InProgress"},
                    "sessionAttributes": session_attributes,
                },
                "messages": [{"contentType": "PlainText", "content": "Perfeito! Agora, por favor, escreva os itens."}]
            }
    else:
        itens = itens['value']['interpretedValue']
        itens = [item for item in re.split(r"[,\s\.]+", itens) if item]
        
        # Verifica se algum item é proibido
        itens_validos = [item for item in itens if item.lower() not in itens_proibidos]
        itens_proibidos_detectados = [item for item in itens if item.lower() in itens_proibidos]
        
        if itens_proibidos_detectados:
            itens_proibidos_tratados = ", ".join(itens_proibidos_detectados)
            return {
                "sessionState": {
                    "dialogAction": {
                        "type": "ElicitSlot",
                        "slotToElicit": "itens",
                        "intent": {"name": "Texto", "slots": slots}
                    },
                    "intent": {"name": "Texto", "state": "InProgress"},
                    "sessionAttributes": session_attributes,
                },
                "messages": [{"contentType": "PlainText", "content": f"Os itens {itens_proibidos_tratados} são proibidos. Por favor, adicione outros itens."}]
            }
        
        iten_aconfirmar.extend(itens_validos)
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
            "messages": [{"contentType": "PlainText", "content": f"Encontrei ({iten_aconfirmar_tratado}). Isso está correto?(Sim ou Não)"}]
        }
