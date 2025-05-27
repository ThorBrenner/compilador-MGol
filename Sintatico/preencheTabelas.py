import csv

csvTerminais = "Sintatico/Tabela Sintática - Terminais.csv"
csvNaoTerminais = "Sintatico/Tabela Sintática - Não Terminais.csv"
csvQtdSimbolos = "Sintatico/Tabela Sintática - qtd_Simbolos.csv"
csvErros = "Sintatico/Tabela Sintática - Pânico.csv"

def preencheTabela(csvFile):
    tabela = []
    with open(csvFile) as fT:
        dados = csv.DictReader(fT, delimiter=',') 
        for linha in dados:
            tabela.append(linha)
    return tabela


def preencheTabelaAcoes():
    tabela = preencheTabela(csvTerminais)
    return tabela


def preencheTabelaDesvios():
    tabela = preencheTabela(csvNaoTerminais)
    return tabela


def preencheTabelaQtdSimbolos():
    tabela = preencheTabela(csvQtdSimbolos)
    return tabela


def preencheTabelaErros():
    tabela = preencheTabela(csvErros)

    for entrada in tabela:
        if not (entrada['Follow'] == ''):
            lista = entrada['Follow'].split()
            entrada['Follow'] = lista
    return tabela
