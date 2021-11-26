import pygame
import random
import serial.tools.list_ports
import datetime
import time
import math
import os

# This code was made in 2020 - 2021 by Ecocar UNICAMP
# Authors: Daniel Carvalho Frulane de Souza, Nuno Kuschnaroff Barbosa,
# Guilherme Magalhães Soares and Igor Oura Belieri

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
parametrizar tudo!!!!
deixar explicação
-- futuros pontos de melhoria:
resizing: https://www.youtube.com/watch?v=edJZOQwrMKw&list=WL&index=5&t=233s&ab_channel=DaFluffyPotato
transpor classes e funções para arquivos separados
caso tenhamos um membro daltonico, reavaliar cores
passos não estão sendo distanciados corretamente quando possuem OGs diferentes. é um problema do dummy apenas
'''

pygame.init()

# -#-#-#-#-#-#-#-#-#-#-# Program's base interface #-#-#-#-#-#-#-#-#-#-#-#
x_size_of_window = 1400
y_size_of_window = 700
color_of_screen = (40, 40, 40)

try:
    icon = pygame.image.load('Logo TelEco 32x32.png')  # program's icon image
    pygame.display.set_icon(icon)
except FileNotFoundError:
    print("No image for Logo found")

window_of_visualization = pygame.display.set_mode((x_size_of_window, y_size_of_window))  # the base display
window_of_visualization.fill(color_of_screen)

list_of_colors_for_lines = [(248, 82, 82), (97, 205, 97), (70, 118, 206), (255, 255, 105),
                            (48, 228, 228), (255, 152, 82), (127, 255, 127), (127, 127, 255)]

text_font = "Arial"
font = pygame.font.SysFont(text_font, 16)
minor_font = pygame.font.SysFont(text_font, 12)

pygame.display.set_caption("Telemetry Plotter")  # program's name

version_text = font.render("Telemetry Plotter  Version: " + str(program_version), False,
                           (200, 200, 200))  # program version info
version_text_position = (4, y_size_of_window - 20)
window_of_visualization.blit(version_text, version_text_position)

information_box_x = 170
information_box_y = 480


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
        converted = converted_list[0] + "{0:+}".format(int(converted_list[1]))  # removes "e" and 0
    return converted

# -_-_-_-_-_-_-_-_-_-_-# Timestamp of the x axis
# returns a string based on the number of seconds timestamp. precision is based on the smallest step
def timestamp(seconds):
    converted = datetime.timedelta(seconds=seconds)
    if seconds < 3600:
        initial = 2
    else:
        initial = 0
    return str(converted)[initial:final_timestamp_index]

# -#-#-#-#-#-#-#-#-#-#-# Button #-#-#-#-#-#-#-#-#-#-#-#
# -_-_-_-_-_-_-_-_-_-_-# Class
# A button for clicking purposes
class button():
    def __init__(self, window, color, x, y, width, height, text=''):
        self.window = window
        self.color = color
        self.secondary_color = tuple(map(lambda i: i - 20 if i>20 else 0, color))
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

        # Draws the Button

    def draw(self, cursor_position):
        color_used = self.color
        self.secondary_color = tuple(map(lambda i: i - 20 if i>20 else 0, self.color))
        if self.cursor_is_over(cursor_position):
            color_used = self.secondary_color

        pygame.draw.rect(self.window, (0, 0, 0), (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)
        pygame.draw.rect(self.window, color_used, (self.x, self.y, self.width, self.height), 0)

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
connection_button_color = (97, 205, 97)
connection_button_color1 = (255, 255, 105)
connection_button_color2 = (248, 82, 82)
connection_button = button(window_of_visualization, connection_button_color, 30, 30, 100, 20,
                           message_connection_button_0)

# -_-_-_-_-_-_-_-_-_-_-# Live Data + Freezing Button variables
# button for freezing or defreezing the graph
message_freezing_button_0 = "Freeze"
message_freezing_button_1 = "Live Data"
freezing_button_color = (100, 100, 100)
freezing_button = button(window_of_visualization, freezing_button_color, 30, 60, 100, 20, message_freezing_button_0)
live_data = True

# -_-_-_-_-_-_-_-_-_-_-# Set Window Button variables
# button for setting the window size as the lenghth of the list of values
set_window_button_color = (100, 100, 100)
set_window_button = button(window_of_visualization, set_window_button_color, 30, 90, 100, 20, "Set Window")

# -_-_-_-_-_-_-_-_-_-_-# Change View Button variables
# button for freezing or defreezing the graph
message_change_view_button_0 = "Local View"
message_change_view_button_1 = "Global View"
change_view_button_color = (100, 100, 100)
change_view_button = button(window_of_visualization, change_view_button_color, 30, 120, 100, 20,
                            message_change_view_button_0)
local_view = True

# -_-_-_-_-_-_-_-_-_-_-# New Tab Button variables
new_tab_button_color = (100, 100, 100)
new_tab_button = button(window_of_visualization, new_tab_button_color, 30, 150, 100, 20, "New Tab")
max_number_of_tabs = 10


def draws_buttons(cursor_position):
    connection_button.draw(cursor_position)
    freezing_button.draw(cursor_position)
    new_tab_button.draw(cursor_position)
    set_window_button.draw(cursor_position)
    change_view_button.draw(cursor_position)


# -#-#-#-#-#-#-#-#-#-#-# Infograph Class #-#-#-#-#-#-#-#-#-#-#-#
# Information holder for individual graphs
class infograph():
    def __init__(self, name, step, color, unit, alert_higher = None, alert_lower = None):
        self.name = name
        self.step = step
        self.unit = unit
        self.color = color
        self.list_of_values = []
        self.highest_global_value = None
        self.lowest_global_value = None
        self.alert_higher = alert_higher
        self.alert_lower = alert_lower

alert_time_on_screen = 1 # seconds
list_of_infographs = []

# -#-#-#-#-#-#-#-#-#-#-# Connection #-#-#-#-#-#-#-#-#-#-#-#
serial_COM_port = None
biggest_step = None
smallest_step_infograph = None
minimum_frame_size = None

dummy_infograph = False  # used for testing without Serial
final_timestamp_index = None  # precision of function timestamp()


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
                    if (input == "begin"):  # any other case: serial_COM_port = None
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
                            alert_higher = input_list[3]
                            if alert_higher == "":
                                alert_higher = None
                            else:
                                alert_higher = float(alert_higher)
                            alert_lower = input_list[4]
                            if alert_lower == "":
                                alert_lower = None
                            else:
                                alert_lower = float(alert_lower)
                            number = number % len(list_of_colors_for_lines)  # makes sure that the color is in the list
                            color = list_of_colors_for_lines[number]
                            list_of_infographs.append(infograph(name, step, color, unit, alert_higher, alert_lower))

                            if not biggest_step or step > biggest_step:
                                biggest_step = step
                            if not smallest_step_infograph or step < smallest_step_infograph.step:
                                smallest_step_infograph = list_of_infographs[number]
                            number += 1

                        minimum_frame_size = 3 * biggest_step / smallest_step_infograph.step
                        final_timestamp_index = 10 - int(math.log10(smallest_step_infograph.step))
                        return
    serial_COM_port = None


# -#-#-#-#-#-#-#-#-#-#-# Graph #-#-#-#-#-#-#-#-#-#-#-#
# allows intuitive visualization of data

# -_-_-_-_-_-_-_-_-_-_-# Class
graph_info_color = (255, 255, 255)
graph_background_color = (0, 0, 0)
graph_second_background_color = (50, 50, 50)
info_dot_color = (120, 120, 255)

line_width = 2
info_line_width = 1
info_dot_radius = 3

axis_color = (200, 200, 200)
number_of_x_marks = 7  # don't set it to <= 0
number_of_y_marks = 5  # don't set it to <= 0

main_graph_x = 175
main_graph_y = 30
main_graph_width = 1200
main_graph_height = 360

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

    def cursor_is_over(self,
                       cursor_position):  # Determines if the mouse cursor position in tuple (x,y) is over the button
        return cursor_is_over(self.x, self.y, self.width, self.height, cursor_position)

    # draws the graph
    def draw(self):
        pygame.draw.rect(self.window_of_visualization, graph_second_background_color,
                         (main_graph_x - 4, main_graph_y - 4, main_graph_width + 8, main_graph_height + 88))
        pygame.draw.rect(self.window_of_visualization, graph_background_color,
                         (self.x, self.y, self.width, self.height))
        pygame.draw.rect(self.window_of_visualization, axis_color, (self.x, self.y + self.height, self.width, 40))

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
                pygame.draw.line(self.window_of_visualization, graph_info_color,
                                 (self.x + position * graphic_step, self.y),
                                 (self.x + position * graphic_step, self.y + self.height), info_line_width)
                text = minor_font.render(
                    timestamp(self.initial_smallest_step_position_in_list * smallest_step_infograph.step +
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
                             (self.x + self.width, self.y, len(selected_tab.selected_indexes) * y_axis_lenght, self.height))
            for i in range(len(selected_tab.selected_indexes)):
                color = None
                color = list_of_infographs[selected_tab.selected_indexes[i]].color
                pygame.draw.line(window_of_visualization, color, (self.x + self.width + (i + 1 / 2) * y_axis_lenght, self.y),
                                 (self.x + self.width + (i + 1 / 2) * y_axis_lenght, self.y + self.height), width=1)
                text = font.render((list_of_infographs[selected_tab.selected_indexes[i]].name)[:4], True, axis_color)
                (self.window_of_visualization).blit(text, (
                    self.x + self.width + (i + 1 / 2) * y_axis_lenght - text.get_width() / 2, self.y + self.height + 5))

            graphic_step = self.height / (number_of_y_marks - 1)
            for position in range(number_of_y_marks):
                pygame.draw.line(window_of_visualization, graph_info_color,
                                 (self.x, self.y + position * graphic_step),
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

                    # -_-_-_-_-_-_-_-_-_-_-# Information Presentation / Y axis part 2
                    if local_view:
                        lowest_value = min(list_of_selected_values)
                        highest_value = max(list_of_selected_values)
                        value_step = (highest_value - lowest_value) / (number_of_y_marks - 1)
                    else:
                        value_step = (self.list_of_infographs[i].highest_global_value - self.list_of_infographs[
                            i].lowest_global_value) / (number_of_y_marks - 1)
                    graphic_step = self.height / (number_of_y_marks - 1)
                    for position in range(number_of_y_marks):
                        if local_view:
                            value = lowest_value + position * value_step
                        else:
                            value = self.list_of_infographs[i].lowest_global_value + position * value_step
                        text = minor_font.render(scientific_notation(value), True, (0, 0, 0))
                        if position == 0:
                            (self.window_of_visualization).blit(text, (
                                self.x + self.width + (1 / 2 + i) * y_axis_lenght - text.get_width() / 2,
                                self.y + self.height - position * graphic_step - text.get_height()))
                        elif position == number_of_y_marks - 1:
                            (self.window_of_visualization).blit(text, (
                                self.x + self.width + (1 / 2 + i) * y_axis_lenght - text.get_width() / 2,
                                self.y + self.height - position * graphic_step))
                        else:
                            (self.window_of_visualization).blit(text, (
                                self.x + self.width + (1 / 2 + i) * y_axis_lenght - text.get_width() / 2,
                                self.y + self.height - position * graphic_step - text.get_height() / 2))

                    # -_-_-_-_-_-_-_-_-_-_-# Information Presentation / Visual part
                    graphic_step = smallest_step_x_graphic_step / relative_step_proportion
                    initial_x_position = initial_position_in_list * graphic_step - self.initial_smallest_step_position_in_list * smallest_step_x_graphic_step

                    for j in range(len(list_of_selected_values)):
                        x_coordinate = self.x + initial_x_position + j * graphic_step
                        if local_view:
                            y_coordinate = self.y + self.height - proportional_conversion(
                                list_of_selected_values[j] - lowest_value, highest_value - lowest_value, self.height)
                        else:
                            y_coordinate = self.y + self.height - proportional_conversion(
                                list_of_selected_values[j] - self.list_of_infographs[i].lowest_global_value,
                                self.list_of_infographs[i].highest_global_value - self.list_of_infographs[
                                    i].lowest_global_value, self.height)

                        self.current_list_of_coordinates[i].append((x_coordinate, y_coordinate))

                    pygame.draw.lines(window_of_visualization, self.list_of_infographs[i].color, False,
                                      self.current_list_of_coordinates[i], line_width)

    # -_-_-_-_-_-_-_-_-_-_-# Additional Information
    def info(self, cursor_position):  # conditional if cursor_is_over graph
        point_distance = None
        aux = 0
        font3 = pygame.font.SysFont(text_font, 12)
        closest_points = []

        if len(self.current_list_of_coordinates) and len(self.current_list_of_values_initial_and_final_positions) == len(self.current_list_of_coordinates):
            info_box_text2 = font.render("Cursor", True, (200, 200, 200))
            self.window_of_visualization.blit(info_box_text2, (information_box_x + 250, information_box_y + 3))
            incrementor = 0
            for index in selected_tab.selected_indexes:
                closest_points.append(0)
                point_distance = None
                aux = 0
                for j in range(len(self.current_list_of_coordinates[incrementor])):  # finds closest points to the cursor
                    aux = abs(cursor_position[0] - self.current_list_of_coordinates[incrementor][j][0])
                    if point_distance == None or aux < point_distance:
                        point_distance = aux
                        closest_points[incrementor] = (j, self.current_list_of_coordinates[incrementor][j], self.list_of_infographs[incrementor].color)
                pygame.draw.circle(self.window_of_visualization, closest_points[incrementor][2], closest_points[incrementor][1],
                                   info_dot_radius)

                info = minor_font.render(
                scientific_notation(list_of_infographs[index].list_of_values[closest_points[incrementor][0] +
                                    self.current_list_of_values_initial_and_final_positions[incrementor][0]]), True, (200, 200, 200))
                self.window_of_visualization.blit(info, (information_box_x + 275 - (info.get_width() / 2),
                                                         (20 * index) + (information_box_y + 30) - (
                                                                 info.get_height() / 2)))
                incrementor += 1

            info_box_text3 = font.render("Time", True, (200, 200, 200))
            self.window_of_visualization.blit(info_box_text3, (information_box_x + 330, information_box_y + 3))
            time_info = minor_font.render(timestamp(self.initial_smallest_step_position_in_list * smallest_step_infograph.step + (cursor_position[0] - self.x)*(((self.size_of_frame - 1) * smallest_step_infograph.step)/self.width)), True, (200, 200, 200))
            self.window_of_visualization.blit(time_info, (information_box_x + 350 - (time_info.get_width() / 2), (information_box_y + 30) - (time_info.get_height() / 2)))
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
    def __init__(self, window, infog, x, y, size=20, state=False):
        self.window = window
        self.x = x
        self.y = y
        self.size = size
        self.color = checkbox_main_color

        self.name = infog.name
        self.text_color = infog.color
        self.unit = infog.unit
        self.state = state

    def draw(self):
        pygame.draw.rect(self.window, (0, 0, 0), (self.x - 2, self.y - 2, self.size + 4, self.size + 4), 0)

        pygame.draw.rect(self.window, self.color, (self.x, self.y, self.size, self.size), 0)

        text = font.render(self.name[:11] + " [" + self.unit[:4] + "]", True, self.text_color)
        (self.window).blit(text, (self.x + (self.size + 10), self.y + (self.size / 2 - text.get_height() / 2)))

        if self.state:
            font2 = pygame.font.SysFont(text_font, int(1.5 * self.size))
            text = font2.render("X", True, (0, 0, 0))
            (self.window).blit(text, (
                self.x + (self.size / 2 - text.get_width() / 2), self.y + (self.size / 2 - text.get_height() / 2)))

    def cursor_is_over(self, cursor_position):
        return cursor_is_over(self.x, self.y, self.size, self.size, cursor_position)


# -#-#-#-#-#-#-#-#-#-#-# Last value box #-#-#-#-#-#-#-#-#-#-#-#
class last_value_box():
    def __init__(self, window, x, y, width, height):
        self.window = window

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.last_value = None

        self.show_alert_values_times = 0

    def draw(self):
        if (self.last_value != None):
            color = (200, 200, 200)
            if self.show_alert_values_times > 0:
                color = (248, 42, 42)
                self.show_alert_values_times -= 1
            text = minor_font.render(scientific_notation(self.last_value), True, color)
            (self.window).blit(text, (
                self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))


# -#-#-#-#-#-#-#-#-#-#-# Tab #-#-#-#-#-#-#-#-#-#-#-#
tab_main_color = (100, 100, 100)  # mudar
tab_secondary_color = (60, 60, 60)
tab_close_color = (248, 82, 82)
values_table_X = 1105
values_table_Y = 90


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
            self.checkboxes.append(checkbox(window_of_visualization, list_of_infographs[self.selected_indexes[i]],
                                            information_box_x + 5, 20 * i + information_box_y + 20, 15, True))
            self.last_value_boxes.append(
                last_value_box(window_of_visualization, information_box_x + 165, (20 * i) + (information_box_y + 20), 70,20))

    def draw(self, cursor_position):  # Draws the tab
        pygame.draw.rect(self.window, (0, 0, 0), (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)
        pygame.draw.rect(self.window, (0, 0, 0),
                         (self.close_x - 2, self.close_y - 2, self.close_width + 4, self.close_height + 4), 0)

        used_color = self.color
        if self.selected:
            used_color = tab_secondary_color
        elif self.cursor_is_over(cursor_position):
            used_color = tuple(map(lambda i: i - 20, self.color))

        used_close_color = self.close_color
        if self.cursor_is_over_close(cursor_position):
            used_close_color = tuple(map(lambda i: i - 20, self.close_color))

        pygame.draw.rect(self.window, used_color, (self.x, self.y, self.width, self.height), 0)
        pygame.draw.rect(self.window, used_close_color,
                         (self.close_x, self.close_y, self.close_width, self.close_height), 0)
        font2 = pygame.font.SysFont(text_font, int(1.5 * self.close_height))
        text = font2.render("X", True, (0, 0, 0))
        (self.window).blit(text, (self.close_x + (self.close_width / 2 - text.get_width() / 2),
                                  self.y + (self.close_height / 2 - text.get_height() / 2)))

        if self.text != '':
            text = font.render(self.text[:10], True, (0, 0, 0))
            (self.window).blit(text, (
                self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

        if self.selected:
            pygame.draw.rect(self.window, (50, 50, 50),
                             (information_box_x, information_box_y, 400, 10 * len(self.checkboxes) + 80), 0)
            info_box_text1 = font.render("Last", True, (200, 200, 200))
            self.window.blit(info_box_text1, (information_box_x + 180, information_box_y+3))
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
tab_number = 1
file_name = "predefined tabs.txt"

# -#-#-#-#-#-#-#-#-#-#-# Dummy Data Generator #-#-#-#-#-#-#-#-#-#-#-#
# for testing without serial, just uncomment this part
# do not attempt to connect the arduino when working with dummy, many bugs are not solved
'''
dummy_infograph = True
last_times = []
a = 0
list_of_infographs.append(infograph("D1", 0.5, list_of_colors_for_lines[0], "d1", 500, 0))
list_of_infographs.append(infograph("D2", 1.5, list_of_colors_for_lines[1], "d2"))
list_of_infographs.append(infograph("D3", 0.5, list_of_colors_for_lines[2], "d3"))
list_of_infographs.append(infograph("D4", 0.1, list_of_colors_for_lines[3], "d4", 1.5))
list_of_infographs.append(infograph("D5", 1, list_of_colors_for_lines[4], "d5", None, 10000))
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
final_timestamp_index = 10 - int(math.log10(smallest_step_infograph.step))
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
running = True

