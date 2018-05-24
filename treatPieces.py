'''
Trata as informacoes necessarias das pecas quando ainda brutas, ou seja,
antes de estarem completamente ajustadas para a exibicao na tela do jogo.
'''

import os
import sys
import math
import random
from PIL import Image
from tkinter import messagebox
from screenBack import screenBack
from configFile import configFile

class treatPieces:
    '''
    Construtor treatPieces
    '''
    def __init__(self):
        self.arquivo = None
        self.imagem = None
        self.dim = 9,5 #Define o tamanho da coluna e linhas de pecas existentes na imagem original
        self.tamanhoPeca = None #Tamanho original de uma peca
        self.listaPecas = {} #Lista de todas as pecas que compoe o jogo e suas posicoes que aparecem na imagem original
        self.matrizTabuleiro = None #Matriz de pecas a serem passadas para o tabuleiro

    '''
    Retorna o valor de cada peca analisando a imagem de pecas original
    '''
    def tamanhoPecasIndividual(self, arquivo):
        self.arquivo = (screenBack.getCaminhoOther()+"\\%s" %(arquivo))

        if not os.path.isfile(self.arquivo):
            raise messagebox.showwarning("Arquivo PNG:", "Não foi possível carregar o arquivo\n'%s'." %(self.arquivo))
            sys.exit(1)

        self.imagem = Image.open(self.arquivo)
        (imgLargura, imgAltura) = self.imagem.size #Pega a largura e a altura da imagem tiles.png (imagem que contem as pecas)

        if (imgLargura % self.dim[0]  != 0) or (imgAltura % self.dim[1] != 0):
            raise messagebox.showwarning("Tamanho da imagem", "A imagem '%s' não pode ser dividida em peças inteiras." %(self.arquivo))
            sys.exit(1)

        #Definindo o tamanho das pecas
        #//: divisor de piso, pega a parte inteira do resultado da divisao
        self.tamanhoPeca = (imgLargura // self.dim[0]), (imgAltura // self.dim[1])

    '''
    Define o novo tamanho das pecas em relacao a tela e a dimensao do tabuleiro
    '''
    def novoTamanhoPeca(self, dimensao):
        telax = 1024 #Tela eixo X
        telay = 610  #Tela eixo Y
        (pecax, pecay) = self.tamanhoPeca #Tamanho X e Y de uma peca
        (dimx, dimy) = dimensao #Tamanho X e Y do tabuleiro
        pecar = (pecax / pecay) #Tamanho relativo da peca

        #Tamanho peca em relacao ao tamanho da tela
        ptx = (telax / (dimx + 2))
        pty = (telay / (dimy + 2))
        prpx = (ptx / pecar)

        if (prpx < pty):
            pecafy = math.ceil(prpx)
        else:
            pecafy = math.ceil(pty)

        pecafx = math.ceil(pecar * pecafy)
        return(pecafx, pecafy)

    '''
    Retorna a pocicao da peca no conjunto de todas as pecas
    '''
    def getPosicaoPeca(self, nome_peca):
        return (self.listaPecas[nome_peca])

    '''
    Adiciona as pecas e as suas posicoes originais em uma lista
    '''
    def adicionaPosicaoLista(self, todasPecas):
        linha = 0
        for pecas_linha in todasPecas:
            coluna = 0
            for peca in pecas_linha:
                self.listaPecas[peca] = (linha, coluna)
                coluna += 1
            linha += 1

    '''
    Multiplica os tipos de pecas da opcao de tamanho do tabuleiro escolhido
    '''
    def getParesPecas(self, x, y):  # X,Y refere a dimensao do tabuleiro
        qtdTabuleiro = (x * y) #Qtd de pecas a serem colocadas no tabuleiro
        modoJogo = configFile.carregaItemArquivo('tiles') #Pega o conjunto dos possiveis tamanho de tabuleiro

        for opcao in modoJogo:
            dimOpcao = opcao['dim'] #Dimensoes da opcao de jogo
            dim = configFile.tipoDimensao(dimOpcao) #Formata a dimensao
            pecasOpcao = int(opcao['t']) #Qtd de variacao de pecas

            if (dim[0] * dim[1]) == qtdTabuleiro:
                tipo_pecas = opcao['list'] #Pega os tipos de pecas informadas para aquela config. de jogo
                total_pecas = (tipo_pecas * (qtdTabuleiro // pecasOpcao)) #Multiplica as pecas da opcao de jogo para formar pares
                break
        else:
            messagebox.showwarning("Dimensão Tabuleiro:", "O tamanho de tabuleiro não foi tratado no arquivo de configuração.")
            sys.exit(1)

        return(total_pecas)

    '''
    Cria matriz de pecas com a dimensao do tabuleiro selecionado
    '''
    def criaMatriz(self, dimensao):
        (x, y) = dimensao #Pega as posicoes do tabuleiro no eixo x e eixo y
        matriz = [] #Matriz que contem todas as pecas para o jogo e suas respectivas posicoes
        lista_temp = [] #Lista temporaria para salvar as posicoes referentes a matriz

        for i in range(0, y):
            matriz.append([])
            for j in range(0, x):
                matriz[i].append(None)
                lista_temp.append([i, j])

        random.shuffle(lista_temp) #Embaralha a ordem da lista que contem as posicoes da matriz
        #Uma ideia eh dividir por 4, pois o n de pecas a serem usadas podem ser 1/4 da dimensao x y
        pecas_tab = self.getParesPecas(x, y)#Todas as pecas de um modo de jogo multiplicadas para fazer par de pecas

        pos = 0
        for item in lista_temp:
            i = item[0]
            j = item[1]
            matriz[i][j] = pecas_tab[pos]
            pos += 1

        self.matrizTabuleiro = matriz

    '''
    Responsavel por retornar a composicao da matriz de pecas
    '''
    def getComposicaoMatriz(self, dimensao):
        todasPecas = configFile.carregaItemArquivo('tiles-matrix') #Carrega todas as pecas que compoe o jogo
        self.adicionaPosicaoLista(todasPecas) #Passa para uma lista com as posicoes que se seguem cada uma vinda do arquivo
        self.criaMatriz(dimensao) #Funcao para tratar a matriz do tabuleiro
        return(self.matrizTabuleiro)