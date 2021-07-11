import pygame
import random
import serial.tools.list_ports
import datetime  #time: time.localtime([5])
import time

#parametrizar tudo
#deixar explicação

##necessario
#except electronic prototyping platform desconectou
#checar sempre se listas vazias - "Identified: PermissionError"

pygame.init()

x_size_of_window = 1200
y_size_of_window = 650
color_of_screen = (0,128,128)

window_of_visualization = pygame.display.set_mode((x_size_of_window, y_size_of_window))
window_of_visualization.fill(color_of_screen)

list_of_colors_for_lines = [(255,0,0),(0,255,0),(0,0,255)]
font = pygame.font.Font('freesansbold.ttf', 16)


def cursor_is_over(x, y, width, height, cursor_position):  # Determines if the mouse cursor position in tuple (x,y) is over
    if cursor_position[0] > x and cursor_position[0] < x + width:
        if cursor_position[1] > y and cursor_position[1] < y + height:
            return True
    return False

#A button for clicking purposes
class button():
    def __init__(self, window, color, x, y, width, height, text=''):
        self.window = window
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, outline=True): # Draw the Button
        if outline:
            pygame.draw.rect(self.window, (0,0,0), (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)


        pygame.draw.rect(self.window, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            text = font.render(self.text, True, (0, 0, 0))
            (self.window).blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def cursor_is_over(self, cursor_position): #Determines if the mouse cursor position in tuple (x,y) is over the button
        return (self.x,self.y,self.width,self.height,cursor_position)

#button for connecting with the electronic prototyping platform
connection_button = button(window_of_visualization,(255,0,0), 100, 100, 100, 20, "Connect")

#Information holder for individual graphs
class infograph():
    def __init__(self, name, step, color):
        self.name = name
        self.step = step
        self.color = color

        self.list_of_values = []

list_of_infographs = []
serial_COM_port = None

biggest_step = None
smallest_step = None

minimum_window_size = None

'''DEVE MOSTRAR SE FOI DESCONECTADO: "Disconnected"'''
#function for connecting with the electronic prototyping platform
def connect():
    global list_of_infographs
    global list_of_colors_for_lines
    global serial_COM_port

    #identifies available COM ports
    serial_COM_port = None
    ports = [comport.device for comport in serial.tools.list_ports.comports()]
    for i in range(len(ports)):
        try:
            selected_port = ports[i]
            serial_COM_port = serial.Serial(selected_port, 9600, timeout=3)
            time.sleep(3)
        except serial.SerialException:
            print("Identified: PermissionError")
        else:
            #connects with identified electronic prototyping platform
            serial_COM_port.reset_input_buffer()
            serial_COM_port.write("connect".encode())
            timing = time.time()
            while not serial_COM_port.in_waiting or (time.time() - timing < 3):
                pass
            if serial_COM_port.in_waiting:
                input = serial_COM_port.readline().decode('utf-8').strip()
                print(input)
                if(input == "begin"): #any other case: serial_COM_port = None
                    list_of_infographs = []
                    biggest_step = None
                    smallest_step = None
                    minimum_window_size = None
                    number = 0
                    while(1):
                        #receives names and steps for graphs
                        input = serial_COM_port.readline().decode('utf-8').strip()
                        print(input)
                        if(input == "end"):
                            break
                        lista_input = input.split(";")
                        name = lista_input[0]
                        step = float(lista_input[1])
                        number = number % len(list_of_colors_for_lines) #makes sure that the color is in the list
                        color = list_of_colors_for_lines[number]
                        list_of_infographs.append(infograph(name,step,color))
                        number += 1

                        if not biggest_step or step > biggest_step:
                            biggest_step = step
                        if not smallest_step or step < smallest_step:
                            smallest_step = step
                    minimum_window_size = 3 * biggest_step
                    break
            serial_COM_port = None


#cor_da_linha_vertical_de_informacao_do_graph = (255,255,255)
#cor_da_informacao_do_graph = (255,255,255)
graph_background_color = (0,0,0)

#graph for visualization
class graph():
    def __init__(self, window_of_visualization, x, y, width, height):
        self.window_of_visualization = window_of_visualization
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.initial_value = 0
        #self.size_of_frame = 10 * biggest_step
        self.list_of_infographs = [] #atualizado automaticamente no inicio do while(1) para selecionadas por checks

    #draws graph
    def draw(self):
        '''
        # scroll - tamanho_minimo_de_janela = 5
        # valor max, min para adicao de valor - considerar os que saíram, adicionados (pode ter q percorrer tudo de novo), posicao 0
        # pos processamento para bordas: y = ax + b, valor max e min
        # abreviação de nome
        # minimo tamanho do graph é o valor do menor passo
        # linhas verticais de graph - sensor de proximidade - fazer função
        # diversos eixos y
        # marcações por bolinhas nos eixos
        # ordem em que guias sao clicadas define mostragem de graph - ultima clicada na frente
        # botao direito desativa verticais
        # valores negativos precisam de variavel para menor valor - cuidado maior = menor
        '''

        pygame.draw.rect(self.window_of_visualization, graph_background_color, (self.x, self.y, self.width, self.height))


        '''listas_para_visualizar = []

        for i in range(len(lista_de_listas)):

            if len(lista_de_listas[i]) - 1 < size_of_frame:
                listas_para_visualizar.append(lista_de_listas[i])

            else:
                listas_para_visualizar.append(lista[len(lista) - size_of_frame: len(lista) + size_of_frame])

        lista_de_listas_de_coordenadas = []'''

        '''for i in range(len(lista_de_listas)): #evita divisao por 0
            if maior_valor > 0:
                multiplicador_vertical = proporcao* self.height / lista_de_maiores_valores[i]
            else:
                multiplicador_vertical = proporcao * self.height
            multiplicador_horizontal = self.width / (size_of_frame - 1)

            lista_de_listas_de_coordenadas.append([])

            for j in range(len(listas_para_visualizar[i])):
                coordx = self.x + fator_horizontal * j
                coordy = self.y - fator_vertical * lista_de_listas_de_coordenadas[i][j]
                lista_de_listas_de_coordenadas[i].append((x, y))'''

'''def graph(guia, lista, lista2, cursor_positionicao_inicial, origemx, origemy, widthdisplay, heightdisplay, janela,cursor_positionicao):   #gera graphs

    if len(lista) - 1 < tamanho:
        coord = lista
        coord2 = lista2
    else:
        coord = lista[cursor_positionicao_inicial: cursor_positionicao_inicial + janela]
        coord2 = lista2[cursor_positionicao_inicial: cursor_positionicao_inicial + janela]

    final = []
    final2 = []

    if maior_valor > 0:
        fator_vertical = (proporcao) * heightdisplay/maior_valor
    else:
        fator_vertical = (proporcao) * heightdisplay
    fator_horizontal = widthdisplay/(tamanho-1)


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
            if x - alcance < cursor_positionicao[0] and x + alcance > cursor_positionicao[0]:
                if y - alcance < cursor_positionicao[1] and y + alcance > cursor_positionicao[1]:
                    escreve_x = j
                    escreve_y = coord[j]

                    pygame.draw.rect(window_of_visualization,(100,100,100),(x,y,150,40))

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
            pygame.draw.lines(window_of_visualization, (255, 0, 0), False, final, 3)
        if check2.estate == True:
            pygame.draw.lines(window_of_visualization, (255, 0, 0), False, final2, 3)'''

    #.atualiza_valores
    #.define infographs
    #def informacao_mouse + linhas verticais


main_graph = graph(window_of_visualization,300,100,800,400)


running = True
while running:

    main_graph.draw()
    connection_button.draw(window_of_visualization)

    #if serial has received information
    if serial_COM_port and serial_COM_port.in_waiting:
        input = serial_COM_port.readline().decode('utf-8').strip()
        print(input)
        lista_input = input.split(";")
        #adds new information to respective infograph
        for i in range(len(list_of_infographs)):
            if lista_input[0] == list_of_infographs[i].name:
                list_of_infographs[i].list_of_values.append(float(lista_input[1]))


    for event in pygame.event.get():
        cursor_position = pygame.mouse.get_pos()
        button_pressed = pygame.mouse.get_pressed(3)

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and button_pressed == (1,0,0):

            #connects with electronic prototyping platform
            if connection_button.cursor_is_over(cursor_position) and not serial_COM_port:
                last_text = connection_button.text
                connection_button.text = "Connecting"
                connection_button.color = (255,255,0)
                connection_button.draw(window_of_visualization)
                pygame.display.update()
                connect()
                if serial_COM_port:
                    connection_button.color = (0,255,0)
                    connection_button.text = "Connected"
                else:
                    connection_button.color = (255,0,0)
                    if last_text != "Verify Link":
                        connection_button.text = "Verify Link"
                    else: #for visual confirmation
                        connection_button.text = "Error"

    pygame.display.update()

'''for i in range(len(list_of_infographs)):
    print(list_of_infographs[i].list_of_values)'''