while running:

    # -_-_-_-_-_-_-_-_-_-_-# Data acquirement
    try:
        if serial_COM_port and serial_COM_port.in_waiting:  # if serial has received information
            input = serial_COM_port.readline().decode('utf-8').strip()
            print(input)
            input_list = input.split(";")
            index = int(input_list[0])
            value = float(input_list[1])
            # adds new information to respective infograph
            list_of_infographs[index].list_of_values.append(value)
            Save_data(list_of_infographs[index], path_savedData)
            # calculates new global highest and lowest
            if list_of_infographs[index].highest_global_value == None or list_of_infographs[
                index].highest_global_value < value:
                list_of_infographs[index].highest_global_value = value
            if list_of_infographs[index].lowest_global_value == None or list_of_infographs[
                index].lowest_global_value > value:
                list_of_infographs[index].lowest_global_value = value
    except (ValueError, serial.SerialException):
        print("Disconnected")
        serial_COM_port = None
        connection_button.color = connection_button_color2
        connection_button.text = message_connection_button_4
        main_graph.x = main_graph_x
        main_graph.width = main_graph_width
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
                    value = random.randint(0, 1)
                if i == 1:
                    value = 100 * b + random.randrange(-100000, 100000, 1)
                if i == 2:
                    value = b + math.cos(random.randrange(-1000, 1000, 1) / 300)
                if i == 3:
                    value = -b + math.acos(random.randrange(-1000, 1000, 1) / 1000)
                if i == 4:
                    value = b + 2 ** -random.randint(0, 10)
                if i == 5:
                    value = b + random.randint(1, 10) ** (-1)
                list_of_infographs[i].list_of_values.append(value)
                # calculates new global highest and lowest
                if list_of_infographs[i].highest_global_value == None or list_of_infographs[
                    i].highest_global_value < value:
                    list_of_infographs[i].highest_global_value = value
                if list_of_infographs[i].lowest_global_value == None or list_of_infographs[
                    i].lowest_global_value > value:
                    list_of_infographs[i].lowest_global_value = value

    # -_-_-_-_-_-_-_-_-_-_-# User commands
    for event in pygame.event.get():
        cursor_position = pygame.mouse.get_pos()
        button_pressed = pygame.mouse.get_pressed(3)
        key_pressed = pygame.key.get_pressed()

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEWHEEL:
            if main_graph.size_of_frame and (serial_COM_port or dummy_infograph):
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
                connection_button.color = connection_button_color1
                connection_button.draw(cursor_position)
                pygame.display.update()
                connect()
                path_savedData = CreateArch(list_of_infographs)
                if serial_COM_port:
                    connection_button.color = connection_button_color
                    connection_button.text = message_connection_button_2
                    main_graph.size_of_frame = 10 * minimum_frame_size

                    try:
                        with open(file_name, "r") as file:
                            for line in file:
                                split_line = line.split(";")
                                if len(split_line) and split_line[0] != "" and len(list_of_tabs) < max_number_of_tabs:
                                    if len(list_of_tabs):
                                        list_of_tabs.append(tab(window_of_visualization, 30, list_of_tabs[-1].y + 30, 100, 20, split_line[0], False))
                                    else:
                                        list_of_tabs.append(tab(window_of_visualization, 30, 180, 100, 20, split_line[0], True))
                                    for j in range(len(split_line) - 1):
                                        if j + 1 < len(list_of_tabs[-1].checkboxes):
                                            try:
                                                list_of_tabs[-1].checkboxes[j].state = bool(int(split_line[j + 1]))
                                                if list_of_tabs[-1].checkboxes[j].state == False:
                                                    list_of_tabs[-1].selected_indexes.remove(j)
                                            except ValueError:
                                                break
                    except FileNotFoundError:
                        print("No predefined tabs")
                    if not len(list_of_tabs):
                        list_of_tabs.append(tab(window_of_visualization, 10, 150, 100, 20, "Tab " + str(tab_number), True))
                        tab_number += 1
                    selected_tab = list_of_tabs[0]

                    # configurates the y axis
                    main_graph.width -= len(selected_tab.selected_indexes) * y_axis_lenght
                    main_bar.width = main_graph.width
                else:
                    connection_button.color = connection_button_color2
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

            # -_-_-_-_-_-_-_-_-_-_-# User commands / Set Window button
            # set window size as standard
            if set_window_button.cursor_is_over(cursor_position):
                if serial_COM_port or dummy_infograph:
                    main_graph.initial_smallest_step_position_in_list = 0
                    main_graph.size_of_frame = len(smallest_step_infograph.list_of_values)
                    if main_graph.size_of_frame < minimum_frame_size:
                        main_graph.size_of_frame = minimum_frame_size

            # -_-_-_-_-_-_-_-_-_-_-# User commands / Change View button
            # alterantes between global and local view
            if change_view_button.cursor_is_over(cursor_position):
                if change_view_button.text == message_change_view_button_0:
                    change_view_button.text = message_change_view_button_1
                    local_view = False
                elif change_view_button.text == message_change_view_button_1:
                    change_view_button.text = message_change_view_button_0
                    local_view = True

            # -_-_-_-_-_-_-_-_-_-_-# User commands / Tab management
            # creates a new tab
            if new_tab_button.cursor_is_over(cursor_position) and len(list_of_tabs) and len(list_of_tabs) < max_number_of_tabs:
                list_of_tabs.append(tab(window_of_visualization, 30, list_of_tabs[-1].y + 30, 100, 20,
                                        "Tab " + str(tab_number)))
                tab_number += 1

            # checks if a tab is selected or closed
            for t in range(len(list_of_tabs)):
                if list_of_tabs[t].cursor_is_over(cursor_position):
                    selected_tab.selected = False
                    selected_tab = list_of_tabs[t]
                    selected_tab.selected = True
                    main_graph.width = main_graph_width - len(list_of_tabs[t].selected_indexes) * y_axis_lenght
                    main_bar.width = main_graph.width
                    break
                if list_of_tabs[t].cursor_is_over_close(cursor_position) and len(list_of_tabs) > 1:
                    test = list_of_tabs[t]
                    del list_of_tabs[t]
                    if test.selected:
                        list_of_tabs[0].selected = True
                        selected_tab = list_of_tabs[0]
                    for j in range(len(list_of_tabs) - t):
                        list_of_tabs[t + j].y = list_of_tabs[t + j].y - 30
                        list_of_tabs[t + j].close_y = list_of_tabs[t + j].close_y - 30
                    main_graph.width = main_graph_width - len(list_of_tabs[t].selected_indexes) * y_axis_lenght
                    main_bar.width = main_graph.width
                    break

            # -_-_-_-_-_-_-_-_-_-_-# User commands / Checkbox Management
            # checks if a checkbox is selected or deselected
            if selected_tab:
                for c in range(len(selected_tab.checkboxes)):
                    if selected_tab.checkboxes[c].cursor_is_over(cursor_position):
                        if selected_tab.checkboxes[c].state:
                            selected_tab.selected_indexes.remove(c)
                            main_graph.width += y_axis_lenght
                        else:
                            selected_tab.selected_indexes.append(c)
                            main_graph.width -= y_axis_lenght
                        main_bar.width = main_graph.width
                        selected_tab.checkboxes[c].state = not selected_tab.checkboxes[c].state


        if button_pressed[0] and (serial_COM_port or dummy_infograph):
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
        if event.type == pygame.KEYDOWN and (serial_COM_port or dummy_infograph):
            live_data = False
            freezing_button.text = message_freezing_button_1
            if event.key == pygame.K_LEFT:
                main_graph.initial_smallest_step_position_in_list -= 1
            if event.key == pygame.K_RIGHT:
                main_graph.initial_smallest_step_position_in_list += 1
            aovivo = False

    # displaces the graph
    if key_pressed[pygame.K_UP] and (serial_COM_port or dummy_infograph):
        live_data = False
        freezing_button.text = message_freezing_button_1
        main_graph.initial_smallest_step_position_in_list += 1
    if key_pressed[pygame.K_DOWN] and (serial_COM_port or dummy_infograph):
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
                value = list_of_infographs[i].list_of_values[-1]
                selected_tab.last_value_boxes[i].last_value = value
                if (list_of_infographs[i].alert_higher and value > list_of_infographs[i].alert_higher)  or (list_of_infographs[i].alert_lower and value < list_of_infographs[i].alert_lower):
                    selected_tab.last_value_boxes[i].show_alert_values_times = 1 + int(round((alert_time_on_screen / list_of_infographs[i].step)))

    main_graph.draw()
    main_bar.draw()

    # -_-_-_-_-_-_-_-_-_-_-# User interactives
    draws_buttons(cursor_position)
    pygame.draw.rect(window_of_visualization, (120, 120, 120), (25, 175, 140, 300), 0)
    for t in list_of_tabs:
        t.draw(cursor_position)

    if main_graph.cursor_is_over(cursor_position):
        pygame.mouse.set_visible(False)
        main_graph.info(cursor_position)
    else:
        pygame.mouse.set_visible(True)

    # updates pointer position while more values are taken into account
    main_bar.update_pointer()

    pygame.display.update()
