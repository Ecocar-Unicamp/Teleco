import pygame
import random
import serial.tools.list_ports
import datetime
import time
import math
import os

# import classes

program_version = "BETA"  # 1.0

'''
comentários em inglês servem para explicar o código; em português, fazem um direcionamento de futuras mudanças
'''

'''
Marcadores:
#-#-#-#-#-#-#-#-#-#-#-# TítuloTópico #-#-#-#-#-#-#-#-#-#-#-#
#-_-_-_-_-_-_-_-_-_-_-# Tópico / Subtópico
# Explicação
#$%$%$%$%$%$%$%$%# Extra #$%$%$%$%$%$%$%$%#
'''

'''
#$%$%$%$%$%$%$%$%# Criação de executável com PyInstaller #$%$%$%$%$%$%$%$%#
ícone precisa estar formatado: https://www.icoconverter.com/
Abrir cmd e digitar:
cd /diretorio/do/arquivo
pyinstaller programa.py --onefile --noconsole --icon=/diretorio/icone.ico
encontar .exe na pasta dist, agregar dependencias em uma pasta e compactar para o envio
criar atalho
'''

'''
-- fazer até v1
desenhar necessário básico antes de conectar - depois de decidir a aparencia
parametrizar tudo!!!!
deixar explicação
-- futuros pontos de melhoria:
resizing: https://www.youtube.com/watch?v=edJZOQwrMKw&list=WL&index=5&t=233s&ab_channel=DaFluffyPotato
transpor classes e funções para arquivos separados
função única para desenhar grupamento de entidades, ex: botões
passos não estão sendo distanciados corretamente quando possuem OGs diferentes. é um problema do dummy apenas
'''

pygame.init()

# -#-#-#-#-#-#-#-#-#-#-# Program's base interface #-#-#-#-#-#-#-#-#-#-#-#
x_size_of_window = 1400
y_size_of_window = 650
color_of_screen = (0, 128, 128)

window_of_visualization = pygame.display.set_mode((x_size_of_window, y_size_of_window))  # the base display
window_of_visualization.fill(color_of_screen)

list_of_colors_for_lines = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255),
                            (0, 255, 255), (255, 127, 127), (127, 255, 127), (127, 127, 255)]

text_font = "Arial"
font = pygame.font.SysFont(text_font, 16)
minor_font = pygame.font.SysFont(text_font, 12)

pygame.display.set_caption("Telemetry Plotter")  # program's name
try:
    Icon = pygame.image.load("Logo_blurange.png")  # program's icon image
    pygame.display.set_icon(Icon)
except FileNotFoundError:
    print("No image for Logo found")

version_text = font.render("Telemetry Plotter  Version: " + str(program_version), False,
                           (0, 0, 0))  # program version info
version_text_position = (0, y_size_of_window - 16)
window_of_visualization.blit(version_text, version_text_position)


# -#-#-#-#-#-#-#-#-#-#-# Saving the data #-#-#-#-#-#-#-#-#-#-#-#
# Function creates a file to be used to save the data
def CreateArch(list_of_infographs):
    # Cheks for and create if needed folder for all saved data
    directory = "savedData"
    parent_directory = os.getcwd()
    path = os.path.join(parent_directory, directory)

    try:
        os.mkdir(path)

    except FileExistsError:
        print("savedData exists")
        # Creates folder named with current date and time
    finally:
        Current_Date = datetime.datetime.today()
        path = os.path.join(path, str(Current_Date).replace(":", ";"))
        try:
            os.mkdir(path)
        except FileExistsError:
            print("File already exists")
        # Creates files for each infograph
        for i in list_of_infographs:
            pathi = os.path.join(path, i.name)
            arch = open(pathi, "a")
            arch.write(i.name)
            arch.write("\nData collection started at: " + str(Current_Date.day) + str(Current_Date.month) + str(
                Current_Date.year) + str(Current_Date.hour) + str(Current_Date.minute) + str(
                Current_Date.second) + "\n")
            arch.write("time ")
            arch.write("\n")
            arch.close()

        return path

def Save_data(infograph, path):
    # open the file of the infograph and writes the new data
    pathi = os.path.join(path, infograph.name)
    arch = open(pathi, "a")
    arch.write(str(infograph.step * len(infograph.list_of_values)))
    arch.write(" ; ")
    arch.write(str(infograph.list_of_values[-1]))
    arch.write("\n")
    arch.close()


# -#-#-#-#-#-#-#-#-#-#-# Frequently used functions #-#-#-#-#-#-#-#-#-#-#-#
# Determines if the mouse cursor position in tuple (x,y) is over
def cursor_is_over(x, y, width, height, cursor_position):
    if cursor_position[0] > x and cursor_position[0] < x + width:
        if cursor_position[1] > y and cursor_position[1] < y + height:
            return True
    return False


# Converts a position old_value within the interval [old_a,old_b] to [new_a,new_b]
def proportional_conversion(old_value, old_range, new_range):
    if old_range == 0 or new_range == 0:
        return new_range / 2
    else:
        return (old_value * new_range / old_range)


