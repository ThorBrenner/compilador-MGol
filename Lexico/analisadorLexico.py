from Lexico.tabelaTransicao import *
from Lexico.tabelaSimbolos import *

dadosErro = {"linha" : 1, "colAtual": 0, "colAntiga": 0 }


def verifica_tabela_dfa(caractere, estado_atual, TabelaTransicao):
    prox_estado = TabelaTransicao[estado_atual].get(caractere)
    if prox_estado != None:
        return prox_estado
    else:
        return -1

def verifica_token_dfa(estado):
    if estado == 1 or estado == 3 or estado == 6:
        token = "Num"
    if estado == 8:
        token = "Lit"
    if estado == 9:
        token = "id"
    if estado == 11:
        token = "Comentário"
    if estado == 12:
        token = "OPM"
    if estado == 13 or estado == 15 or estado == 16 or estado == 17 or estado == 18:
        token = "OPR"
    if estado == 14:
        token = "ATR"
    if estado == 19:
        token = "AB_P"
    if estado == 20:
        token = "FC_P"
    if estado == 21:
        token = "PT_V"
    if estado == 22:
        token = "VIR"
    return token


def analisadorLexico(arquivo, TabelaTransicao, TabelaSimbolos):
    distanciaUltimoAceito = 1

    tupla = {"lexema": "", "token": "", "tipo": "null", "linha": "","coluna": ""}

    char = arquivo.read(1)
    dadosErro['colAtual'] += 1
    palavra = ""
    estado = 0

    if not char:           
        return {"lexema": "EOF", "token": "$", "tipo": "null", "linha": str(dadosErro["linha"]),"coluna": str(dadosErro["colAtual"])}

    while True:

        if char == '\n':
            dadosErro["linha"] += 1
            dadosErro["colAntiga"] = dadosErro["colAtual"] 
            dadosErro["colAtual"] = 0

        estado_aux = verifica_tabela_dfa(char, estado, TabelaTransicao)
        estado_anterior = estado
        estado = estado_aux

        if estado == -1:  
            
            if not char:
                if tupla['token'] == '' and tupla['lexema'] != '':

                    tipoErro = "Caractere invalido"
                    print("Erro léxico. "+ tipoErro + ": "+ palavra + " - Linha " + str(dadosErro["linha"]) + ", Coluna " + str(dadosErro["colAtual"]))
                    tupla = {"lexema": "null", "token": "ERRO", "tipo": "null", "linha": str(dadosErro["linha"]), "coluna": str(dadosErro["colAtual"])}
                elif tupla["token"] == "id":
                    tupla = procuraToken(tupla, TabelaSimbolos)
                    tupla.update({"linha": str(dadosErro["linha"]), "coluna": str(dadosErro["colAtual"])})
                else:
                    tupla = {"lexema": "EOF", "token": "$", "tipo": "null", "linha": str(dadosErro["linha"]),"coluna": str(dadosErro["colAtual"])}
                return tupla

            if tupla['lexema'] == '':

                tipoErro = "Caractere invalido"
                print("Erro léxico. " + tipoErro + ": " + char + " - Linha " + str(dadosErro["linha"]) + ", Coluna " + str(dadosErro["colAtual"]))
                tupla = {"lexema": "null", "token": "ERRO", "tipo": "null", "linha": str(dadosErro["linha"]),"coluna": str(dadosErro["colAtual"])}
                return tupla
            
            if tupla["token"] == "Num" and (estado_anterior == 2 or estado_anterior == 4 or estado_anterior == 5):
                print("Erro léxico. " + 'caractere inválido' + ": " + char + " - Linha " + str(dadosErro["linha"]) + ", Coluna " + str(dadosErro["colAtual"]))
                tupla = {"lexema": "null", "token": "ERRO", "tipo": "null", "linha": str(dadosErro["linha"]),"coluna": str(dadosErro["colAtual"])}
                return tupla
            
            arquivo.seek(arquivo.tell() - distanciaUltimoAceito)

            if char == '\n':
                dadosErro["linha"] -= 1
                dadosErro["colAtual"] = dadosErro["colAntiga"] - distanciaUltimoAceito
            else :
                dadosErro["colAtual"] = dadosErro["colAtual"] - distanciaUltimoAceito

            if tupla["token"] == "id":
                tupla = procuraToken(tupla, TabelaSimbolos)
                tupla.update({"linha": str(dadosErro["linha"]),"coluna": str(dadosErro["colAtual"])})
            
            return tupla

        elif TabelaTransicao[estado].get("final"):
            palavra = palavra + char
            distanciaUltimoAceito = 1
            token = verifica_token_dfa(estado)

            if(estado == 1):
                tupla = {"lexema": palavra, "token": token, "tipo": "int", "linha": str(dadosErro["linha"]),"coluna": str(dadosErro["colAtual"])}
            elif(estado == 3 or estado == 6):
                tupla = {"lexema": palavra, "token": token, "tipo": "real", "linha": str(dadosErro["linha"]),"coluna": str(dadosErro["colAtual"])}
            else:
                tupla = {"lexema": palavra, "token": token, "tipo": "null", "linha": str(dadosErro["linha"]),"coluna": str(dadosErro["colAtual"])}

        else:
            if (estado == 0 and char != " " and char != "\n" and char != "\t") or estado != 0:
                palavra = palavra + char
                distanciaUltimoAceito += 1

        char = arquivo.read(1)
        dadosErro['colAtual'] += 1

