#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class SemanticAnalyzer:
    def __init__(self):
        self.texto_arquivo = []
        self.texto_variaveis_temporarias = []
        self.contador_temporarias = 0
        self.flag_erro = False
        
        # Output formatting
        self.BOLD = '\033[1m'
        self.CYANDARK = "\033[94m"
        self.CYAN = "\033[96m"
        self.GREEN = '\033[92m'
        self.RED = "\033[1;31m"
        self.RESET = '\033[0m'
    
    def atribui_tipo(self, token_tupla):
        if token_tupla['token'] == 'OPM':
            token_tupla['tipo'] = token_tupla['lexema']
        elif token_tupla['token'] == 'lit':
            token_tupla['tipo'] = 'literal'
        elif token_tupla['token'] == 'inteiro':
            token_tupla['tipo'] = 'int'
        elif token_tupla['token'] == 'real':
            token_tupla['tipo'] = 'real'
        elif token_tupla['token'] == 'OPR':
            token_tupla['tipo'] = token_tupla['lexema']
        elif token_tupla['token'] == 'RCB':
            token_tupla['tipo'] = '='
        return token_tupla
    
    def imprimir_arquivo(self, nome_arquivo_destino):
        print(self.BOLD + "----------------------------------------------------------------")
        
        if self.flag_erro:
            print("Análise Semântica finalizada: " + self.RESET + "foram encontrados erros. " + self.RED + "Falha!")
            print(self.RESET + self.BOLD + "----------------------------------------------------------------")    
            return
        
        print("Análise Semântica finalizada: " + self.GREEN + "aceitou!")
        print(self.RESET + self.BOLD + "----------------------------------------------------------------")    
        
        try:
            with open(f"{nome_arquivo_destino}.c", "w+") as arq_destino:
                arq_destino.write("#include<stdio.h>\n\n")
                arq_destino.write("typedef char literal[256];\n")
                arq_destino.write("typedef double real;\n\n")
                arq_destino.write("void main(void){\n")
                
                arq_destino.write("\t/*----Variaveis temporarias----*/\n")
                for texto in self.texto_variaveis_temporarias:
                    arq_destino.write(f"\t{texto}\n")
                arq_destino.write("\t/*------------------------------*/\n")
                
                contador_identacao = 1
                for texto in self.texto_arquivo:
                    if "}" in texto:
                        contador_identacao -= 1
                    
                    for i in range(0, contador_identacao):
                        arq_destino.write("\t")
                    
                    arq_destino.write(f"{texto}\n")
                    
                    if "{" in texto:
                        contador_identacao += 1
                
                arq_destino.write("}\n")
                
            print(f"Arquivo {nome_arquivo_destino}.c gerado")
        except IOError:
            print(self.RED + "Erro ao criar arquivo de saída" + self.RESET)
    
    def imprimir_terminal(self, texto_impressao):
        print(self.BOLD + "\n-----------------------" + " SEMÂNTICO " + "-----------------------")
        print(texto_impressao)
        print(self.BOLD + "---------------------------------------------------------\n" + self.RESET)
    
    def verificar_compatibilidade_tipos(self, tipo1, tipo2, operacao):
        if operacao == 'aritmetica':
            if tipo1 == 'literal' or tipo2 == 'literal':
                return False, None
            
            if tipo1 == 'real' or tipo2 == 'real':
                return True, 'real'
            
            return True, 'int'
            
        elif operacao == 'relacional':
            if tipo1 == 'literal' or tipo2 == 'literal':
                return False, None
                
            return True, 'int'
            
        elif operacao == 'atribuicao':
            if tipo1 == tipo2:
                return True, tipo1
            elif tipo1 == 'real' and tipo2 == 'int':
                return True, 'real'
            else:
                return False, None
                
        return False, None
    
    def gerar_variavel_temporaria(self, tipo):
        nome_temp = f"T{self.contador_temporarias}"
        self.texto_variaveis_temporarias.append(f"{tipo} {nome_temp};")
        self.imprimir_terminal(f"Gerada variável temporária: {self.GREEN}{nome_temp}{self.RESET}")
        self.contador_temporarias += 1
        return nome_temp
        
    def analisar(self, t, A, tokens_para_validacao, tabela_simbolos):
        tupla = {"lexema": str(A), "token": str(A), "tipo": "", "linha": "", "coluna": ""}
        
        # Ensure tokens_para_validacao is not None and is a list
        if not isinstance(tokens_para_validacao, list):
            tokens_para_validacao = []
        
        try:
            if t == 5:  # LV -> varfim;
                self.texto_arquivo.append("\n\n")
                self.imprimir_terminal(f"Impresso no arquivo: {self.CYAN}\n\n{self.RESET}")
            
            elif t == 6:  # D -> id TIPO;
                if len(tokens_para_validacao) >= 2:
                    id_token = tokens_para_validacao.pop()
                    tipo_token = tokens_para_validacao.pop()
                    
                    tabela_simbolos[id_token['lexema']]['tipo'] = tipo_token['tipo']
                    texto = f"{tipo_token['tipo']} {id_token['lexema']};"
                    self.texto_arquivo.append(texto)
                    self.imprimir_terminal(f"Impresso no arquivo: {self.CYAN}{texto}{self.RESET}")
            
            elif t == 7:  # TIPO -> inteiro
                if tokens_para_validacao:
                    inteiro_token = tokens_para_validacao.pop()
                    tupla['tipo'] = inteiro_token['tipo']
            
            elif t == 8:  # TIPO -> real
                if tokens_para_validacao:
                    real_token = tokens_para_validacao.pop()
                    tupla['tipo'] = real_token['tipo']
            
            elif t == 9:  # TIPO -> literal
                if tokens_para_validacao:
                    literal_token = tokens_para_validacao.pop()
                    tupla['tipo'] = literal_token['tipo']
            
            elif t == 11:  # ES -> leia id;
                if len(tokens_para_validacao) >= 2:
                    tokens_para_validacao.pop()  # Pop 'leia' token
                    id_token = tokens_para_validacao.pop()
                    
                    if id_token['tipo'] == "null":
                        texto = f"{self.RED}Erro Semântico: {self.RESET}{self.BOLD}Variável não declarada!\nLinha: {self.RESET}{id_token['linha']}{self.BOLD} Coluna: {self.RESET}{id_token['coluna']}"
                        self.flag_erro = True
                    else:
                        if id_token['tipo'] == "literal":
                            texto = f'scanf("%s", {id_token["lexema"]});'
                        elif id_token['tipo'] == "int":
                            texto = f'scanf("%d", &{id_token["lexema"]});'
                        elif id_token['tipo'] == "real":
                            texto = f'scanf("%lf", &{id_token["lexema"]});'
                        
                        if not self.flag_erro:
                            self.texto_arquivo.append(texto)
                    
                    self.imprimir_terminal(f"Impresso no arquivo: {self.CYAN}{texto}{self.RESET}")
            
            elif t == 12:  # ES -> escreva ARG;
                if len(tokens_para_validacao) >= 2:
                    tokens_para_validacao.pop()  # Pop 'escreva' token
                    arg_token = tokens_para_validacao.pop()
                    
                    if arg_token['token'] == 'Literal':
                        texto = f"printf({arg_token['lexema']});"
                    elif arg_token['token'] == "id":
                        if arg_token["tipo"] == "null":
                            texto = f"{self.RED}Erro Semântico: {self.RESET}{self.BOLD}Variável não declarada!\nLinha: {self.RESET}{arg_token['linha']}{self.BOLD} Coluna: {self.RESET}{arg_token['coluna']}"
                            self.flag_erro = True
                        else:
                            if arg_token["tipo"] == 'int':
                                texto = f'printf("%d", {arg_token["lexema"]});'
                            elif arg_token["tipo"] == 'real':
                                texto = f'printf("%lf", {arg_token["lexema"]});'
                            elif arg_token["tipo"] == 'literal':
                                texto = f'printf("%s", {arg_token["lexema"]});'
                    
                    if arg_token['tipo'] and not self.flag_erro:
                        self.texto_arquivo.append(texto)
                        self.imprimir_terminal(f"Impresso no arquivo: {self.CYAN}{texto}{self.RESET}")
            
            elif t == 13:  # ARG -> literal
                if tokens_para_validacao:
                    literal_token = tokens_para_validacao.pop()
                    tupla.update(literal_token)
            
            elif t == 14:  # ARG -> num
                if tokens_para_validacao:
                    num_token = tokens_para_validacao.pop()
                    tupla.update(num_token)
            
            elif t == 15:  # ARG -> id
                if tokens_para_validacao:
                    id_token = tokens_para_validacao.pop()
                    if id_token['tipo'] != "null":
                        tupla.update(id_token)
                    else:
                        self.imprimir_terminal(f"{self.RED}Erro Semântico: {self.RESET}{self.BOLD}Variável não declarada!\nLinha: {self.RESET}{id_token['linha']}{self.BOLD} Coluna: {self.RESET}{id_token['coluna']}")
                        self.flag_erro = True
            
            elif t == 17:  # CMD -> id rcb LD;
                if len(tokens_para_validacao) >= 3:
                    id_token = tokens_para_validacao.pop()
                    rcb_token = tokens_para_validacao.pop()
                    ld_token = tokens_para_validacao.pop()
                    
                    if id_token['tipo'] != "null":
                        is_compatible, _ = self.verificar_compatibilidade_tipos(id_token['tipo'], ld_token['tipo'], 'atribuicao')
                        
                        if is_compatible:
                            texto = f"{id_token['lexema']} {rcb_token['tipo']} {ld_token['lexema']};"
                            self.texto_arquivo.append(texto)
                            self.imprimir_terminal(f"Impresso no arquivo: {self.CYAN}{texto}{self.RESET}")
                        else:
                            texto = f"{self.RED}Erro Semântico: {self.RESET}{self.BOLD}Tipos incompatíveis para atribuição.\nLinha: {self.RESET}{id_token['linha']}{self.BOLD} Coluna: {self.RESET}{id_token['coluna']}"
                            self.flag_erro = True
                            self.imprimir_terminal(texto)
                    else:
                        texto = f"{self.RED}Erro Semântico: {self.RESET}{self.BOLD}Variável não declarada!\nLinha: {self.RESET}{id_token['linha']}{self.BOLD} Coluna: {self.RESET}{id_token['coluna']}"
                        self.flag_erro = True 
                        self.imprimir_terminal(texto)
            
            elif t == 18:  # LD -> OPRD1 opm OPRD2
                if len(tokens_para_validacao) >= 3:
                    oprd1_token = tokens_para_validacao.pop()
                    opm_token = tokens_para_validacao.pop()
                    oprd2_token = tokens_para_validacao.pop()
                    
                    is_compatible, result_type = self.verificar_compatibilidade_tipos(
                        oprd1_token['tipo'], oprd2_token['tipo'], 'aritmetica'
                    )
                    
                    if is_compatible:
                        temp_var = self.gerar_variavel_temporaria(result_type)
                        tupla['lexema'] = temp_var
                        tupla["tipo"] = result_type
                        
                        texto = f"{temp_var} = {oprd1_token['lexema']} {opm_token['tipo']} {oprd2_token['lexema']};"
                        self.texto_arquivo.append(texto)
                        self.imprimir_terminal(f"Impresso no arquivo: {self.CYAN}{texto}{self.RESET}")
                    else:
                        texto = f"{self.RED}Erro Semântico: {self.RESET}{self.BOLD}Operandos com tipos incompatíveis para operação aritmética.\nLinha: {self.RESET}{oprd2_token['linha']}{self.BOLD} Coluna: {self.RESET}{oprd2_token['coluna']}"
                        self.flag_erro = True 
                        self.imprimir_terminal(texto)
            
            elif t == 19:  # LD -> OPRD
                if tokens_para_validacao:
                    oprd_token = tokens_para_validacao.pop()
                    tupla.update(oprd_token)
            
            elif t == 20:  # OPRD -> id
                if tokens_para_validacao:
                    id_token = tokens_para_validacao.pop()
                    if id_token['tipo'] != "null":
                        tupla.update(id_token)
                    else:
                        self.imprimir_terminal(f"{self.RED}Erro Semântico: {self.RESET}{self.BOLD}Variável não declarada!\nLinha: {self.RESET}{id_token['linha']}{self.BOLD} Coluna: {self.RESET}{id_token['coluna']}")
                        self.flag_erro = True
            
            elif t == 21:  # OPRD -> num
                if tokens_para_validacao:
                    num_token = tokens_para_validacao.pop()
                    tupla.update(num_token)
            
            elif t == 23:  # COND -> CABEÇALHO CORPO
                self.texto_arquivo.append("}")
                self.imprimir_terminal(f"Impresso no arquivo: {self.CYAN}}}{self.RESET}")
            
            elif t == 24:  # CABEÇALHO -> se (EXPR) então
                if len(tokens_para_validacao) >= 5:
                    tokens_para_validacao.pop()  # se
                    tokens_para_validacao.pop()  # (
                    expr_token = tokens_para_validacao.pop()  # EXPR
                    tokens_para_validacao.pop()  # )
                    tokens_para_validacao.pop()  # então
                    
                    texto = f"if ({expr_token['lexema']}){{"
                    self.texto_arquivo.append(texto)
                    self.imprimir_terminal(f"Impresso no arquivo: {self.CYAN}{texto}{self.RESET}")
            
            elif t == 25:  # EXP_R -> OPRD1 opr OPRD2
                if len(tokens_para_validacao) >= 3:
                    oprd1_token = tokens_para_validacao.pop()
                    opr_token = tokens_para_validacao.pop()
                    oprd2_token = tokens_para_validacao.pop()
                    
                    is_compatible, result_type = self.verificar_compatibilidade_tipos(
                        oprd1_token['tipo'], oprd2_token['tipo'], 'relacional'
                    )
                    
                    if is_compatible:
                        temp_var = self.gerar_variavel_temporaria(result_type)
                        tupla['lexema'] = temp_var
                        tupla["tipo"] = result_type
                        
                        texto = f"{temp_var} = {oprd1_token['lexema']} {opr_token['tipo']} {oprd2_token['lexema']};"
                        self.texto_arquivo.append(texto)
                        
                        tupla['valorEXP'] = texto
                        self.imprimir_terminal(f"Impresso no arquivo: {self.CYAN}{texto}{self.RESET}")
                    else:
                        texto = f"{self.RED}Erro Semântico: {self.RESET}{self.BOLD}Operandos com tipos incompatíveis para operação relacional.\nLinha: {self.RESET}{oprd2_token['linha']}{self.BOLD} Coluna: {self.RESET}{oprd2_token['coluna']}"
                        self.flag_erro = True 
                        self.imprimir_terminal(texto)
            
            elif t == 31:  # REPETE -> TESTE AÇÃO
                self.texto_arquivo.append("}")
                self.imprimir_terminal(f"Impresso no arquivo: {self.CYAN}}}{self.RESET}")
            
            elif t == 32:  # TESTE -> enquanto (EXP_R) faça
                if len(tokens_para_validacao) >= 5:
                    tokens_para_validacao.pop()  # enquanto
                    tokens_para_validacao.pop()  # (
                    expr_token = tokens_para_validacao.pop()  # EXP_R
                    tokens_para_validacao.pop()  # )
                    tokens_para_validacao.pop()  # faça
                    
                    texto = f"while ({expr_token['lexema']}){{"
                    self.texto_arquivo.append(texto)
                    self.imprimir_terminal(f"Impresso no arquivo: {self.CYAN}{texto}{self.RESET}")
                    
                    if "valorEXP" in expr_token:
                        texto = expr_token["valorEXP"]
                        self.texto_arquivo.append(texto)
                        self.imprimir_terminal(f"Impresso no arquivo: {self.CYAN}{texto}{self.RESET}")
            
        except Exception as e:
            self.imprimir_terminal(f"{self.RED}Erro Semântico: {self.RESET}{self.BOLD}Erro ao processar regra {t}: {str(e)}")
            self.flag_erro = True
            
        return tupla

# Create singleton instance
semantic_analyzer = SemanticAnalyzer()

# Compatibility functions
def atribuiTipo(token_tupla):
    return semantic_analyzer.atribui_tipo(token_tupla)

def imprimirArquivo(nome_arquivo_destino):
    return semantic_analyzer.imprimir_arquivo(nome_arquivo_destino)

def imprimirTerminal(texto_impressao):
    return semantic_analyzer.imprimir_terminal(texto_impressao)

def analisadorSemantico(t, A, tokens_para_validacao, tabela_simbolos):
    return semantic_analyzer.analisar(t, A, tokens_para_validacao, tabela_simbolos)