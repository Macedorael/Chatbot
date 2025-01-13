import boto3 
rekognition_client = boto3.client('rekognition')
from filtro import excluir_labels
from tradutor import traduzir_nome

def enviar_fotos_intent(session_attributes, slots, iten_aconfirmar,itens_proibidos):
    foto = slots.get('foto')
    if foto is None:
        return {
                "sessionState": {
                    "dialogAction": {
                        "type": "ElicitSlot",
                        "slotToElicit": "foto",
                        "intent": {"name": "EnviarFotos", "slots": slots}
                    },
                    "intent": {"name": "EnviarFotos", "state": "InProgress"},
                    "sessionAttributes": session_attributes,
                },
                "messages": [{"contentType": "PlainText", "content": "Legal! Agora, por favor, envie a foto."}]
            }
    else:
        foto_url = foto['value']['interpretedValue']
        response = rekognition_client.detect_labels(
            Image={'S3Object': {'Bucket': 'testefinal', 'Name': foto_url}},
            MaxLabels=10,
            MinConfidence=90
        )

        labels_filtradas = excluir_labels(response['Labels'])

        if labels_filtradas:
            primeira_label = labels_filtradas[0]
            nome_traduzido = traduzir_nome(primeira_label)  # Traduz o nome do item detectado

            # Verifica se o nome traduzido está na lista de itens proibidos
            if nome_traduzido.lower() in itens_proibidos:
                return {
                    "sessionState": {
                        "dialogAction": {
                            "type": "ElicitSlot",
                            "slotToElicit": "foto",
                            "intent": {"name": "EnviarFotos", "slots": slots}
                        },
                        "intent": {"name": "EnviarFotos", "state": "InProgress"},
                        "sessionAttributes": session_attributes,
                    },
                    "messages": [{"contentType": "PlainText", "content": f"A foto contém um item proibido ({nome_traduzido}). Por favor, envie uma nova foto."}]
                }

            # Se o item não for proibido, adiciona à lista de itens confirmados
            iten_aconfirmar.append(nome_traduzido)

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
                "messages": [{"contentType": "PlainText", "content": f"Encontrei(s) {nome_traduzido}. Está tudo certo? (Responda Sim ou Não)"}]   
            } 
        else:
            return {
                "sessionState": {
                    "dialogAction": {
                        "type": "ElicitSlot",
                        "slotToElicit": "foto",
                        "intent": {"name": "EnviarFotos", "slots": slots}
                    },
                    "intent": {"name": "EnviarFotos", "state": "InProgress"},
                    "sessionAttributes": session_attributes,
                },
                "messages": [{"contentType": "PlainText", "content": "Não consegui reconhecer nenhum item. Que tal tentar enviar outra foto?"}]
            }
