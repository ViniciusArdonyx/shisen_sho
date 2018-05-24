import os
from random import choice
from PIL import Image, ImageTk

class screenBack:
    '''
    Construtor ScreenBackground
    '''
    def __init__(self):
        self.bg = None
        self.opc1 = None
        self.opc2 = None
        self.opc3 = None
        self.opc4 = None

    '''
    Retorna o caminho onde esta localizado o arquivo "screenBack.py"
    '''
    def getCaminhoMainBack():
        #"os.path.dirname" = retorna o nome do diretorio do caminho
        #"os.path.realpath" = retorna o caminho canonico do nome do arquivo especificado
        return(os.path.dirname(os.path.realpath(__file__)))

    '''
    Retorna o caminho final da pasta others onde encontra-se as imagens da principal
    '''
    def getCaminhoOther():
        return(screenBack.getCaminhoMainBack()+"\\others")

    '''
    Retorna o caminho final da pasta bg onde encontra-se as imagens do tabuleiro
    '''
    def getCaminhoBg():
        return(screenBack.getCaminhoMainBack()+"\\bg")

    '''
    Carrega as imagens da background e das opcoes da tela principal
    '''
    def personalizaPricipal(self):
        caminho = screenBack.getCaminhoOther()
        self.bg = ImageTk.PhotoImage(Image.open(caminho+"\\bg.jpg"))
        self.opc1 = ImageTk.PhotoImage(Image.open(caminho+"\\btn1.jpg"))
        self.opc2 = ImageTk.PhotoImage(Image.open(caminho+"\\btn2.jpg"))
        self.opc3 = ImageTk.PhotoImage(Image.open(caminho+"\\btn3.jpg"))
        self.opc4 = ImageTk.PhotoImage(Image.open(caminho+"\\btn4.jpg"))

    '''
    Carrega uma imagem aleatoria para background durante o jogo
    '''
    def personalizaTabuleiro(self):
        caminho = screenBack.getCaminhoBg()
        #Lista com o nome das imagemns para fundo do tabuleiro
        wpaper = ["campo", "entardecer", "m_gelada", "montanha", "paisagem", "planice"]
        #Choice: retorna um dos itens da lista de forma aleatoria
        self.bg = ImageTk.PhotoImage(Image.open(caminho+"\\%s.jpg" %(choice(wpaper))))