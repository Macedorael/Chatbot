from gpt import generate_recipe

def confimarcoesquantidade_intent(session_attributes, slots, itens_confirmados, iten_aconfirmar, resposta_positiva, resposta_negativa):
    quantidade = slots.get("quantidade")
        
    retry_count = int(session_attributes.get("retryCountQuantidade", 0))

    if quantidade is None:
        retry_count += 1 
        session_attributes["retryCountQuantidade"] = str(retry_count)

        if retry_count >= 3:
            session_attributes["retryCountQuantidade"] = "0" 

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
                    "slotToElicit": "quantidade",
                    "intent": {"name": "ConfimacoesQuantidade", "slots": slots}
                },
                "intent": {"name": "ConfimacoesQuantidade", "state": "InProgress"},
                "sessionAttributes": session_attributes,
            },
            "messages": [{"contentType": "PlainText", "content": "Gostaria de adicionar mais itens? Responda Sim ou Não."}]
        }

    elif quantidade['value']['interpretedValue'].lower() in resposta_positiva:
        session_attributes["retryCountQuantidade"] = "0" 
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
                    "content": "Você pode selecionar Áudio, Texto ou Foto para continuar."
                },
                {
                    "contentType": "ImageResponseCard",
                    "imageResponseCard": {
                        "title": "Escolha uma opção",
                        "subtitle": "Você pode selecionar Áudio, Texto ou Foto para continuar.",
                        "buttons": [
                            {"text": "Áudio", "value": "Audio"},
                            {"text": "Texto", "value": "Texto"},
                            {"text": "Foto", "value": "Foto"}
                        ]
                    }
                }
            ]
        }

    elif quantidade['value']['interpretedValue'].lower() in resposta_negativa:
        session_attributes["retryCountQuantidade"] = "0" 
        kcal = session_attributes.get('caloria', 'não especificada')
        receita = generate_recipe(itens_confirmados, kcal)
        itens_confirmadosfinal = ", ".join(itens_confirmados)

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
                {
                    "contentType": "PlainText",
                    "content": f"Fico feliz em ajudar! 😊\n\nAqui estão os ingredientes confirmados:\n{itens_confirmadosfinal}\n\nE agora, com todo carinho, aqui está a sua receita:\n{receita}"
                },
                {
                    "contentType": "PlainText",
                    "content": "Você gostaria de outra receita? (Sim ou Não)."
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

    else:
        retry_count += 1  
        session_attributes["retryCountQuantidade"] = str(retry_count)

        
        if retry_count >= 3:
            session_attributes["retryCountQuantidade"] = "0"  

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
                    "slotToElicit": "quantidade",
                    "intent": {"name": "ConfimacoesQuantidade", "slots": slots}
                },
                "intent": {"name": "ConfimacoesQuantidade", "state": "InProgress"},
                "sessionAttributes": session_attributes,
            },
            "messages": [
                {"contentType": "PlainText", "content": "Desculpe, não entendi sua resposta. Por favor, responda com Sim ou Não."}
            ]
        }