import pygame
import random
import serial.tools.list_ports
import datetime  #ou biblioteca time: time.localtime([5])
import time


pygame.init()

tamanho_janela_x = 1200
tamanho_janela_y = 650
cor_tela = (0,128,128) #RGB

tela_de_visualizacao = pygame.display.set_mode((tamanho_janela_x, tamanho_janela_y))
tela_de_visualizacao.fill(cor_tela)


font = pygame.font.Font('freesansbold.ttf', 16)

class button():
    def __init__(self, screen, color, x, y, width, height, text=''):
        self.screen = screen
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, outline=True): # Draw the Button
        if outline:
            pygame.draw.rect(self.screen, (0,0,0), (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(self.screen, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            text = font.render(self.text, True, (0, 0, 0))
            (self.screen).blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def cursor_is_over(self, position): #Mouse position in tuple (x,y)
        if position[0] > self.x and position[0] < self.x + self.width:
            if position[1] > self.y and position[1] < self.y + self.height:
                return True
        return False

botao_de_conexao = button(tela_de_visualizacao,(255,0,0), 100, 100, 100, 20, 'Conectar')



lista_de_nomes = []
lista_de_passos = []
lista_de_listas = []
lista_de_maiores_valores = [] #+- inf NaN

porta_serial = None


def conexao():
    global lista_de_nomes
    global lista_de_passos
    global lista_de_listas
    global porta_serial
    global lista_de_maiores_valores
    portas = [comport.device for comport in serial.tools.list_ports.comports()]
    print("COMs:" + str(portas))
    for i in range(len(portas)):
        try:
            porta_selecionada = portas[i]
            porta_serial = serial.Serial(porta_selecionada, 9600, timeout=3)
            time.sleep(3) #necessario
        except serial.SerialException: #Exception
            print("identificado: PermissionError")
        else:
            porta_serial.reset_input_buffer()
            porta_serial.write("conectar".encode())
            tempo = time.time()
            while not porta_serial.in_waiting or (time.time() - tempo < 3):
                pass
            if porta_serial.in_waiting:
                input = porta_serial.readline().decode('utf-8').strip()
                print(input)
                if(input == "inicio"): #qualquer outro caso faz porta_serial = None
                    lista_de_nomes = []
                    lista_de_passos = []
                    lista_de_listas = []
                    lista_de_maiores_valores = []
                    while(1):
                        input = porta_serial.readline().decode('utf-8').strip()
                        print(input)
                        if(input == "fim"):
                            break
                        lista_input = input.split(";")
                        lista_de_nomes.append(lista_input[0])
                        lista_de_passos.append(float(lista_input[1]))
                        lista_de_listas.append([])
                        lista_de_maiores_valores.append(0)
                    break
            porta_serial = None



#########################################################################


tamanho_da_janela_1 = 1
tamanho_minimo_de_janela = 5 #precisa de funcao especifica para tratar

cor_do_fundo_do_grafico = (0,0,0)
cor_da_linha_vertical_de_informacao_do_grafico = (255,255,255)
cor_da_informacao_do_grafico = (255,255,255)
lista_de_cores_das_linhas = [(255,0,0),(0,255,0),(0,0,255)]

#proporcao = 0.95 #para nao encostar no teto do grafico

#lista de valores é dada por função intermediária que interage com guias selcionadas
#minimo tamanho do grafico é o valor do menor passo
#linhas verticais de grafico
#clicar em grafico o realça
#grafico
#acesso a com e receber valores
#tamanho da janela
#valores negativos
#proporcao_da_altura

class grafico():
    def __init__(self, tela_de_visualizacao, x, y, largura, altura, lista_de_cores_das_linhas):
        self.lista_de_cores_das_linhas = lista_de_cores_das_linhas #ordenar
        self.x = x
        self.y = y
        self.largura = largura
        self.altura = altura
        self.tela_de_visualizacao = tela_de_visualizacao

        self.lista_de_listas = []
        self.lista_de_passos = []
        self.lista_de_maiores_valores = []
        self.tamanho_da_janela = 40

    def desenha_grafico(self): #pode usar só self?

        pygame.draw.rect(self.tela_de_visualizacao, cor_do_fundo_do_grafico, (self.x, self.y, self.largura, self.altura))

        '''listas_para_visualizar = []

        for i in range(len(lista_de_listas)):

            if len(lista_de_listas[i]) - 1 < tamanho_da_janela:
                listas_para_visualizar.append(lista_de_listas[i])

            else:
                listas_para_visualizar.append(lista[len(lista) - tamanho_da_janela: len(lista) + tamanho_da_janela])

        lista_de_listas_de_coordenadas = []'''

        '''for i in range(len(lista_de_listas)): #evita divisao por 0
            if maior_valor > 0:
                multiplicador_vertical = proporcao* self.altura / lista_de_maiores_valores[i]
            else:
                multiplicador_vertical = proporcao * self.altura
            multiplicador_horizontal = self.largura / (tamanho_da_janela - 1)

            lista_de_listas_de_coordenadas.append([])

            for j in range(len(listas_para_visualizar[i])):
                coordx = self.x + fator_horizontal * j
                coordy = self.y - fator_vertical * lista_de_listas_de_coordenadas[i][j]
                lista_de_listas_de_coordenadas[i].append((x, y))'''

'''def grafico(guia, lista, lista2, posicao_inicial, origemx, origemy, larguradisplay, alturadisplay, janela,posicao):   #gera graficos

    if len(lista) - 1 < tamanho:
        coord = lista
        coord2 = lista2
    else:
        coord = lista[posicao_inicial: posicao_inicial + janela]
        coord2 = lista2[posicao_inicial: posicao_inicial + janela]

    final = []
    final2 = []

    if maior_valor > 0:
        fator_vertical = (proporcao) * alturadisplay/maior_valor
    else:
        fator_vertical = (proporcao) * alturadisplay
    fator_horizontal = larguradisplay/(tamanho-1)


    x = 0
    y = 0

    #tuplas
    for j in range(len(coord)):
        x = origemx + fator_horizontal*j
        y = origemy - fator_vertical*coord[j]
        y2 = origemy - fator_vertical*coord2[j]
        final.append((x, y))
        final2.append((x,y2))

        if estado == False:
            if x - alcance < posicao[0] and x + alcance > posicao[0]:
                if y - alcance < posicao[1] and y + alcance > posicao[1]:
                    escreve_x = j
                    escreve_y = coord[j]

                    pygame.draw.rect(tela_de_visualizacao,(100,100,100),(x,y,150,40))

                    escrevevalor(x,y,j)
                    escrevevalor(x,y+20,escreve_y,e_segundo=False,bola=False)

    if len(coord) > 1:
        if guia.list[0] == True:
            check1.estate = True
        else:
            check1.estate = False
        if guia.list[1] == True:
            check2.estate = True
        else:
            check2.estate = False


    if len(coord) > 1:
        if check1.estate == True:
            pygame.draw.lines(tela_de_visualizacao, (255, 0, 0), False, final, 3)
        if check2.estate == True:
            pygame.draw.lines(tela_de_visualizacao, (255, 0, 0), False, final2, 3)'''


    #def atualiza_valores
    #def informacao_mouse

grafico_principal = grafico(tela_de_visualizacao,300,100,800,400,lista_de_cores_das_linhas)


programa_funcionando = True
while programa_funcionando:

    grafico_principal.desenha_grafico()
    botao_de_conexao.draw(tela_de_visualizacao)

    if porta_serial and porta_serial.in_waiting:
        input = porta_serial.readline().decode('utf-8').strip()
        print(input)
        lista_input = input.split(";")
        for i in range(len(lista_de_listas)):
            if lista_input[0] == lista_de_nomes[i]:
                lista_de_listas[i].append(int(lista_input[1]))
                if lista_de_maiores_valores[i] < int(lista_input[1]):
                    lista_de_maiores_valores[i] = int(lista_input[1])


    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()
        press = pygame.mouse.get_pressed(3)

        if event.type == pygame.QUIT:
            programa_funcionando = False

        if event.type == pygame.MOUSEBUTTONDOWN and press == (1,0,0):
            if botao_de_conexao.cursor_is_over(pos): #evitar travar com "millis"
                print("click")
                botao_de_conexao.text = "Conectando"
                botao_de_conexao.color = (255,255,0)
                botao_de_conexao.draw(tela_de_visualizacao)
                pygame.display.update()
                time.sleep(1)
                conexao()##############################################não tem como ser função se vai continuar while 1
                if porta_serial:
                    botao_de_conexao.color = (0,255,0)
                    botao_de_conexao.text = "Conectado"
                else:
                    botao_de_conexao.color = (255,0,0)
                    botao_de_conexao.text = "Conectar"


    pygame.display.update()

print(lista_de_passos)
print(lista_de_nomes)
print(porta_serial)
print(lista_de_listas)
print(lista_de_maiores_valores)