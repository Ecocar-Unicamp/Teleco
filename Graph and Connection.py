import pygame
import random
import serial.tools.list_ports
import datetime  #time: time.localtime([5])
import time

#parametrizar tudo
#deixar explicação

#except electronic prototyping platform desconectou
#checar sempre se listas vazias - "Identified: PermissionError"
#ultimos valores  - pode ser ao lado das checks
#info tempo na barra
#fazer troca de cores dos botoes na chamada de draw e is over

pygame.init()

x_size_of_window = 1400
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
message_connection_button_0 = "Connect"
message_connection_button_1 = "Connecting"
message_connection_button_2 = "Connected"
message_connection_button_30 = "Verify Link"
message_connection_button_31 = "Error"
connection_button_color = (255,0,0)
connection_button = button(window_of_visualization,connection_button_color, 100, 100, 100, 20, message_connection_button_0)

#button for freezing or defreezing the graph
message_freezing_button_0 = "Freeze"
message_freezing_button_1 = "Live Data"
freezing_button_color = (0,0,255)
freezing_button = button(window_of_visualization,freezing_button_color,100,140,100,20, message_freezing_button_0)

new_tab_button_color = (100,100,255)
new_tab_button = button(window_of_visualization,new_tab_button_color,100,200,100,20, "New Tab")

'''fazer funão que faz draw de botoes; tambem pro resto'''

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
            input = None
            while (time.time() - timing < 3):#deixar mais simples
                if serial_COM_port.in_waiting:
                    input = serial_COM_port.readline().decode('utf-8').strip()
                    #print(input)
                    if (input == "begin"):
                        break
                    else:
                        input = None
            if input:
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
                        #print(input)
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

        self.current_list_of_coordinates = []
        self.current_list_of_values_initial_and_final_positions = []

    def cursor_is_over(self, cursor_position):  # Determines if the mouse cursor position in tuple (x,y) is over the button
        return cursor_is_over(self.x, self.y, self.width, self.height, cursor_position)

    #draws graph
    def draw(self):
        pygame.draw.rect(self.window_of_visualization, graph_second_background_color,(self.x - 4, self.y - 4, self.width + 8, self.height + 8))
        pygame.draw.rect(self.window_of_visualization, graph_background_color, (self.x, self.y, self.width, self.height))

        if serial_COM_port:
            self.current_list_of_coordinates = []
            self.current_list_of_values_initial_and_final_positions = []
            smallest_step_x_graphic_step = self.width/(self.size_of_frame - 1)

            for i in range(len(self.list_of_infographs)):
                self.current_list_of_coordinates.append([])
                if len(self.list_of_infographs[i].list_of_values) > 1:
                    '''
                    # conferir se todos os selfs precisam ser selfs ou algum outro dado precisa ser self
                    # conferir se nao generaliza coisa que se baseia na lista de infog recebida - smallest_step_infograph.step
                    # pos processamento para bordas: y = ax + b, valor max e min
                    # diversos eixos y: abreviação de nome
                    '''
                    '''CONFERIR SE NAO VAI SAIR PRA FORA DA JANELA'''
                    relative_step_proportion = smallest_step_infograph.step/self.list_of_infographs[i].step
                    list_of_selected_values = []
                    initial_position_in_list = None
                    final_position_in_list = None

                    if len(self.list_of_infographs[i].list_of_values) < self.size_of_frame * relative_step_proportion:
                        initial_position_in_list = 0
                    else:
                        initial_position_in_list = self.initial_smallest_step_position_in_list * relative_step_proportion
                        if int(initial_position_in_list) == initial_position_in_list:
                            initial_position_in_list = int(initial_position_in_list)
                        else:
                            initial_position_in_list = int(initial_position_in_list) + 1
                    final_position_in_list = int(relative_step_proportion * (self.initial_smallest_step_position_in_list + self.size_of_frame - 1)) + 1

                    list_of_selected_values = self.list_of_infographs[i].list_of_values[initial_position_in_list: final_position_in_list]
                    self.current_list_of_values_initial_and_final_positions.append((initial_position_in_list,final_position_in_list))

                    lowest_value = min(list_of_selected_values)
                    highest_value = max(list_of_selected_values)

                    graphic_step = smallest_step_x_graphic_step/ relative_step_proportion
                    initial_x_position = initial_position_in_list * graphic_step - self.initial_smallest_step_position_in_list * smallest_step_x_graphic_step

                    for j in range(len(list_of_selected_values)):

                        x_coordinate = self.x + initial_x_position + j * graphic_step
                        y_coordinate = self.y + self.height - proportional_conversion(list_of_selected_values[j] - lowest_value, highest_value - lowest_value, self.height)

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


