import sys
from Lexico.tabelaTransicao import *
from Lexico.tabelaSimbolos import *
from Lexico.analisadorLexico import *
from Sintatico.analisadorSintatico import *
from Sintatico.preencheTabelas import *
from Semantico.analisadorSemantico import *
import os


tabelaAcoes = preencheTabelaAcoes()
tabelaDesvios = preencheTabelaDesvios()
tabelaQtdSimbolos = preencheTabelaQtdSimbolos()
tabelaErros = preencheTabelaErros()


argumentos = sys.argv
arqFonte = open(argumentos[1], encoding="utf-8")
print(arqFonte)

nome, extensao = os.path.splitext("fonte.alg")


analisadorSintatico(tabelaAcoes,tabelaDesvios,tabelaQtdSimbolos, tabelaErros, arqFonte, nome)

arqFonte.close()
