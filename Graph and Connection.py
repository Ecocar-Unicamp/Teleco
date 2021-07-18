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

list_of_colors_for_lines = [(255,0,0),(0,255,0),(0,0,255),(255,255,0),(255,0,255),(0,255,255)]
font = pygame.font.Font('freesansbold.ttf', 16)


def cursor_is_over(x, y, width, height, cursor_position):  # Determines if the mouse cursor position in tuple (x,y) is over
    if cursor_position[0] > x and cursor_position[0] < x + width:
        if cursor_position[1] > y and cursor_position[1] < y + height:
            return True
    return False

#converts a position old_value within the interval [old_a,old_b] to [new_a,new_b]
def proportional_conversion(old_value, old_range, new_range):
    if old_range == 0 or new_range == 0:
        return new_range/2
    else:
        return (old_value * new_range/old_range)

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
        return cursor_is_over(self.x,self.y,self.width,self.height,cursor_position)

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
smallest_step_infograph = None

minimum_frame_size = None

'''DEVE MOSTRAR SE FOI DESCONECTADO: "Disconnected"'''
#function for connecting with the electronic prototyping platform
def connect():
    global list_of_infographs
    global list_of_colors_for_lines
    global serial_COM_port
    global biggest_step
    global smallest_step_infograph
    global minimum_frame_size

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
                    smallest_step_infograph = None
                    minimum_frame_size = None
                    number = 0
                    timing = time.time()
                    while(1):
                        if time.time() - timing > 3: ##################configurar restante dos resets
                            serial_COM_port = None
                            break
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

                        if not biggest_step or step > biggest_step:
                            biggest_step = step
                        if not smallest_step_infograph:
                            smallest_step_infograph = list_of_infographs[number]
                        elif step < smallest_step_infograph.step:
                            smallest_step_infograph = list_of_infographs[number]

                        number += 1

                    minimum_frame_size = 3 * biggest_step / smallest_step_infograph.step
                    break
            serial_COM_port = None


graph_info_color = (255,255,255)
graph_background_color = (0,0,0)
graph_second_background_color = (50,50,50)
info_dot_color = (120, 120, 255)

line_width = 1
info_line_width = 1
info_dot_radius = 3

#graph for visualization
class graph():
    def __init__(self, window_of_visualization, x, y, width, height):
        self.window_of_visualization = window_of_visualization
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.initial_smallest_step_position_in_list = 0 #considering the smallest step
        self.size_of_frame = None #number of points shown of the smallest step's list
        self.list_of_infographs = [] #atualizado automaticamente no inicio do while(1) para selecionadas por checks

        self.previous_highest_and_lowest_values_list = [] #tuple (highest value, lowest value, position)
        self.current_list_of_coordinates = []

    def cursor_is_over(self, cursor_position):  # Determines if the mouse cursor position in tuple (x,y) is over the button
        return cursor_is_over(self.x, self.y, self.width, self.height, cursor_position)

    #draws graph
    def draw(self):
        pygame.draw.rect(self.window_of_visualization, graph_second_background_color,(self.x - 4, self.y - 4, self.width + 8, self.height + 8))
        pygame.draw.rect(self.window_of_visualization, graph_background_color, (self.x, self.y, self.width, self.height))

        if serial_COM_port:
            #self.previous_highest_and_lowest_values_list = [] #prevenir computação extra
            self.current_list_of_coordinates = []
            smallest_step_x_graphic_step = self.width/(self.size_of_frame - 1)##############

            for i in range(len(self.list_of_infographs)):
                self.current_list_of_coordinates.append([])
                if len(self.list_of_infographs[i].list_of_values) > 1:##########******************
                    '''
                    # conferir se todos os selfs precisam ser selfs
                    # conferir se nao generaliza coisa que se baseia na lista de infog recebida - smallest_step_infograph.step
                    # verificar intervalo para valores saindo pra baixo
                    # verificar valor inicial x para nao menor step saindo para esquerda
                    # valor max, min para adicao de valor - considerar os que saíram, adicionados (pode ter q percorrer tudo de novo), posicao 0
                    # pos processamento para bordas: y = ax + b, valor max e min
                    # valores negativos precisam de variavel para menor valor - cuidado maior = menor
                    # minimo tamanho do graph é o valor do menor passo
                    # checagem size of frame > pos inicial + len lista
                    # diversos eixos y: abreviação de nome
                    '''
                    relative_step_proportion = smallest_step_infograph.step/self.list_of_infographs[i].step
                    list_of_y = []
                    initial_position_in_list = None
                    final_position_in_list = None

                    if len(self.list_of_infographs[i].list_of_values) <= self.size_of_frame * relative_step_proportion:
                        initial_position_in_list = 0
                        final_position_in_list = len(self.list_of_infographs[i].list_of_values)
                    else:#############################################conferir
                        initial_position_in_list = self.initial_smallest_step_position_in_list * relative_step_proportion
                        if int(initial_position_in_list) == initial_position_in_list:
                            initial_position_in_list = int(initial_position_in_list)
                            #final_position_in_list = int((self.initial_smallest_step_position_in_list + self.size_of_frame) * relative_step_proportion)
                        else:
                            #final_position_in_list = int(relative_step_proportion * (self.initial_smallest_step_position_in_list + self.size_of_frame) +
                                                         #(self.list_of_infographs[i].step - int(initial_position_in_list + 1) % initial_position_in_list))
                            initial_position_in_list = int(initial_position_in_list) + 1
                        final_position_in_list = int(relative_step_proportion * (self.initial_smallest_step_position_in_list + self.size_of_frame - 1)) + 1
                    list_of_y = self.list_of_infographs[i].list_of_values[initial_position_in_list: final_position_in_list]##################

                    if len(list_of_y) > 2:#############**********************
                        highest_value = None
                        lowest_value = None
                        for j in range(len(list_of_y)): ##############################prevenir computação extra
                            if not highest_value or list_of_y[j] > highest_value:
                                highest_value = list_of_y[j]
                            if not lowest_value or list_of_y[j] < lowest_value:
                                lowest_value = list_of_y[j]

                        y_difference = highest_value - lowest_value

                        graphic_step = smallest_step_x_graphic_step/ relative_step_proportion
                        initial_x_position = initial_position_in_list * graphic_step - self.initial_smallest_step_position_in_list * smallest_step_x_graphic_step

                        for j in range(len(list_of_y)): ########################## ref funcao de conversao de proporcao

                            x_coordinate = self.x + initial_x_position + j * graphic_step
                            y_coordinate = self.y + self.height - proportional_conversion(list_of_y[j] - lowest_value, y_difference, self.height)

                            self.current_list_of_coordinates[i].append((x_coordinate,y_coordinate))

                        pygame.draw.lines(window_of_visualization, self.list_of_infographs[i].color, False, self.current_list_of_coordinates[i], line_width)

    def info(self, cursor_position): #conditional if cursor_is_over graph
        pygame.draw.line(self.window_of_visualization,graph_info_color,(cursor_position[0],self.y),(cursor_position[0],self.y + self.height),info_line_width)

        '''for i in range(len(self.current_list_of_coordinates)):
            considered_coordinates = self.current_list_of_coordinates[i]
            index = 0'''
        coordinate = cursor_position#None
        #encontrar coordinate com chute por proportional conversion, incrementando index até (x,y)
        pygame.draw.circle(self.window_of_visualization,info_dot_color,coordinate,info_dot_radius)