checkbox_main_color = (53, 87, 28)

class checkbox:
    def __init__(self, window, name, x, y, size=20, state=False):
        self.window = window
        self.x = x
        self.y = y
        self.size = size
        self.color = checkbox_main_color

        self.name = name
        self.state = state

    def draw(self, outline=None):
        if outline:
            pygame.draw.rect(self.window, outline, (self.x - 2, self.y - 2, self.size + 4, self.size + 4), 0)

        pygame.draw.rect(self.window, self.color, (self.x, self.y, self.size, self.size), 0)

        text = font.render(self.name, True, (0, 0, 0))
        (self.window).blit(text, (self.x + 40, self.y + (self.size / 2 - text.get_height() / 2)))

        if self.state:
            font2 = pygame.font.SysFont('freesansbold.ttf',int(1.5 * self.size))  #######verificar se parametrizavel
            text = font2.render("X", True, (0, 0, 0))
            (self.window).blit(text, (self.x + (self.size / 2 - text.get_width() / 2), self.y + (self.size / 2 - text.get_height() / 2)))

    def cursor_is_over(self, cursor_position):
        return cursor_is_over(self.x, self.y, self.size, self.size, cursor_position)

    ##########################
    def is_over(self, pos):
        if self.x < pos[0] < self.x + self.size:
            if self.y < pos[1] < self.y + self.size:
                self.color = self.secondary_color #################permite a troca da cor nao diretamente no main
                return True
        self.color = self.main_color
        return False
    ##########################


tab_main_color = (0,255,0)
tab_secondary_color = (0,150,0)

