from tkinter import *
from screenBack import screenBack
from configFile import configFile
from manageBoard import manageBoard

class window:
	'''
	Construtor Window
	'''
	def __init__(self):
		self.tela = Tk()
		self.caminho = None
		self.dimTela = 1026, 612 #Dimensoes da tela do jogo
		self.canvas = Canvas(self.tela)
		self.frame = Frame(self.tela)

	'''
	Configura a janela
	'''
	def configuraJanela(self, janela):
		titulo = configFile.carregaItemArquivo('app-title') #Busca no arquivo JSON o titulo do jogo
		versao = configFile.carregaItemArquivo('version') #Busca no arquivo JSON a versao do jogo
		tituloFormatado = titulo.replace("%v%", versao) #Ajusta o titulo e a versao do jogo
		janela.title(tituloFormatado)
		janela.iconbitmap(bitmap="logo.ico") #Seta logo da janela

		#---- Centraliza a janela --------------------------------------------------------------------------------------
		(largura, altura) = self.dimTela #Largura e altura definada para a tela do tk

		#Usado para recuperar a largura e a altura da janela para garantir que os valores retornados sejam precisos
		janela.update_idletasks()

		w = janela.winfo_screenwidth()  #Largura do monitor
		h = janela.winfo_screenheight() #Altura do monitor
		x = (w/2 - largura/2) #eixo x
		y = (h/2 - altura/2)  #eixo y
		janela.geometry("%dx%d+%d+%d" %(largura, altura, x, y))
		#---------------------------------------------------------------------------------------------------------------

		janela.resizable(False, False) #Tornando a tela nao redimensionavel

	'''
	Controla as acoes dos botoes da tela principal
	'''
	def acoesPrincipal(self, btn1, btn2, btn3, btn4):
		btn1.config(command=lambda: self.backgroundTabuleiro(self.tela, self.caminho))#Botao Jogar: chama funcao de construir tabuleiro
		btn2.config(command=lambda: self.backgroundTabuleiro(self.tela, self.caminho))#Botao SA: chama funcao de construir tabuleiro
		btn3.config(command=self.frame.destroy) #Botao Sobre: informações do jogo e do desenvolvedor
		btn4.config(command=self.tela.destroy)#Botao de Sair: termina a execucao

	'''
	Carrega o background da tela principal
	'''
	def backgroundPrincipal(self, janela, caminho):
		#Reseta o canvas
		self.canvas.destroy()
		self.canvas = Canvas(janela, width=self.dimTela[0], height=self.dimTela[1])
		self.canvas.pack()

		#Configurando a imagem de background
		caminho.personalizaPricipal() #Carrega as imagens para usar na tela principal
		backg = self.canvas.create_image(0, 0, image=caminho.bg, anchor=NW)
		self.canvas.itemconfig(backg, image=caminho.bg)

		#Setando os botoes
		btn1 = Button(self.canvas)
		btn1["image"] = caminho.opc1 #Define a imagem para o botao
		btn1Window = self.canvas.create_window(448, 325, window=btn1, anchor=NW)

		btn2 = Button(self.canvas)
		btn2["image"] = caminho.opc2 #Define a imagem para o botao
		btn2Window = self.canvas.create_window(448, 395, window=btn2, anchor=NW)

		btn3 = Button(self.canvas)
		btn3["image"] = caminho.opc3 #Define a imagem para o botao
		btn3Window = self.canvas.create_window(448, 465, window=btn3, anchor=NW)

		btn4 = Button(self.canvas)
		btn4["image"] = caminho.opc4 #Define a imagem para o botao
		btn4Window = self.canvas.create_window(448, 535, window=btn4, anchor=NW)

		self.acoesPrincipal(btn1, btn2, btn3, btn4)

	'''
	Carrega o background do tabuleiro
	'''
	def backgroundTabuleiro(self, janela, caminho):
		#Reseta o canvas
		self.canvas.destroy()
		self.canvas = Canvas(janela, width=self.dimTela[0], height=self.dimTela[1])
		self.canvas.pack()

		#Configurando a imagem de background
		caminho.personalizaTabuleiro() #Carrega a imagem para usar na tela de fundo do jogo
		backg = self.canvas.create_image(0, 0, image=caminho.bg, anchor=NW)
		self.canvas.itemconfig(backg, image=caminho.bg)

		#Realiza todas configuracoes para organizar o tabuleiro
		tabuleiro = manageBoard(self.canvas)
		tabuleiro.configuraTabuleiro()

	'''
	Inicia o programa
	'''
	def inicializa(self):
		self.caminho = screenBack()
		self.configuraJanela(self.tela) #Funcao para configuracoes puras de tela
		self.backgroundPrincipal(self.tela, self.caminho) #Chama as configuracoes de interface da tela principal

		#Mantem a tela ativa
		self.tela.mainloop()
		self.tela.destroy