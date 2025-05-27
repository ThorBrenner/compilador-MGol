import sys
from Lexico.tabelaTransicao import *
from Lexico.tabelaSimbolos import *
from Lexico.analisadorLexico import *

TabelaTransicao = []
preenche_tabela_dfa(TabelaTransicao)

TabelaSimbolos = preenchePalavrasReservadas()

argumentos = sys.argv

arq = open("teste.mgol", encoding="utf-8")


while(1):
    resultado = analisadorLexico(arq, TabelaTransicao, TabelaSimbolos)
    if resultado:
        if resultado.get("token") == "$":
            print(resultado)
            break
        else:
            print(resultado)

arq.close() 