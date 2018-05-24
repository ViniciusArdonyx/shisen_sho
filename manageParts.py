import os
import math
import random
from PIL import Image
from tkinter import messagebox
from screenBack import screenBack
from configFile import configFile

class manageParts:
    '''
    Construtor manageParts
    '''
    def __init__(self):
        self.tipo = None  #Tipo = nome da peca
        self.tupla = None #(x1,y1,x2,y2)
        self.objTK = None
        self.tamanho = None
        self.posicao = None
        self.canvasref = None
        self.objImagem = None