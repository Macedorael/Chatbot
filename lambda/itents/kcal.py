import re 

def kcal_intent(session_attributes, slots):
    caloria = slots.get('caloria')

    if caloria is None:
        retry_count += 1  
        session_attributes["retryCount"] = str(retry_count)
        
        if retry_count >= 3:
            session_attributes["retryCount"] = "0"  

            return {
                "sessionState": {
                    "dialogAction": {
                        "type": "ElicitIntent" 
                    },
                    "sessionAttributes": session_attributes,
                },
                "messages": [
                    {
                        "contentType": "PlainText",
                        "content": "Parece que você está com dificuldades para inserir a caloria. Vou redirecioná-lo para o início para tentarmos novamente."
                    }
                ]
            }

        return {
            "sessionState": {
                "dialogAction": {
                    "type": "ElicitSlot",
                    "slotToElicit": "caloria",
                    "intent": {"name": "Kcal", "slots": slots}
                },
                "intent": {"name": "Kcal", "state": "InProgress"},
                "sessionAttributes": session_attributes,
            },
            "messages": [{"contentType": "PlainText", "content": "Olá! Por favor, diga qual é a caloria da refeição?"}]
        }
    else:
        caloria = caloria['value']['interpretedValue']
        
        
        if not re.match(r"^\d{1,5}$", caloria):
            retry_count += 1  
            session_attributes["retryCount"] = str(retry_count)

            
            if retry_count >= 3:
                session_attributes["retryCount"] = "0"  

                return {
                    "sessionState": {
                        "dialogAction": {
                            "type": "ElicitIntent"  
                        },
                        "sessionAttributes": session_attributes,
                    },
                    "messages": [
                        {
                            "contentType": "PlainText",
                            "content": "Parece que você está com dificuldades para inserir um valor válido. Vou redirecioná-lo para o início."
                        }
                    ]
                }

            return {
                "sessionState": {
                    "dialogAction": {
                        "type": "ElicitSlot",
                        "slotToElicit": "caloria",
                        "intent": {"name": "Kcal", "slots": slots}
                    },
                    "intent": {"name": "Kcal", "state": "InProgress"},
                    "sessionAttributes": session_attributes,
                },
                "messages": [{"contentType": "PlainText", "content": f"Desculpe, O valor '{caloria}' não é válido. Por favor, informe apenas o número de calorias da refeição."}]
            }

        session_attributes['caloria'] = caloria
        session_attributes["retryCount"] = "0" 

        return {
            "sessionState": {
                "dialogAction": {
                    "type": "ElicitSlot",
                    "slotToElicit": "opcao",
                    "intent": {"name": "Opcoes", "slots": slots}
                },
                "intent": {"name": "Opcoes", "state": "InProgress"},
                "sessionAttributes": session_attributes,
            },
            "messages": [
                {
                    "contentType": "PlainText",
                    "content": "Qual a melhor forma de enviar os ingredientes? Escolha uma opção abaixo:"
                },
                {
                    "contentType": "ImageResponseCard",
                    "imageResponseCard": {
                        "title": "Como prefere enviar?",
                        "buttons": [
                            {"text": "Áudio", "value": "Audio"},
                            {"text": "Texto", "value": "Texto"},
                            {"text": "Foto", "value": "Foto"}
                        ]
                    }
                }
            ]
        }
