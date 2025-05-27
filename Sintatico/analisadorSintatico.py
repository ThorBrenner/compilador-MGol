from Lexico.analisadorLexico import *
from Lexico.tabelaSimbolos import *
from Lexico.tabelaTransicao import *
from Semantico.analisadorSemantico import *


BOLD = '\033[1m'
CYANDARK  = "\033[94m"
CYAN = "\033[96m"
GREEN = '\033[92m'
RED = "\033[1;31m"
RESET = '\033[0m'

def traduzToken(token):
    tokenTraduzido = token + "("
    if token == "Num":
        return tokenTraduzido + "Número)"
    if token == "Lit":
        return tokenTraduzido + "Literal)"
    if token == "id":
        return tokenTraduzido + "Identificador)"
    if token == "Comentário":
        return tokenTraduzido + "Comentário)"
    if token == "OPM":
        return tokenTraduzido + "Operador Matemático)"
    if token == "OPR":
        return tokenTraduzido + "Operador Relacional)"
    if token == "ATR":
        return tokenTraduzido + "Atribuição)"
    if token == "AB_P":
        return tokenTraduzido + "Abre Parêntesis - '(')"
    if token == "FC_P":
        return tokenTraduzido + "Fecha Parêntesis - ')')"
    if token == "PT_V":
        return tokenTraduzido + "Ponto e Vírgula - ;)"
    if token == "VIR":
        return tokenTraduzido + "Vírgula - ,)"

    else:
        return token

def analisadorSintatico(tabelaAcoes, tabelaDesvios, tabelaQtdSimbolos, tabelaErros, arquivo, nomeArquivoDestino):

    TabelaTransicao = []
    preenche_tabela_dfa(TabelaTransicao)

    TabelaSimbolos = preenchePalavrasReservadas()

    pilha = []

    pilha_semantica = []

    pilha.append(0)

    pilha_semantica.append({"lexema": "null", "token": "", "tipo": "null", "linha": "", "coluna": ""})

    while True:

        b = analisadorLexico(arquivo, TabelaTransicao, TabelaSimbolos)
        aux = atribuiTipo(b)
        b = aux
        a = b["token"]

        if a != "Comentário" and a != "ERRO":
            break

    flagSimbolo = False

    aAntigo = a

    flagErro = False

    celula = ""

    while(1):
        s = pilha[len(pilha) - 1]
        a = str.lower(a)
        if tabelaAcoes[int(s)].get(a):
            celula = tabelaAcoes[int(s)].get(a)

            operacao = celula[0]
            t = celula.translate({ord('S'): None, ord('R'): None, ord('E'): None})

        else:
            t = 0

        if t and operacao == "S":

            pilha.append(t)

            pilha_semantica.append(b)

            while True:

                if flagSimbolo:
                    a = aAntigo
                    flagSimbolo = False

                else:
                    b = analisadorLexico(arquivo, TabelaTransicao, TabelaSimbolos)
                    aux = atribuiTipo(b)
                    b = aux
                    a = b["token"]

                if a != "Comentário" and a != "ERRO":
                    break

        elif t and operacao == "R":
            x = tabelaQtdSimbolos[int(t) - 1].get("TamanhoBeta")
            A = tabelaQtdSimbolos[int(t) - 1].get("A")
            B = tabelaQtdSimbolos[int(t) - 1].get("Beta")

            tokensParaValidacao = []

            if x:
                for i in range(0, int(x)):
                    pilha.pop()
                    desempilha_semantica = pilha_semantica.pop()
                    tokensParaValidacao.append(desempilha_semantica)

            nTerminal = analisadorSemantico(int(t), A, tokensParaValidacao, TabelaSimbolos)
            t = pilha[len(pilha) - 1]

            if tabelaDesvios[int(t)].get(A):

                valor = tabelaDesvios[int(t)].get(A)
                pilha.append(valor)
                pilha_semantica.append(nTerminal)

            print("Regra aplicada: " + A +" -> " + B + RESET)

        elif t and operacao == "E":
            x = tabelaQtdSimbolos[int(t) - 1].get("TamanhoBeta")
            A = tabelaQtdSimbolos[int(t) - 1].get("A")
            B = tabelaQtdSimbolos[int(t) - 1].get("Beta")

            if x:
                for i in range(0, int(x)):
                    pilha.pop()

            t = pilha[len(pilha) - 1]

            if tabelaDesvios[int(t)].get(A):
                valor = tabelaDesvios[int(t)].get(A)
                pilha.append(valor)

        elif celula == "aceita":

            print()
            print("----------------------------------------------------------------")

            if flagErro:
                print("Análise Sintática finalizada: " + RESET + "foram encontrados erros. " + RED + "Falha!")
                print(RESET + "----------------------------------------------------------------")

            else:
                print("Análise Sintática finalizada: " + GREEN + "aceitou!")
                print(RESET + "----------------------------------------------------------------")

                imprimirArquivo(nomeArquivoDestino)
            return

        else:
            flagErro = True

            simbolosFaltando = {}
            listaParaImprimir = ""

            for k,v in tabelaAcoes[int(s)].items():
                if v != '' and k!='Estado':
                    simbolosFaltando.update({k : v})
                    nomeToken = traduzToken(k)
                    listaParaImprimir = listaParaImprimir + " " + str(nomeToken)

            print(RED + BOLD + "\nErro Sintático. " + RESET + "Linha: " + b.get("linha") +" Coluna: " + b.get("coluna") +" Faltando algum do(s) símbolo(s):" + BOLD + CYANDARK + listaParaImprimir + RESET)

            if len(simbolosFaltando) == 1:
                print("\tTratamento de erro." + RESET + " Inserindo símbolo ausente...")
                chave = [key for key in simbolosFaltando.keys()]

                aAntigo = a

                a = chave[0]

                flagSimbolo = True

                print("\t" + CYANDARK + a + RESET + " inserido para prosseguir a análise.")
                print("\tFim de tratamento de erro\n" + RESET)
            else:
                print("\t\tIniciando tratamento de erro." + RESET + " À procura de um token sincronizante...")

                listaFollow = tabelaErros[int(s)].get('Follow')
                aux = 1

                while (aux):
                    while True:

                        a = analisadorLexico(arquivo, TabelaTransicao, TabelaSimbolos)["token"]

                        if a == "$":

                            print("\t\tArquivo finalizado. Não foi possível concluir a recuperação...")
                            print("\t\tFim de tratamento de erro\n")
                            print("\n----------------------------------------------------------------")
                            print("Análise Sintática finalizada: " + RESET + "foram encontrados erros. " + RED + "Falha!")
                            print(RESET + "----------------------------------------------------------------")
                            return

                        elif a != "Comentário" and a != "ERRO":
                            break

                    for token in listaFollow:
                        if token == a:
                            aux = 0
                            break

                print("\t\tEncontrado token sincronizante: " + CYANDARK + a + RESET)
                x = tabelaErros[int(s)].get('QtdSimbolos')
                if x:
                    for i in range(0, int(x)):
                        pilha.pop()
                        pilha_semantica.pop()

                print("\t\tRetomando análise sintática\n" + RESET)