# Class for the tabs of diferent infographs. The class holds an index that identifies the tab, a list of the infographs
# avilable and a list of checkboxes used to selecte wich infographs will be shown. The class has a function to create
# new tabs and a class to draw the contents of the tab
class tab:
    def __init__(self, window, x, y, width, height, text, selected=False):
        self.window = window
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.color = tab_main_color

        self.selected = selected
        self.checkboxes = []
        self.selected_names = []
        for i in range(len(list_of_infographs)):
            self.selected_names.append(list_of_infographs[i].name)

        for i in range(len(self.selected_names)):
            self.checkboxes.append(checkbox(window_of_visualization, self.selected_names[i],
                                            1200, 40 * i + 100, 20,True))#######################################

    def draw(self, outline=True): # Draw the Button
        if outline:
            pygame.draw.rect(self.window, (0,0,0), (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        if self.selected: #isso dá pra ser enxugado
            self.color = tab_secondary_color
        else:
            self.color = tab_main_color

        pygame.draw.rect(self.window, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            text = font.render(self.text, True, (0, 0, 0))
            (self.window).blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

        if self.selected:
            pygame.draw.rect(self.window, (100, 100, 100), (1150, 50, 200, 400), 0) #deixar em f do tamanho abaixo
            for c in range(len(self.checkboxes)):
                self.checkboxes[c].draw()

    '''def draw(self):
        if self.selected:
            for i in range(len(self.list_of_infographs)):
                self.checkboxes[i].draw(window, (0, 0, 0))
                if self.checkboxes[i].state:
                    if not self.list_of_infographs[i] in self.selected_infographs:
                        self.selected_infographs.append(self.list_of_infographs[i])
                elif not self.checkboxes[i].state:
                    if self.list_of_infographs[i] in self.selected_infographs:
                        self.selected_infographs.remove(self.list_of_infographs[i])'''

    def cursor_is_over(self, cursor_position):  # Determines if the mouse cursor position in tuple (x,y) is over the button
        return cursor_is_over(self.x, self.y, self.width, self.height, cursor_position)

list_of_tabs = []
selected_tab = None

#se x pressionado: list_of_tabs.remove(tal) - checar se tem ao menos uma, garantir que tem alguma selecionada



while running:

    connection_button.draw(window_of_visualization)
    freezing_button.draw(window_of_visualization)
    new_tab_button.draw(window_of_visualization)
    for t in list_of_tabs:
        t.draw(window_of_visualization)

    #if serial has received information
    # desconexão inesperada: serial.serialutil.SerialException: ClearCommError failed (PermissionError(13, 'O dispositivo não reconhece o comando.', None, 22))
    if serial_COM_port and serial_COM_port.in_waiting:
        input = serial_COM_port.readline().decode('utf-8').strip()
        #print(input)
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


        if event.type == pygame.MOUSEBUTTONDOWN and button_pressed == (1,0,0):
            #connects with electronic prototyping platform
            if connection_button.cursor_is_over(cursor_position) and not serial_COM_port:
                last_text = connection_button.text
                connection_button.text = message_connection_button_1
                connection_button.color = (255,255,0)
                connection_button.draw(window_of_visualization)
                pygame.display.update()
                connect()
                if serial_COM_port:
                    connection_button.color = (0,255,0)
                    connection_button.text = message_connection_button_2
                    main_graph.size_of_frame = 10 * minimum_frame_size #################condicional

                    list_of_tabs.append(tab(window_of_visualization, 100, 240, 100, 20, "Tab 1", True))###################################fazer mais simples
                    selected_tab = list_of_tabs[0]
                else:
                    connection_button.color = (255,0,0)
                    if last_text != message_connection_button_30:
                        connection_button.text = message_connection_button_30
                    else: #for visual confirmation
                        connection_button.text = message_connection_button_31

            if freezing_button.cursor_is_over(cursor_position): #ponderar tamanho do valor da lista
                if freezing_button.text == message_freezing_button_0:
                    freezing_button.text = message_freezing_button_1
                    live_data = False
                elif freezing_button.text == message_freezing_button_1:
                    freezing_button.text = message_freezing_button_0
                    live_data = True

            if new_tab_button.cursor_is_over(cursor_position) and len(list_of_tabs):
                list_of_tabs.append(tab(window_of_visualization,100,list_of_tabs[-1].y + 40,100,20,"Tab " + str(len(list_of_tabs) + 1)))

            for t in range(len(list_of_tabs)):
                if list_of_tabs[t].cursor_is_over(cursor_position):
                    selected_tab.selected = False
                    selected_tab = list_of_tabs[t]
                    selected_tab.selected = True

            if selected_tab:
                for c in range(len(selected_tab.checkboxes)):
                    if selected_tab.checkboxes[c].cursor_is_over(cursor_position):
                        print(selected_tab.checkboxes[c].state)
                        if selected_tab.checkboxes[c].state:
                            selected_tab.selected_names.remove(selected_tab.checkboxes[c].name)
                        else:
                            selected_tab.selected_names.append(selected_tab.checkboxes[c].name)
                        selected_tab.checkboxes[c].state = not selected_tab.checkboxes[c].state


            #pra cada guia ve se ta acima:
            #atualizar guia selecionada: main_graph.list_of_infographs = guia_selecionada.list_of_infographs

        if event.type == pygame.KEYDOWN:
            live_data = False
            freezing_button.text = message_freezing_button_1
            if event.key == pygame.K_LEFT: #pode passar
                main_graph.initial_smallest_step_position_in_list -= 1
            if event.key == pygame.K_RIGHT:
                main_graph.initial_smallest_step_position_in_list += 1
            aovivo = False

    if key_pressed[pygame.K_UP]: #conta como event?
        live_data = False
        freezing_button.text = message_freezing_button_1
        main_graph.initial_smallest_step_position_in_list += 1
    if key_pressed[pygame.K_DOWN]:
        live_data = False
        freezing_button.text = message_freezing_button_1
        main_graph.initial_smallest_step_position_in_list -= 1


    if serial_COM_port and (live_data or (not live_data and len(smallest_step_infograph.list_of_values) <
                     main_graph.size_of_frame + main_graph.initial_smallest_step_position_in_list)):
        main_graph.initial_smallest_step_position_in_list = len(smallest_step_infograph.list_of_values) - main_graph.size_of_frame
        if main_graph.size_of_frame > len(smallest_step_infograph.list_of_values):
            main_graph.initial_smallest_step_position_in_list = 0

    if serial_COM_port and main_graph.initial_smallest_step_position_in_list < 0:
        main_graph.initial_smallest_step_position_in_list = 0


    main_graph.list_of_infographs = []
    if selected_tab: #########################################simplificar
        for name in selected_tab.selected_names:
            for equals in list_of_infographs:
                if name == equals.name:
                    main_graph.list_of_infographs.append(equals)


    main_graph.draw()
    if main_graph.cursor_is_over(cursor_position):
        main_graph.info(cursor_position)

    pygame.display.update()