# Converts a values with more than 3 digits to a string with at maximum 3 significant algarisms;
# if necessary, with scientific notation
def scientific_notation(value):
    converted = "{:#.3g}".format(value)
    if 'e' in converted:
        converted_list = converted.split("e")
        converted = converted_list[0] + "{0:+}".format(int(converted_list[1])) #removes "e" and 0
    return converted

# -#-#-#-#-#-#-#-#-#-#-# Button #-#-#-#-#-#-#-#-#-#-#-#
# -_-_-_-_-_-_-_-_-_-_-# Class
# A button for clicking purposes
class button():
    def __init__(self, window, color, x, y, width, height, text=''):
        self.window = window
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    # Draws the Button
    def draw(self):
        pygame.draw.rect(self.window, (0, 0, 0), (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(self.window, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            text = font.render(self.text, True, (0, 0, 0))
            (self.window).blit(text, (
                self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    # Determines if the mouse cursor position in tuple (x,y) is over the button
    def cursor_is_over(self, cursor_position):
        return cursor_is_over(self.x, self.y, self.width, self.height, cursor_position)


# -_-_-_-_-_-_-_-_-_-_-# Connection Button variables
# button for connecting with the electronic prototyping platform
message_connection_button_0 = "Connect"
message_connection_button_1 = "Connecting"
message_connection_button_2 = "Connected"
message_connection_button_30 = "Verify Link"
message_connection_button_31 = "Error"
message_connection_button_4 = "Disconnected"
connection_button_color = (255, 0, 0)
connection_button = button(window_of_visualization, connection_button_color, 100, 100, 100, 20,
                           message_connection_button_0)

# -_-_-_-_-_-_-_-_-_-_-# Live Data + Freezing Button variables
# button for freezing or defreezing the graph
message_freezing_button_0 = "Freeze"
message_freezing_button_1 = "Live Data"
freezing_button_color = (0, 0, 255)
freezing_button = button(window_of_visualization, freezing_button_color, 100, 140, 100, 20, message_freezing_button_0)

# -_-_-_-_-_-_-_-_-_-_-# New Tab Button variables
new_tab_button_color = (100, 100, 255)
new_tab_button = button(window_of_visualization, new_tab_button_color, 100, 200, 100, 20, "New Tab")


# -#-#-#-#-#-#-#-#-#-#-# Infograph Class #-#-#-#-#-#-#-#-#-#-#-#
# Information holder for individual graphs
class infograph():
    def __init__(self, name, step, color, unit):
        self.name = name
        self.step = step
        self.unit = unit
        self.color = color
        self.list_of_values = []


list_of_infographs = []

# -#-#-#-#-#-#-#-#-#-#-# Connection #-#-#-#-#-#-#-#-#-#-#-#
serial_COM_port = None
biggest_step = None
smallest_step_infograph = None
minimum_frame_size = None

dummy_infograph = False  # used for testing without Serial
final_timestamp_index = None # precision of function timestamp()


# function for connecting with the electronic prototyping platform
def connect():
    global list_of_infographs
    global list_of_colors_for_lines
    global serial_COM_port
    global biggest_step
    global smallest_step_infograph
    global minimum_frame_size
    global final_timestamp_index

    # identifies available COM ports
    ports = [comport.device for comport in serial.tools.list_ports.comports()]
    for i in range(len(ports)):
        try:
            selected_port = ports[i]
            serial_COM_port = serial.Serial(selected_port, 9600, timeout=3)
            time.sleep(3)
        except serial.SerialException:
            print("Identified: PermissionError")
        else:
            # connects with identified electronic prototyping platform
            serial_COM_port.reset_input_buffer()
            serial_COM_port.write("connect".encode())
            timing = time.time()
            while (time.time() - timing < 3):
                if serial_COM_port.in_waiting:
                    input = serial_COM_port.readline().decode('utf-8').strip()
                    print(input)
                    if (input == "begin"): # any other case: serial_COM_port = None
                        list_of_infographs = []
                        biggest_step = None
                        smallest_step_infograph = None
                        minimum_frame_size = None
                        dummy_infograph = False
                        final_timestamp_index = None
                        number = 0
                        timing = time.time()
                        while (1):
                            if time.time() - timing > 3:
                                serial_COM_port = None
                                list_of_infographs = []
                                biggest_step = None
                                smallest_step_infograph = None
                                minimum_frame_size = None
                                final_timestamp_index = None
                                return
                            # receives names and steps for graphs
                            input = serial_COM_port.readline().decode('utf-8').strip()
                            print(input)
                            if (input == "end"):
                                break
                            input_list = input.split(";")
                            name = input_list[0]
                            step = float(input_list[1])
                            unit = input_list[2]
                            number = number % len(list_of_colors_for_lines)  # makes sure that the color is in the list
                            color = list_of_colors_for_lines[number]
                            list_of_infographs.append(infograph(name, step, color, unit))

                            if not biggest_step or step > biggest_step:
                                biggest_step = step
                            if not smallest_step_infograph or step < smallest_step_infograph.step:
                                smallest_step_infograph = list_of_infographs[number]
                            number += 1

                        minimum_frame_size = 3 * biggest_step / smallest_step_infograph.step
                        final_timestamp_index = 9 - int(math.log10(smallest_step_infograph.step))
                        return
    serial_COM_port = None


# -#-#-#-#-#-#-#-#-#-#-# Graph #-#-#-#-#-#-#-#-#-#-#-#
# allows intuitive visualization of data

# -_-_-_-_-_-_-_-_-_-_-# Timestamp of the x axis
# returns a string based on the number of seconds timestamp. precision is based on the smallest step
def timestamp(seconds):
    converted = datetime.timedelta(seconds = seconds)
    if seconds < 3600:
        initial = 2
    else:
        initial = 0
    return str(converted)[initial:final_timestamp_index]


# -_-_-_-_-_-_-_-_-_-_-# Class
graph_info_color = (255, 255, 255)
graph_background_color = (0, 0, 0)
graph_second_background_color = (50, 50, 50)
info_dot_color = (120, 120, 255)

line_width = 1
info_line_width = 1
info_dot_radius = 3

axis_color = (200, 200, 200)
number_of_x_marks = 7 # don't set it to <= 0
number_of_y_marks = 5 # don't set it to <= 0

main_graph_x = 300
main_graph_y = 100
main_graph_width = 800
main_graph_height = 400

y_axis_lenght = 50

class graph():
    def __init__(self, window_of_visualization, x, y, width, height):
        self.window_of_visualization = window_of_visualization
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.initial_smallest_step_position_in_list = 0  # considering the smallest step
        self.size_of_frame = None  # number of points shown of the smallest step's list
        self.list_of_infographs = []  # updated automatically at the beggining of the loop

        self.current_list_of_coordinates = []
        self.current_list_of_values_initial_and_final_positions = []  # (x,y) for showing information

    def cursor_is_over(self, cursor_position):  # Determines if the mouse cursor position in tuple (x,y) is over the button
        return cursor_is_over(self.x, self.y, self.width, self.height, cursor_position)

    # draws the graph
    def draw(self):
        pygame.draw.rect(self.window_of_visualization, graph_second_background_color,
                         (main_graph_x - 4, main_graph_y - 4, main_graph_width + 8, main_graph_height + 88))
        pygame.draw.rect(self.window_of_visualization, graph_background_color,
                         (self.x, self.y, self.width, self.height))
        pygame.draw.rect(self.window_of_visualization, axis_color, (self.x, self.y + self.height, self.width, 40))
        pygame.draw.rect(self.window_of_visualization, color_of_screen,
                         (10, self.height - 130, 60, 2 + 20 * len(self.current_list_of_coordinates)))

        if serial_COM_port or dummy_infograph:
            # -_-_-_-_-_-_-_-_-_-_-# Axis base draw
            self.current_list_of_coordinates = []
            self.current_list_of_values_initial_and_final_positions = []
            smallest_step_x_graphic_step = self.width / (self.size_of_frame - 1)

            # -_-_-_-_-_-_-_-_-_-_-# Axis base draw / X axis
            time_step = None
            if number_of_x_marks == 1:
                time_step = (self.size_of_frame - 1) * smallest_step_infograph.step / (number_of_x_marks)
                graphic_step = self.width / (number_of_x_marks)
            else:
                time_step = (self.size_of_frame - 1) * smallest_step_infograph.step / (number_of_x_marks - 1)
                graphic_step = self.width / (number_of_x_marks - 1)
            for position in range(number_of_x_marks):
                pygame.draw.circle(self.window_of_visualization, info_dot_color,
                                   (self.x + position * graphic_step, self.y + self.height), info_dot_radius)
                text = minor_font.render(timestamp(self.initial_smallest_step_position_in_list * smallest_step_infograph.step +
                            position * time_step), True, (0, 0, 0))
                if position == 0:
                    (self.window_of_visualization).blit(text,
                                                        (self.x + position * graphic_step, self.y + self.height))
                elif position == number_of_x_marks - 1:
                    (self.window_of_visualization).blit(text, (
                    self.x + position * graphic_step - text.get_width(), self.y + self.height))
                else:
                    (self.window_of_visualization).blit(text, (
                    self.x + position * graphic_step - text.get_width() / 2, self.y + self.height))

            # -_-_-_-_-_-_-_-_-_-_-# Axis base draw / Y axis part 1
            pygame.draw.rect(self.window_of_visualization, axis_color,
                             (main_graph_x, self.y, len(selected_tab.selected_indexes) * y_axis_lenght, self.height))
            for i in range(len(selected_tab.selected_indexes)):
                color = None
                color = list_of_infographs[selected_tab.selected_indexes[i]].color
                pygame.draw.line(window_of_visualization, color, (main_graph_x + (i + 1 / 2) * y_axis_lenght, self.y),
                                 (main_graph_x + (i + 1 / 2) * y_axis_lenght, self.y + self.height), width=1)
                text = font.render((list_of_infographs[selected_tab.selected_indexes[i]].name)[:3], True, (0, 0, 0))
                (self.window_of_visualization).blit(text, (
                main_graph_x + (i + 1 / 2) * y_axis_lenght - text.get_width() / 2, self.y + self.height))

            graphic_step = self.height / (number_of_y_marks - 1)
            for position in range(number_of_y_marks):
                pygame.draw.line(window_of_visualization, (255, 255, 255),
                                 (main_graph_x, self.y + position * graphic_step),
                                 (self.x + self.width, self.y + position * graphic_step), width=1)

            # -_-_-_-_-_-_-_-_-_-_-# Information Presentation
            # defines what data will be worked with
            for i in range(len(self.list_of_infographs)):
                self.current_list_of_coordinates.append([])
                if len(self.list_of_infographs[i].list_of_values) > 1:

                    # -_-_-_-_-_-_-_-_-_-_-# Information Presentation / List Intervals
                    relative_step_proportion = smallest_step_infograph.step / self.list_of_infographs[i].step
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
                    final_position_in_list = int(relative_step_proportion * (
                            self.initial_smallest_step_position_in_list + self.size_of_frame - 1)) + 1

                    list_of_selected_values = self.list_of_infographs[i].list_of_values[
                                              initial_position_in_list: final_position_in_list]
                    self.current_list_of_values_initial_and_final_positions.append(
                        (initial_position_in_list, final_position_in_list))

                    lowest_value = min(list_of_selected_values)
                    highest_value = max(list_of_selected_values)

                    # -_-_-_-_-_-_-_-_-_-_-# Information Presentation / Y axis part 2
                    value_step = (highest_value - lowest_value) / (number_of_y_marks - 1)
                    graphic_step = self.height / (number_of_y_marks - 1)
                    for position in range(number_of_y_marks):
                        value = lowest_value + position * value_step
                        text = minor_font.render(scientific_notation(value), True, (0, 0, 0))
                        if position == 0:
                            (self.window_of_visualization).blit(text, (
                                main_graph_x + (1 / 2 + i) * y_axis_lenght - text.get_width() / 2,
                                self.y + self.height - position * graphic_step - text.get_height()))
                        elif position == number_of_y_marks - 1:
                            (self.window_of_visualization).blit(text, (
                                main_graph_x + (1 / 2 + i) * y_axis_lenght - text.get_width() / 2,
                                self.y + self.height - position * graphic_step))
                        else:
                            (self.window_of_visualization).blit(text, (
                                main_graph_x + (1 / 2 + i) * y_axis_lenght - text.get_width() / 2,
                                self.y + self.height - position * graphic_step - text.get_height() / 2))

                    # -_-_-_-_-_-_-_-_-_-_-# Information Presentation / Visual part
                    graphic_step = smallest_step_x_graphic_step / relative_step_proportion
                    initial_x_position = initial_position_in_list * graphic_step - self.initial_smallest_step_position_in_list * smallest_step_x_graphic_step

                    for j in range(len(list_of_selected_values)):
                        x_coordinate = self.x + initial_x_position + j * graphic_step
                        y_coordinate = self.y + self.height - proportional_conversion(
                            list_of_selected_values[j] - lowest_value, highest_value - lowest_value, self.height)

                        self.current_list_of_coordinates[i].append((x_coordinate, y_coordinate))

                    pygame.draw.lines(window_of_visualization, self.list_of_infographs[i].color, False,
                                      self.current_list_of_coordinates[i], line_width)

    # -_-_-_-_-_-_-_-_-_-_-# Additional Information
    def info(self, cursor_position):  # conditional if cursor_is_over graph
        point_distance = 1000000000
        aux = 0
        font3 = pygame.font.SysFont(text_font, 12)
        closest_points = []

        if len(self.current_list_of_coordinates) >= 1:
            if len(self.current_list_of_values_initial_and_final_positions) == len(self.current_list_of_coordinates):
                for i in range(len(self.current_list_of_coordinates)):
                    closest_points.append(0)
                    point_distance = 1000000000
                    aux = 0
                    for j in range(len(self.current_list_of_coordinates[i])):  # finds closest points to the cursor
                        aux = abs(cursor_position[0] - self.current_list_of_coordinates[i][j][0])
                        if aux < point_distance:
                            point_distance = aux
                            closest_points[i] = (
                            j, self.current_list_of_coordinates[i][j], self.list_of_infographs[i].color)

                pygame.draw.rect(self.window_of_visualization, (255, 255, 255), (
                    10, self.height - 130, 60, 2 + 20 * len(self.current_list_of_coordinates)))

                for i in range(len(closest_points)):  # gets the information for each point and prints it
                    info1 = font3.render(self.list_of_infographs[i].name + ":", True, (0, 0, 0))
                    info2 = font3.render(scientific_notation(self.list_of_infographs[i].list_of_values[closest_points[i][0] +
                                                              self.current_list_of_values_initial_and_final_positions[i][0]]), True, (0, 0, 0))
                    self.window_of_visualization.blit(info1, (10, self.height - 130 + (20 * i)))
                    self.window_of_visualization.blit(info2, (10, self.height - 120 + (20 * i)))
                    pygame.draw.circle(self.window_of_visualization, closest_points[i][2], closest_points[i][1],
                                       info_dot_radius)

        pygame.draw.line(self.window_of_visualization, graph_info_color, (cursor_position[0], self.y),
                         (cursor_position[0], self.y + self.height), info_line_width)
        pygame.draw.circle(self.window_of_visualization, info_dot_color, cursor_position, info_dot_radius)


main_graph = graph(window_of_visualization, main_graph_x, main_graph_y, main_graph_width, main_graph_height)

# -#-#-#-#-#-#-#-#-#-#-# Bar #-#-#-#-#-#-#-#-#-#-#-#
color_of_pointer = (0, 255, 0)
pointer_thickness = 2

class bar:
    def __init__(self, window, color, x, y, width, height):
        self.window = window
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self):
        pygame.draw.rect(self.window, self.color, (self.x, self.y, self.width, self.height), 0)

    def pointer(self, color, position_x, position_y, thickness):
        pygame.draw.rect(self.window, color,
                         (position_x - thickness, position_y + 23 - thickness, 5, self.height - thickness))

    def update_pointer(self):
        if smallest_step_infograph != None:
            pointer_pos = proportional_conversion(main_graph.initial_smallest_step_position_in_list,
                                                  len(smallest_step_infograph.list_of_values) - main_graph.size_of_frame,
                                                  main_graph.width - pointer_thickness)
            self.pointer(color_of_pointer, pointer_pos + main_graph.x, main_graph.y + main_graph.height + 30,
                         pointer_thickness)

    def cursor_is_over(self, cursor_position):  # Determines if the mouse cursor position in tuple (x,y) is over the bar
        return cursor_is_over(self.x, self.y, self.width, self.height, cursor_position)


main_bar = bar(window_of_visualization, (141, 141, 141), main_graph.x - pointer_thickness,
               main_graph.y + main_graph.height + 50, main_graph.width + 1.5 * pointer_thickness, 30)
pointer_pos = main_graph.x + main_graph.width - pointer_thickness

# -#-#-#-#-#-#-#-#-#-#-# Checkbox #-#-#-#-#-#-#-#-#-#-#-#
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

    def draw(self):
        pygame.draw.rect(self.window, (0,0,0), (self.x - 2, self.y - 2, self.size + 4, self.size + 4), 0)

        pygame.draw.rect(self.window, self.color, (self.x, self.y, self.size, self.size), 0)

        text = font.render(self.name, True, (0, 0, 0))
        (self.window).blit(text, (self.x + 40, self.y + (self.size / 2 - text.get_height() / 2)))

        if self.state:
            font2 = pygame.font.SysFont(text_font, int(1.5 * self.size))
            text = font2.render("X", True, (0, 0, 0))
            (self.window).blit(text, (
                self.x + (self.size / 2 - text.get_width() / 2), self.y + (self.size / 2 - text.get_height() / 2)))

    def cursor_is_over(self, cursor_position):
        return cursor_is_over(self.x, self.y, self.size, self.size, cursor_position)


# -#-#-#-#-#-#-#-#-#-#-# Last value box #-#-#-#-#-#-#-#-#-#-#-#
class last_value_box():
    def __init__(self, window, x, y, width, height, last_value):
        self.window = window

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.last_value = last_value

    def draw(self):
        if(self.last_value != None):
            pygame.draw.rect(self.window, (0, 0, 0), (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)
            pygame.draw.rect(self.window, (150, 150, 150), (self.x, self.y, self.width, self.height), 0)
            text = font.render(scientific_notation(self.last_value), True, (0, 0, 0))
            (self.window).blit(text, (
            self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))


# -#-#-#-#-#-#-#-#-#-#-# Tab #-#-#-#-#-#-#-#-#-#-#-#
tab_main_color = (0, 255, 0)
tab_secondary_color = (0, 150, 0)
tab_close_color = (255, 0, 0)

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

        self.close_x = x + width + 10
        self.close_y = y
        self.close_width = height
        self.close_height = height
        self.close_color = tab_close_color

        self.selected = selected
        self.checkboxes = []
        self.selected_indexes = []
        self.last_value_boxes = []
        for i in range(len(list_of_infographs)):
            self.selected_indexes.append(i)

        for i in range(len(self.selected_indexes)):
            self.checkboxes.append(checkbox(window_of_visualization, list_of_infographs[self.selected_indexes[i]].name,
                                            1200, 40 * i + 100, 20, True))
            self.last_value_boxes.append(last_value_box(window_of_visualization, 1300, 40 * i + 100, 70, 20, None))

    def draw(self):  # Draws the Button
        pygame.draw.rect(self.window, (0, 0, 0), (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)
        pygame.draw.rect(self.window, (0, 0, 0),
                         (self.close_x - 2, self.close_y - 2, self.close_width + 4, self.close_height + 4), 0)

        if self.selected:
            self.color = tab_secondary_color
        else:
            self.color = tab_main_color

        pygame.draw.rect(self.window, self.color, (self.x, self.y, self.width, self.height), 0)
        pygame.draw.rect(self.window, self.close_color,
                         (self.close_x, self.close_y, self.close_width, self.close_height), 0)
        font2 = pygame.font.SysFont(text_font, int(1.5 * self.close_height))
        text = font2.render("X", True, (0, 0, 0))
        (self.window).blit(text, (self.close_x + (self.close_width / 2 - text.get_width() / 2),
                                  self.y + (self.close_height / 2 - text.get_height() / 2)))

        if self.text != '':
            text = font.render(self.text, True, (0, 0, 0))
            (self.window).blit(text, (
                self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

        if self.selected:
            pygame.draw.rect(self.window, (100, 100, 100), (1150, 50, 200, 400), 0)
            for c in range(len(self.checkboxes)):
                self.checkboxes[c].draw()
            for i in range(len(self.last_value_boxes)):
                self.last_value_boxes[i].draw()

    def cursor_is_over(self,
                       cursor_position):  # Determines if the mouse cursor position in tuple (x,y) is over the button
        return cursor_is_over(self.x, self.y, self.width, self.height, cursor_position)

    def cursor_is_over_close(self, cursor_position):
        return cursor_is_over(self.close_x, self.close_y, self.close_width, self.close_height, cursor_position)


list_of_tabs = []
selected_tab = None

# -#-#-#-#-#-#-#-#-#-#-# Dummy Data Generator #-#-#-#-#-#-#-#-#-#-#-#
# for testing without serial, just uncomment this part
# do not try to connect the arduino when working with dummy, many bugs are not solved
'''
dummy_infograph = True
last_times = []
a = 0
list_of_infographs.append(infograph("D1", 0.5, list_of_colors_for_lines[0], "d1"))
list_of_infographs.append(infograph("D2", 1.5, list_of_colors_for_lines[1], "d2"))
list_of_infographs.append(infograph("D3", 0.5, list_of_colors_for_lines[2], "d3"))
list_of_infographs.append(infograph("D4", 0.1, list_of_colors_for_lines[3], "d4"))
list_of_infographs.append(infograph("D5", 1, list_of_colors_for_lines[4], "d5"))
list_of_infographs.append(infograph("D6", 2, list_of_colors_for_lines[5], "d6"))
for i in range(len(list_of_infographs)):
    last_times.append(0)
serial_COM_port = None
biggest_step = None
for i in range(len(list_of_infographs)):
    if not biggest_step or list_of_infographs[i].step > biggest_step:
        biggest_step = list_of_infographs[i].step
smallest_step_infograph = None
for i in range(len(list_of_infographs)):
    if not smallest_step_infograph or list_of_infographs[i].step < smallest_step_infograph.step:
        smallest_step_infograph = list_of_infographs[i]
minimum_frame_size = 3 * biggest_step / smallest_step_infograph.step
final_timestamp_index = 9 - int(math.log10(smallest_step_infograph.step))
main_graph.size_of_frame = 10 * minimum_frame_size
list_of_tabs.append(tab(window_of_visualization, 100, 240, 100, 20, "Tab 1", True))
selected_tab = list_of_tabs[0]
# y axis
main_graph.x += len(list_of_infographs) * y_axis_lenght
main_graph.width -= len(list_of_infographs) * y_axis_lenght
main_bar.x = main_graph.x
main_bar.width = main_graph.width
'''

# -#-#-#-#-#-#-#-#-#-#-# Program's Loop #-#-#-#-#-#-#-#-#-#-#-#
cursor_position = None
live_data = True
running = True

while running:
    # -_-_-_-_-_-_-_-_-_-_-# User interactives
    connection_button.draw()
    freezing_button.draw()
    new_tab_button.draw()
    pygame.draw.rect(window_of_visualization, (100, 100, 100), (90, 225, 150, 400),
                     0)  # precisa esconder guias apagadas
    for t in list_of_tabs:
        t.draw()

    # -_-_-_-_-_-_-_-_-_-_-# Data acquirement
    try:
        if serial_COM_port and serial_COM_port.in_waiting:  # if serial has received information
            input = serial_COM_port.readline().decode('utf-8').strip()
            print(input)
            input_list = input.split(";")
            # adds new information to respective infograph
            list_of_infographs[int(input_list[0])].list_of_values.append(float(input_list[1]))
            Save_data(list_of_infographs[int(input_list[0])], path_savedData)
    except serial.SerialException:
        print("Disconnected")
        serial_COM_port = None
        connection_button.color = (255, 0, 0)
        connection_button.text = message_connection_button_4
        main_graph.x = main_graph_x
        main_graph.width = main_graph_width
        main_bar.x = main_graph.x
        main_bar.width = main_graph.width
        main_graph.list_of_infographs = []
        main_graph.current_list_of_coordinates = []
        main_graph.current_list_of_values_initial_and_final_positions = []
        selected_tab = None
        list_of_tabs = []

    # $%$%$%$%$%$%$%$%# Dummy data #$%$%$%$%$%$%$%$%#
    if dummy_infograph:
        for i in range(len(list_of_infographs)):
            if (time.time() - last_times[i]) > list_of_infographs[i].step:
                last_times[i] = time.time()
                a += 0.05
                b = math.cos(a)
                if i == 0:
                    list_of_infographs[i].list_of_values.append(random.randint(0, 1))
                if i == 1:
                    list_of_infographs[i].list_of_values.append(100*b + random.randrange(-100000, 100000, 1))
                if i == 2:
                    list_of_infographs[i].list_of_values.append(b + math.cos(random.randrange(-1000, 1000, 1) / 300))
                if i == 3:
                    list_of_infographs[i].list_of_values.append(-b + math.acos(random.randrange(-1000, 1000, 1) / 1000))
                if i == 4:
                    list_of_infographs[i].list_of_values.append(b + 2 ** -random.randint(0, 10))
                if i == 5:
                    list_of_infographs[i].list_of_values.append(b + random.randint(1, 10) ** (-1))

    # -_-_-_-_-_-_-_-_-_-_-# User commands
    for event in pygame.event.get():
        cursor_position = pygame.mouse.get_pos()
        button_pressed = pygame.mouse.get_pressed(3)
        key_pressed = pygame.key.get_pressed()

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEWHEEL:
            if main_graph.size_of_frame:
                # proportional growth
                main_graph.size_of_frame += (-1) * event.y * (1 + int(main_graph.size_of_frame / 10))
                if main_graph.size_of_frame < minimum_frame_size:
                    main_graph.size_of_frame = minimum_frame_size

        if event.type == pygame.MOUSEBUTTONDOWN and button_pressed == (1, 0, 0):

            # -_-_-_-_-_-_-_-_-_-_-# User commands / Connect
            # connects with electronic prototyping platform
            if connection_button.cursor_is_over(cursor_position) and not serial_COM_port:
                last_text = connection_button.text
                connection_button.text = message_connection_button_1
                connection_button.color = (255, 255, 0)
                connection_button.draw()
                pygame.display.update()
                connect()
                path_savedData = CreateArch(list_of_infographs)
                if serial_COM_port:
                    connection_button.color = (0, 255, 0)
                    connection_button.text = message_connection_button_2
                    main_graph.size_of_frame = 10 * minimum_frame_size
                    list_of_tabs.append(tab(window_of_visualization, 100, 240, 100, 20, "Tab 1", True))
                    selected_tab = list_of_tabs[0]

                    # configurates the y axis
                    main_graph.x += len(list_of_infographs) * y_axis_lenght
                    main_graph.width -= len(list_of_infographs) * y_axis_lenght
                    main_bar.x = main_graph.x
                    main_bar.width = main_graph.width
                else:
                    connection_button.color = (255, 0, 0)
                    if last_text != message_connection_button_30:
                        connection_button.text = message_connection_button_30
                    else:  # for visual confirmation
                        connection_button.text = message_connection_button_31

            # -_-_-_-_-_-_-_-_-_-_-# User commands / Freezing button
            # freeze or defreeze the graph
            if freezing_button.cursor_is_over(cursor_position):
                if freezing_button.text == message_freezing_button_0:
                    freezing_button.text = message_freezing_button_1
                    live_data = False
                elif freezing_button.text == message_freezing_button_1:
                    freezing_button.text = message_freezing_button_0
                    live_data = True

            # -_-_-_-_-_-_-_-_-_-_-# User commands / Tab management
            # creates a new tab
            if new_tab_button.cursor_is_over(cursor_position) and len(list_of_tabs):
                list_of_tabs.append(tab(window_of_visualization, 100, list_of_tabs[-1].y + 40, 100, 20,
                                        "Tab " + str(len(list_of_tabs) + 1)))

            # checks if a tab is selected or closed
            for t in range(len(list_of_tabs)):
                if list_of_tabs[t].cursor_is_over(cursor_position):
                    selected_tab.selected = False
                    selected_tab = list_of_tabs[t]
                    selected_tab.selected = True
                    main_graph.x = main_graph_x + len(list_of_tabs[t].selected_indexes) * y_axis_lenght
                    main_graph.width = main_graph_width - len(list_of_tabs[t].selected_indexes) * y_axis_lenght
                    main_bar.x = main_graph.x
                    main_bar.width = main_graph.width
                    break
                if list_of_tabs[t].cursor_is_over_close(cursor_position) and len(list_of_tabs) > 1:
                    test = list_of_tabs[t]
                    del list_of_tabs[t]
                    if test.selected:
                        list_of_tabs[0].selected = True
                        selected_tab = list_of_tabs[0]
                    for j in range( len(list_of_tabs) - t):
                        list_of_tabs[t + j].text = "Tab " + str(t + j + 1)
                        list_of_tabs[t + j].y = list_of_tabs[t + j].y - 40
                        list_of_tabs[t + j].close_y = list_of_tabs[t + j].close_y - 40
                    break

            # -_-_-_-_-_-_-_-_-_-_-# User commands / Checkbox Management
            # checks if a checkbox is selected or deselected
            if selected_tab:
                for c in range(len(selected_tab.checkboxes)):
                    if selected_tab.checkboxes[c].cursor_is_over(cursor_position):
                        if selected_tab.checkboxes[c].state:
                            selected_tab.selected_indexes.remove(c)
                            main_graph.x -= y_axis_lenght
                            main_graph.width += y_axis_lenght
                        else:
                            selected_tab.selected_indexes.append(c)
                            main_graph.x += y_axis_lenght
                            main_graph.width -= y_axis_lenght
                        main_bar.x = main_graph.x
                        main_bar.width = main_graph.width
                        selected_tab.checkboxes[c].state = not selected_tab.checkboxes[c].state

            # -_-_-_-_-_-_-_-_-_-_-# User commands / Bar management
            # checks if user clicks the bar
            if smallest_step_infograph != None:
                if main_bar.cursor_is_over(cursor_position):
                    # updates values shown in graph based on click location
                    main_graph.initial_smallest_step_position_in_list = int(
                        proportional_conversion(cursor_position[0] - main_graph.x, main_graph.width,
                                                len(smallest_step_infograph.list_of_values) - main_graph.size_of_frame))
                    if main_graph.size_of_frame < len(smallest_step_infograph.list_of_values):
                        pointer_pos = proportional_conversion(main_graph.initial_smallest_step_position_in_list,
                                                              len(smallest_step_infograph.list_of_values) - main_graph.size_of_frame,
                                                              main_graph.width)  # updates pointer position based on click location
                    # freezes shown data
                    freezing_button.text = message_freezing_button_1
                    live_data = False

        # -_-_-_-_-_-_-_-_-_-_-# User commands / Displacement
        # displaces the graph
        if event.type == pygame.KEYDOWN:
            live_data = False
            freezing_button.text = message_freezing_button_1
            if event.key == pygame.K_LEFT:
                main_graph.initial_smallest_step_position_in_list -= 1
            if event.key == pygame.K_RIGHT:
                main_graph.initial_smallest_step_position_in_list += 1
            aovivo = False

    # displaces the graph
    if key_pressed[pygame.K_UP]:
        live_data = False
        freezing_button.text = message_freezing_button_1
        main_graph.initial_smallest_step_position_in_list += 1
    if key_pressed[pygame.K_DOWN]:
        live_data = False
        freezing_button.text = message_freezing_button_1
        main_graph.initial_smallest_step_position_in_list -= 1

    # -_-_-_-_-_-_-_-_-_-_-# Graph curves bug fixes
    # makes sure that when the size of frame is greater than the number of values, the initial position is set to 0
    if (serial_COM_port or dummy_infograph) and (
            live_data or (not live_data and len(smallest_step_infograph.list_of_values) <
                          main_graph.size_of_frame + main_graph.initial_smallest_step_position_in_list)):
        main_graph.initial_smallest_step_position_in_list = len(
            smallest_step_infograph.list_of_values) - main_graph.size_of_frame
        if main_graph.size_of_frame > len(smallest_step_infograph.list_of_values):
            main_graph.initial_smallest_step_position_in_list = 0

    # makes sure the position in the list of values is no less than 0
    if (serial_COM_port or dummy_infograph) and main_graph.initial_smallest_step_position_in_list < 0:
        main_graph.initial_smallest_step_position_in_list = 0

    # -_-_-_-_-_-_-_-_-_-_-# Drawing interface
    # draws graphs in order of selection
    main_graph.list_of_infographs = []
    if selected_tab:
        for index in selected_tab.selected_indexes:
            main_graph.list_of_infographs.append(list_of_infographs[index])

        # determines the last value and writes it in the box
        for i in range(len(selected_tab.last_value_boxes)):
            if len(list_of_infographs[i].list_of_values) > 1:
                selected_tab.last_value_boxes[i].last_value = round(list_of_infographs[i].list_of_values[-1], 2)
                selected_tab.last_value_boxes[i].draw()

    main_graph.draw()
    main_bar.draw()
    if main_graph.cursor_is_over(cursor_position):
        main_graph.info(cursor_position)

    # updates pointer position while more values are taken into account
    main_bar.update_pointer()

    pygame.display.update()
