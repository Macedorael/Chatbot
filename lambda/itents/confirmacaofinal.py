from gpt import generate_recipe
def confirmacaofinal_intent(session_attributes, slots, itens_confirmados, resposta_positiva, resposta_negativa):

    retry_count = int(session_attributes.get("retryCountFinal", 0))
    final = slots.get("final")

    if final is None:
        retry_count += 1  
        session_attributes["retryCountFinal"] = str(retry_count)

        if retry_count >= 3:
            session_attributes["retryCountFinal"] = "0"
            return {
                "sessionState": {
                    "dialogAction": {
                        "type": "Close",
                        "fulfillmentState": "Fulfilled"
                    },
                    "sessionAttributes": session_attributes,
                },
                "messages": [
                    {"contentType": "PlainText", "content": "Parece que você está com dificuldades para responder. Finalizando o atendimento. Caso precise, estarei disponível!"}
                ]
            }

        return {
            "sessionState": {
                "dialogAction": {
                    "type": "ElicitSlot",
                    "slotToElicit": "final",
                    "intent": {"name": "ConfirmacaoFinal", "slots": slots}
                },
                "intent": {"name": "ConfirmacaoFinal", "state": "InProgress"},
                "sessionAttributes": session_attributes,
            },
            "messages": [{"contentType": "PlainText", "content": "Você confirma o item detectado? (Sim ou Não)"}]
        }

    elif final['value']['interpretedValue'].lower() in resposta_positiva:
        session_attributes["retryCountFinal"] = "0"  
        kcal = session_attributes['caloria']
        receita = generate_recipe(itens_confirmados, kcal)
        itens_confirmadosfinal = ", ".join(itens_confirmados)

        count_confirmados = session_attributes.get('count_confirmados', 0) + 1
        session_attributes['count_confirmados'] = count_confirmados

        return {
            "sessionState": {
                "dialogAction": {
                    "type": "ElicitSlot",
                    "slotToElicit": "final",
                    "intent": {"name": "ConfirmacaoFinal", "slots": slots}
                },
                "intent": {"name": "ConfirmacaoFinal", "state": "InProgress"},
                "sessionAttributes": session_attributes,
            },
            "messages": [
                {"contentType": "PlainText", "content": f"Fico feliz em ajudar! 😊 Aqui estão os itens confirmados: {itens_confirmadosfinal}. E, com carinho, sua receita: {receita}."},
                {"contentType": "PlainText", "content": f"Total de itens confirmados: {count_confirmados}."},
                {
                    "contentType": "PlainText",
                    "content": f"Você gostaria de outra receita? (Sim ou Não)."
                },
                {
                    "contentType": "ImageResponseCard",
                    "imageResponseCard": {
                        "title": "Escolha uma opção",
                        "buttons": [
                            {"text": "Sim", "value": "sim"},
                            {"text": "Não", "value": "nao"},
                        ]
                    }
                }
            ]
        }

    elif final['value']['interpretedValue'].lower() in resposta_negativa:
        session_attributes["retryCountFinal"] = "0"  
        return {
            "sessionState": {
                "dialogAction": {
                    "type": "Close",
                    "fulfillmentState": "Fulfilled"
                },
                "intent": {"name": "ConfirmacaoFinal", "state": "Fulfilled"},
                "sessionAttributes": session_attributes,
            },
            "messages": [{"contentType": "PlainText", "content": "Obrigado por usar nosso serviço para ajudar na sua refeição! 😊 Se precisar de algo mais, estou à disposição!"}]
        }

    else:
        retry_count += 1  
        session_attributes["retryCountFinal"] = str(retry_count)

        if retry_count >= 3:
            session_attributes["retryCountFinal"] = "0"
            return {
                "sessionState": {
                    "dialogAction": {
                        "type": "Close",
                        "fulfillmentState": "Fulfilled"
                    },
                    "sessionAttributes": session_attributes,
                },
                "messages": [
                    {"contentType": "PlainText", "content": "Parece que você está com dificuldades para responder. Finalizando o atendimento. Caso precise, estarei disponível!"}
                ]
            }

        return {
            "sessionState": {
                "dialogAction": {
                    "type": "ElicitSlot",
                    "slotToElicit": "final",
                    "intent": {"name": "ConfirmacaoFinal", "slots": slots}
                },
                "intent": {"name": "ConfirmacaoFinal", "state": "InProgress"},
                "sessionAttributes": session_attributes,
            },
            "messages": [
                {"contentType": "PlainText", "content": "Desculpe, não entendi sua resposta. Por favor, responda com Sim ou Não."}
            ]
        }