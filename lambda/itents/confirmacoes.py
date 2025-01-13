def confirmacoes_intent(session_attributes, slots, itens_confirmados, iten_aconfirmar, resposta_positiva, resposta_negativa):
    confirmacao = slots.get("confirmacao")
        
    retry_count = int(session_attributes.get("retryCountConfirmacoes", 0))

    if confirmacao is None:
        retry_count += 1 
        session_attributes["retryCountConfirmacoes"] = str(retry_count)

        if retry_count >= 3:
            session_attributes["retryCountConfirmacoes"] = "0"  

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
                        "content": "Parece que você está com dificuldades para responder. Vou redirecioná-lo para o início para tentarmos novamente."
                    }
                ]
            }

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
            "messages": [{"contentType": "PlainText", "content": "Você confirma o item detectado? Responda Sim ou Não."}]
        }

    elif confirmacao['value']['interpretedValue'].lower() in resposta_positiva:
        session_attributes["retryCountConfirmacoes"] = "0"  
        itens_confirmados.extend(iten_aconfirmar)
        iten_aconfirmar.clear()
        
        return {
            "sessionState": {
                "dialogAction": {
                    "type": "ElicitSlot",
                    "slotToElicit": "quantidade",
                    "intent": {"name": "ConfimacoesQuantidade", "slots": slots}
                },
                "intent": {"name": "ConfimacoesQuantidade", "state": "InProgress"},
                "sessionAttributes": session_attributes,
            },
            "messages": [
                {
                    "contentType": "PlainText",
                    "content": "Quer adicionar mais algum item? 😊 Responda Sim ou Não."
                },
                {
                    "contentType": "ImageResponseCard",
                    "imageResponseCard": {
                        "title": "Escolha uma opção",
                        "buttons": [
                            {"text": "Sim", "value": "sim"},
                            {"text": "Não", "value": "nao"}
                        ]
                    }
                }
            ]
        }

    elif confirmacao['value']['interpretedValue'].lower() in resposta_negativa:
        session_attributes["retryCountConfirmacoes"] = "0"  
        iten_aconfirmar.clear()
        
        return {
            "sessionState": {
                "dialogAction": {
                    "type": "ElicitSlot",
                    "slotToElicit": "novonome",
                    "intent": {"name": "NovosNomes", "slots": slots}
                },
                "intent": {"name": "NovosNomes", "state": "InProgress"},
                "sessionAttributes": session_attributes,
            },
            "messages": [{"contentType": "PlainText", "content": "Você pode me dizer o nome correto do alimento?"}]
        }

    else:
        retry_count += 1  
        session_attributes["retryCountConfirmacoes"] = str(retry_count)

        
        if retry_count >= 3:
            
            session_attributes["retryCountConfirmacoes"] = "0"  

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
                        "content": "Parece que você está com dificuldades para responder. Vou redirecioná-lo para o início."
                    }
                ]
            }

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
            "messages": [
                {"contentType": "PlainText", "content": "Ops, não entendi sua resposta. Pode me responder com Sim ou Não, por favor?"}
            ]
        }
