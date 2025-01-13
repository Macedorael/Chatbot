def novosnomes_intent(session_attributes, slots,itens_proibidos,itens_confirmados,iten_aconfirmar):
    novonome = slots.get('novonome')

    if novonome:
        nome_item = novonome['value']['interpretedValue']
        
        if nome_item.lower() in itens_proibidos:
            return {
                "sessionState": {
                    "dialogAction": {
                        "type": "ElicitSlot",
                        "slotToElicit": "novonome",
                        "intent": {"name": "NovosNomes", "slots": slots}
                    },
                    "intent": {"name": "NovosNomes", "state": "InProgress"},
                },
                "messages": [{"contentType": "PlainText", "content": f"O item '{nome_item}' não é permitido. Por favor, escolha outro nome para adicionar."}]
            }

        itens_confirmados.append(nome_item)

        return {
            "sessionState": {
                "dialogAction": {
                    "type": "ElicitSlot",
                    "slotToElicit": "quantidade",
                    "intent": {"name": "ConfimacoesQuantidade", "slots": slots}
                },
                "intent": {"name": "ConfimacoesQuantidade", "state": "InProgress"},
            },
            "messages": [{"contentType": "PlainText", "content": "Gostaria de adicionar mais algum ingrediente? (Sim ou Não)"}]
        }