main_graph = graph(window_of_visualization,300,100,800,400)

cursor_position = None
live_data = True
running = True

while running:

    connection_button.draw(window_of_visualization)

    #if serial has received information
    # desconexão inesperada: serial.serialutil.SerialException: ClearCommError failed (PermissionError(13, 'O dispositivo não reconhece o comando.', None, 22))
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
        key_pressed = pygame.key.get_pressed()

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEWHEEL:
            if main_graph.size_of_frame:
                main_graph.size_of_frame += (-1) * event.y * (1 + int(main_graph.size_of_frame/10)) #proportional growth
                if main_graph.size_of_frame < minimum_frame_size:
                    main_graph.size_of_frame = minimum_frame_size
            print(main_graph.size_of_frame)


        '''if event.type == pygame.KEYDOWN:
            live_data = False
            if event.key == pygame.K_LEFT: #pode passar
                main_graph.initial_smallest_step_position_in_list -= 1
            if event.key == pygame.K_RIGHT:
                main_graph.initial_smallest_step_position_in_list += 1
            aovivo = False
    
        if key_pressed[pygame.K_UP]: #conta como event?
            live_data = False
            main_graph.initial_smallest_step_position_in_list += 1
        if key_pressed[pygame.K_DOWN]:
            live_data = False
            main_graph.initial_smallest_step_position_in_list -= 1'''


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
                    main_graph.size_of_frame = 10 * minimum_frame_size #################condicional
                else:
                    connection_button.color = (255,0,0)
                    if last_text != "Verify Link":
                        connection_button.text = "Verify Link"
                    else: #for visual confirmation
                        connection_button.text = "Error"

    if serial_COM_port and (live_data or (not live_data and len(main_graph.list_of_infographs[smallest_step_index].list_of_values) <
                     main_graph.size_of_frame + main_graph.initial_smallest_step_position_in_list)):
        main_graph.initial_smallest_step_position_in_list = len(smallest_step_infograph.list_of_values) - main_graph.size_of_frame
        if main_graph.size_of_frame > len(smallest_step_infograph.list_of_values):
            main_graph.initial_smallest_step_position_in_list = 0

    if serial_COM_port and main_graph.initial_smallest_step_position_in_list < 0:
        main_graph.initial_smallest_step_position_in_list = 0


    main_graph.list_of_infographs = list_of_infographs #substituir por selecionados
    main_graph.draw()
    if main_graph.cursor_is_over(cursor_position):
        main_graph.info(cursor_position)

    pygame.display.update()
