'''
Trata de todas as informacoes necessarias para a montagem final do tabuleiro
do jogo. Documento principal para a visualizacao das pecas no tabuleiro.
'''

from tkinter import *
from PIL import Image, ImageTk
from configFile import configFile
from treatPieces import treatPieces
from manageParts import manageParts

class manageBoard:
    '''
    Construtor manageBoard
    '''
    def __init__(self, canvas):
        self.canvas = canvas
        self.gerencia = treatPieces() #Gerencia o tratamento das pecas
        self.dimensao = None  #Dimensao inicial do tabuliero
        self.tamConjunto = None
        self.matriz_pecas = None #Matriz de pecas a serem colocadas no tabuleiro

    '''
    Calcula a tupla do espaco do tabuleiro
    '''
    def getPosicaoTabuleiro(self, pos, nvTamPeca, tConjunto):
        (nvLargura, nvAltura) = nvTamPeca
        (coluna, linha) = pos
        (lConjunto, aConjunto) = tConjunto

        caixa_tabuleiro = ((coluna * nvLargura + lConjunto), (linha * nvAltura + aConjunto),
                           (coluna * nvLargura + nvLargura + lConjunto), (linha * nvAltura + nvAltura + aConjunto))

        return(caixa_tabuleiro)

    '''
    Desenha um tipo de peca em uma posicao da tabela
    '''
    def desenhaPecas(self, matriz_pecas, nvTamPeca, pos, peca):
        (lpeca, apeca) = self.gerencia.tamanhoPeca #Largura e altura peca antes do ajuste
        (lin_base, col_base) = self.gerencia.getPosicaoPeca(peca) #linhae coluna onde se encontra a peca na imagem original

        xl = (col_base * lpeca) #Calcula onde comeca a peca com base na largura de uma peca vezes a coluna que a peca se encontra
        yl = (lin_base * apeca) #Calcula onde comeca a peca com base na altura de uma peca vezes a linha que a peca se encontra

        #Corta a peca da imagem original
        tuplaPeca = (xl, yl, xl + lpeca, yl + apeca) #Dimensoes onde se encontra a peca desejada
        dimOriginal = self.gerencia.imagem.crop(tuplaPeca) #Realiza recorte da peca

        #Reajustando as dimensoes da peca
        novaDimensao = dimOriginal.resize(size=nvTamPeca, resample=Image.BICUBIC) #Reajusta o tamanho da peca

        tuplaTab = self.getPosicaoTabuleiro(pos, nvTamPeca, self.tamConjunto)
        espacoTK = ImageTk.PhotoImage(novaDimensao)
        canvasref = self.canvas.create_image(tuplaTab[0], tuplaTab[1], image=espacoTK, anchor=NW)
        #self.canvas.itemconfig(canvasref, image=espacoTK)

        pecaTab = manageParts()
        pecaTab.tipo = peca
        pecaTab.posicao = pos
        pecaTab.tupla = tuplaTab
        pecaTab.canvasref = canvasref
        pecaTab.objTK = espacoTK
        pecaTab.objImagem = novaDimensao
        return(pecaTab)

    '''
    Retorna a matriz final das pecas
    '''
    def getMatrizPecas(self, matrizTab, nvTamPeca):
        (dimx, dimy) = self.dimensao #Tamanho X e Y do tabuleiro
        matriz = [[None for x in range(dimx)] for x in range(dimy)]

        #Carrega as pecas para a tela
        linha = 0
        for lpecas in matrizTab: #linha de pecas
            coluna = 0
            for peca in lpecas:
                pos = (coluna, linha) #posicao
                pecaTab = self.desenhaPecas(matrizTab, nvTamPeca, pos, peca)
                matriz[linha][coluna] = pecaTab
                coluna += 1
            linha += 1

        return(matriz)

    '''
    Responsavel por configurar todo o tabuleiro
    '''
    def configuraTabuleiro(self):
        #Atraves da imagem completa, pega os valores das pecas de forma individual
        arquivo = configFile.carregaItemArquivo('tiles-file')
        self.gerencia.tamanhoPecasIndividual(arquivo)

        #Pega as dimensoes iniciais no arquivo
        dimArquivo = configFile.carregaItemArquivo('initial-dim')
        self.dimensao = configFile.tipoDimensao(dimArquivo) #Funcao para verificar a dimensao inicial do tabuleiro

        #Configuracoes da matriz de pecas
        matrizTab = self.gerencia.getComposicaoMatriz(self.dimensao)

        #Novo tamanho das pecas para encaixarem no tamanho do tabuleiro
        nvTamPeca = self.gerencia.novoTamanhoPeca(self.dimensao)
        self.tamConjunto = nvTamPeca

        #self.canvas.create_rectangle(65, 35, 135, 65, fill="yellow")
        self.matriz_pecas = self.getMatrizPecas(matrizTab, nvTamPeca)
        self.tela.update() #Atualiza a tela para mostrar a matriz de pecas