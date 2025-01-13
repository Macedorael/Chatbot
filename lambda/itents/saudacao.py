def saudacoes_intent(session_attributes, slots):
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
        "messages": [
            {"contentType": "PlainText", "content": "Seja bem-vindo(a) ao BotNutri!"},
            {"contentType": "PlainText", "content": "Estou aqui para te ajudar a não sair do foco."},
            {"contentType": "PlainText", "content": "Qual é a caloria da refeição?"}
        ]
    }