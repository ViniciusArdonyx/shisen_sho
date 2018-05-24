import json
from tkinter import messagebox
from screenBack import screenBack

class configFile:
    '''
    Construtor configFile
    '''
    def __init__(self):
        self.arquivo = "config.json"
        self.controle = None #Controla funcoes(abrir, fechar, etc) do arquivo
        self.dados = None #Contem o conteudo do arquivo

    '''
    Retorna o caminho onde se encontra o arquivo JSON
    '''
    def getCaminhoJson(arquivoJson):
        return(screenBack.getCaminhoMainBack()+"\\%s" %(arquivoJson))

    '''
    Abre o arquivo
    '''
    def carregaArquivo(self):
        try:
            self.controle = open(configFile.getCaminhoJson(self.arquivo), 'r')
        except FileNotFoundError:
            raise messagebox.showwarning("Arquivo JSON:","Não foi possível carregar o arquivo json.")
            exit(1)

        self.dados = self.controle.read()

    '''
    Retorna um item especifico do conteudo do arquivo
    '''
    def carregaItemArquivo(item):
        arq = configFile()
        arq.carregaArquivo()
        arq.controle.close()

        try:
            conteudo = json.loads(arq.dados)
        except ValueError:
            raise messagebox.showwarning("Arquivo JSON:","Não foi possível carregar o arquivo json.")
            exit(1)

        return(conteudo[item])

    '''
    Verifica as opcoes de dimensoes de entrada
    '''
    def tipoDimensao(dimArquivo):
        #Trata todos os tipos de possiveis dimensoes
        #Ja retorno a informacao em inteiro
        if (dimArquivo[2] == ",") and (dimArquivo[4] == "]"):
            dimensao = int(dimArquivo[1]), int(dimArquivo[3])
        elif (dimArquivo[2] == ",") and (dimArquivo[5] == "]"):
            dimensao = int(dimArquivo[1]), int(dimArquivo[3:5])
        elif (dimArquivo[2] != ",") and (dimArquivo[5] == "]"):
            dimensao = int(dimArquivo[1:3]), int(dimArquivo[4])
        elif (dimArquivo[2] != ",") and (dimArquivo[5] != "]"):
            dimensao = int(dimArquivo[1:3]), int(dimArquivo[4:6])

        return(dimensao)