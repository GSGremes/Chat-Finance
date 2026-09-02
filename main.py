import os
import datetime

mensagens = []
transacoes = []
proximo_id = 1

nome = input("Nome: ")
while True:
    try:
        mes_atual = int(input("Digite o mês: "))
        ano_atual = int(input("Digite o ano: "))
        if 1 <= mes_atual <= 12:
            break
        print("Digite um mês válido!")
        continue
    except ValueError:
        print("Digite apenas números!")

def atribuirReceita(valor, local):
    global proximo_id
    transacoes.append({
        "id": proximo_id,
        "tipo": "receita",
        "valor": valor,
        "local": local,
        "data": datetime.datetime(ano_atual, mes_atual, 1)
    })
    proximo_id = proximo_id+1

def atribuirDespesa(valor, local):
    global proximo_id
    transacoes.append({
        "id": proximo_id,
        "tipo": "despesa",
        "valor": valor,
        "local": local,
        "data": datetime.datetime(ano_atual, mes_atual, 1)
    })
    proximo_id = proximo_id+1

def calcularSaldo(mes, ano):
    totalReceita = 0
    totalDespesa = 0
    
    for transacao in transacoes:
        if transacao["tipo"] == "receita" and transacao["data"].month == mes and transacao["data"].year == ano:
            totalReceita += transacao["valor"]

        elif transacao["tipo"] == "despesa" and transacao["data"].month == mes and transacao["data"].year == ano:
            totalDespesa += transacao["valor"]
        
    saldo = totalReceita - totalDespesa
    return saldo, totalDespesa, totalReceita

def gerarDetalhes(mes, ano):

    detalhes_receita = ""
    detalhes_despesa = ""

    for transacao in transacoes:
        if transacao["tipo"] == "receita" and transacao["data"].month == mes and transacao["data"].year == ano:
            detalhes_receita += f'{transacao["id"]} - {transacao["local"]} - R$ {transacao["valor"]:.2f}\n'

        elif transacao["tipo"] == "despesa" and transacao["data"].month == mes and transacao["data"].year == ano:
            detalhes_despesa += f'{transacao["id"]} - {transacao["local"]} - R$ {transacao["valor"]:.2f}\n'

    return detalhes_receita, detalhes_despesa

def calcularPorcentagens(mes, ano):
    gastos_por_local = {}
    detalhes_porcentagem = ""

    for transacao in transacoes:
        if transacao["tipo"] == "despesa" and transacao["data"].month == mes and transacao["data"].year == ano:
            if transacao["local"] in gastos_por_local:
                gastos_por_local[transacao["local"]] = gastos_por_local[transacao["local"]] + transacao["valor"]
            else:
                gastos_por_local[transacao["local"]] = transacao["valor"]

    totalDespesa = 0
    for local in gastos_por_local:
        valor = gastos_por_local[local]
        totalDespesa += valor

    for local in gastos_por_local:
        valor = gastos_por_local[local]
        porcentagens = (valor / totalDespesa) * 100
        detalhes_porcentagem += f'{local} - R$ {valor:.2f} - {porcentagens:.2f}%\n'
    return detalhes_porcentagem
        

def pedirValor():
    while True:
        try: # Condição para não aceitar letras ou algo diferente de números.
            valor = float(input("Digite a movimentação desse mês: "))
            if valor <= 0: # Condição para aceitar apenas número positivo.
                print("Digite apenas números positivos e maiores que zero!")
                continue
            break
        except ValueError:
            print("Digite apenas números!")
    return valor

while True:

    os.system("cls") #limpar o terminal sempre que rodar o programa.
    bot = "@Bot"
    msg_bot = f"""
Olá, {nome}! Vamos controlar suas finanças?
    
Período atual: {mes_atual}/{ano_atual}

1 - Adicionar receita
2 - Adicionar despesa
3 - Relatório
4 - Alterar período
5 - Excluir transação
"""
    mensagens.append({
        "nome": bot,
        "texto": msg_bot
    })
    
    if len(mensagens) > 0:
        for m in mensagens:
            print(m['nome'], "-", m['texto'])

    print('________________')
    
    texto = input("mensagem: ").lower().strip()
    if texto == ("fim"):
        break

        # Salvando a mensagem e o nome no array.
    mensagens.append({
        "nome": nome,
        "texto": texto 
    })

    match texto:
        case "1":
            valor = pedirValor()
            local = (input("De onde veio essa receita: "))
            atribuirReceita(valor, local)

            msg_bot = f"Receita de R${valor:.2f} adicionado!"

            mensagens.append({
                "nome": bot,
                "texto": msg_bot
            })
        case "2":
            valor = pedirValor()
            local = (input("de onde veio essa despesa: "))
            atribuirDespesa(valor, local)
            
            msg_bot = f"Despesa de R${valor:.2f} adicionada!"
            mensagens.append({
                "nome": bot,
                "texto": msg_bot
            })
        case "3":
            mes = mes_atual
            ano = ano_atual

            saldo, totalDespesa, totalReceita = calcularSaldo(mes, ano)
            detalhes_receita, detalhes_despesa = gerarDetalhes(mes, ano)
            detalhes_porcentagem = calcularPorcentagens(mes, ano)

            msg_bot = f'''
===== RELATÓRIO DE {mes} / {ano} =====

Receita Total = R$ {totalReceita:.2f}
Receitas:
{detalhes_receita}

Despesas Total = R$ {totalDespesa:.2f}
Gastos:
{detalhes_despesa}

Saldo Final = R$ {saldo:.2f}

===============================
Porcentagem de gastos:
{detalhes_porcentagem}
'''
            mensagens.append({
                "nome": bot,
                "texto": msg_bot
            })
        case "4":
            while True:
                try:
                    mes_atual = int(input("Digite o mês: "))
                    ano_atual = int(input("Digite o ano: "))
                    if 1 <= mes_atual <= 12:
                        break
                    print("Digite um mês válido!")
                    continue
                except ValueError:
                    print("Digite apenas números!")
        case "5":
            try:
                id_excluir = int(input("Digite o número da transação que deseja excluir: "))

                for transacao in transacoes:
                    if transacao["id"] == id_excluir and transacao["data"].month == mes_atual and transacao["data"].year == ano_atual:
                        transacoes.remove(transacao)

                        msg_bot = f"Transação {id_excluir} excluída com sucesso!"
                        mensagens.append({
                            "nome": bot,
                            "texto": msg_bot
                        })
                        break
                else:
                    msg_bot = "Transação não encontrada nesse período!"
                    mensagens.append({
                        "nome": bot,
                        "texto": msg_bot
                    })

            except ValueError:
                msg_bot = "Digite apenas números!"
                mensagens.append({
                    "nome": bot,
                    "texto": msg_bot
                })

        case _:
            msg_bot = "não entendi o que você digitou"
            mensagens.append({
                "nome": bot,
                "texto": msg_bot
            })