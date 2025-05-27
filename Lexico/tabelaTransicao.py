import string

estadoInicial = 0
estadoNum = 1
estadoNumPonto = 2
estadoNumPontoFinal = 3
estadoNumExpoente1 = 4
estadoNumExpoente2 = 5
estadoNumExpoenteFinal = 6
estadoLiteral = 7
estadoLiteralFinal = 8
estadoId = 9
estadoComentario = 10
estadoComentarioFinal = 11
estadoOPM = 12
estadoOPRMenor = 13
estadoRCB = 14
estadoOPRMenorIgualDiferente = 15
estadoOPRMaior = 16
estadoOPRMaiorIgual = 17
estadoOPRIgual = 18
estadoABP = 19
estadoFCP = 20
estadoPTV = 21
estadoVIR = 22

def preenche_tabela_dfa(Tabela_Transicao):

    linha = {}
    linha.update({"final": False})
    for c in string.ascii_letters:
        linha.update({c:estadoId})
    for c in range(0,10):
        linha.update({str(c):estadoNum})
    linha.update({"\n":estadoInicial, " ": estadoInicial, "\t": estadoInicial})
    linha.update({"\"": estadoLiteral})
    linha.update({"{":estadoComentario})
    linha.update({"<":estadoOPRMenor , ">":estadoOPRMaior , "=":estadoOPRIgual})
    linha.update({"+": estadoOPM, "-": estadoOPM, "*": estadoOPM, "/": estadoOPM})
    linha.update({"(": estadoABP, ")": estadoFCP, ";": estadoPTV, ",": estadoVIR})
    Tabela_Transicao.append(linha)

    linha = {}
    linha.update({"final": True})
    for c in range(0, 10):
        linha.update({str(c): estadoNum})
    linha.update({".": estadoNumPonto, "E": estadoNumExpoente1, "e": estadoNumExpoente1})
    Tabela_Transicao.append(linha)

    linha = {}
    linha.update({"final": False})
    for c in range(0, 10):
        linha.update({str(c): estadoNumPontoFinal})
    Tabela_Transicao.append(linha)

    linha = {}
    linha.update({"final": True})
    for c in range(0, 10):
        linha.update({str(c): estadoNumPontoFinal})
    linha.update({"E": estadoNumExpoente1, "e": estadoNumExpoente1})
    Tabela_Transicao.append(linha)

    linha = {}
    linha.update({"final": False})
    for c in range(0, 10):
        linha.update({str(c): estadoNumExpoenteFinal})
    linha.update({"+": estadoNumExpoente2, "-": estadoNumExpoente2})
    Tabela_Transicao.append(linha)

    linha = {}
    linha.update({"final": False})
    for c in range(0, 10):
        linha.update({str(c): estadoNumExpoenteFinal})
    Tabela_Transicao.append(linha)

    linha = {}
    linha.update({"final": True})
    for c in range(0, 10):
        linha.update({str(c): estadoNumExpoenteFinal})
    Tabela_Transicao.append(linha)

    linha = {}
    linha.update({"final": False})
    for c in string.printable:
        if c != "\"":
            linha.update({c:estadoLiteral})
    linha.update({"\"": estadoLiteralFinal})
    Tabela_Transicao.append(linha)

    linha = {}
    linha.update({"final": True})
    Tabela_Transicao.append(linha)

    linha = {}
    linha.update({"final": True})
    for c in range(0, 10):
        linha.update({str(c): estadoId})
    for c in string.ascii_letters:
        linha.update({c:estadoId})
    linha.update({"_": estadoId})
    Tabela_Transicao.append(linha)

    linha = {}
    linha.update({"final": False})
    for c in string.printable:
        linha.update({c:estadoComentario})
    linha.update({"\n": estadoComentario})
    linha.update({"\t": estadoComentario})
    linha.update({"}": estadoComentarioFinal})
    Tabela_Transicao.append(linha)

    linha = {}
    linha.update({"final": True})
    Tabela_Transicao.append(linha)

    linha = {}
    linha.update({"final": True})
    Tabela_Transicao.append(linha)

    linha = {}
    linha.update({"final": True})
    linha.update({"-": estadoRCB})
    linha.update({">": estadoOPRMenorIgualDiferente, "=": estadoOPRMenorIgualDiferente})
    Tabela_Transicao.append(linha)

    linha = {}
    linha.update({"final": True})
    Tabela_Transicao.append(linha)

    linha = {}
    linha.update({"final": True})
    Tabela_Transicao.append(linha)

    linha = {}
    linha.update({"final": True})
    linha.update({"=": estadoOPRMaiorIgual})
    Tabela_Transicao.append(linha)

    linha = {}
    linha.update({"final": True})
    Tabela_Transicao.append(linha)

    linha = {}
    linha.update({"final": True})
    Tabela_Transicao.append(linha)

    linha = {}
    linha.update({"final": True})
    Tabela_Transicao.append(linha)

    linha = {}
    linha.update({"final": True})
    Tabela_Transicao.append(linha)

    linha = {}
    linha.update({"final": True})
    Tabela_Transicao.append(linha)

    linha = {}
    linha.update({"final": True})
    Tabela_Transicao.append(linha)