def opcoes_intent(session_attributes, slots):
    opcao = slots.get('opcao')

    retry_count = int(session_attributes.get("retryCountOpcoes", 0))

    if opcao is None:
        retry_count += 1  
        session_attributes["retryCountOpcoes"] = str(retry_count)

        
        if retry_count >= 3:
            
            session_attributes["retryCountOpcoes"] = "0"  

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
                        "content": "Parece que você está com dificuldades para escolher uma opção. Vou redirecioná-lo para o início para tentarmos novamente."
                    }
                ]
            }

        return {
            "sessionState": {
                "dialogAction": {
                    "type": "ElicitSlot",
                    "slotToElicit": "opcao"
                },
                "intent": {"name": "Opcoes", "state": "InProgress"},
                "sessionAttributes": session_attributes,
            },
            "messages": [
                {
                    "contentType": "PlainText",
                    "content": "Para continuar, escolha uma opção digitando: Áudio, Texto ou Foto."
                }
            ]
        }

    else:
        opcao_valor = opcao['value']['interpretedValue'].lower()

        if opcao_valor not in ["audio", "texto", "foto"]:
            retry_count += 1  
            session_attributes["retryCountOpcoes"] = str(retry_count)

            if retry_count >= 3:

                session_attributes["retryCountOpcoes"] = "0"  

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
                            "content": "Parece que você está com dificuldades para escolher uma opção válida. Vou redirecioná-lo para o início."
                        }
                    ]
                }

            
            return {
                "sessionState": {
                    "dialogAction": {
                        "type": "ElicitSlot",
                        "slotToElicit": "opcao"
                    },
                    "intent": {"name": "Opcoes", "state": "InProgress"},
                    "sessionAttributes": session_attributes,
                },
                "messages": [
                    {
                        "contentType": "PlainText",
                        "content": "Desculpe, não entendi. Por favor, escolha entre Áudio, Texto ou Foto."
                    }
                ]
            }

        session_attributes["retryCountOpcoes"] = "0" 

        if opcao_valor == "audio":
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
                "messages": [
                    {
                        "contentType": "PlainText",
                        "content": "Ótimo! Agora, por favor, envie o áudio."
                    }
                ]
            }

        elif opcao_valor == "texto":
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
                "messages": [
                    {
                        "contentType": "PlainText",
                        "content": "Perfeito! Agora, por favor, escreva os ingredientes."
                    }
                ]
            }

        elif opcao_valor == "foto":
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
                "messages": [
                    {
                        "contentType": "PlainText",
                        "content": "Legal! Agora, por favor, envie a foto."
                    }
                ]
            }
