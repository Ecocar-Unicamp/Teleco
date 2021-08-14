def print_point_value(cursor_position, points, infographs, size, window, color, font, points_range):
    point_distance = 1000000000
    aux = 0
    closest_point = ()
    font3 = pygame.font.SysFont('freesansbold.ttf',int(15))

    if len(points) > 1:
        if len(points[0]) > 1:
            for i in range(len(points)):
                for j in range(len(points[i])):
                    aux = ((cursor_position[0]-points[i][j][0])**2+(cursor_position[1]-points[i][j][1])**2)
                    if aux < point_distance:
                        point_distance = aux
                        closest_point = (i,j)

            if closest_point[0] >= len(points_range):
                closest_point = (len(points_range) - 1, j)

            selected_range = len(points_range[closest_point[0]])

            if j + selected_range >= len(infographs[closest_point[0]].list_of_values):
                j = len(infographs[closest_point[0]].list_of_values) - 1 - selected_range

            if cursor_position[0] > int(size[0]/2):
                if cursor_position[1] > int(size[1]/2):
                    pygame.draw.rect(window, color, (cursor_position[0] - 50, cursor_position[1] - 20, 50, 20))
                    info1 = font3.render(str(infographs[closest_point[0]].name) + ":" ,  True, (0, 0, 0))
                    info2 = font3.render(str(infographs[closest_point[0]].list_of_values[j + selected_range]),  True, (0, 0, 0))
                    window.blit(info1, (cursor_position[0] - 50, cursor_position[1] - 20))
                    window.blit(info2, (cursor_position[0] - 50, cursor_position[1] - 10))
                else:
                    pygame.draw.rect(window, color, (cursor_position[0] - 50, cursor_position[1], 50, 20))
                    info1 = font3.render(str(infographs[closest_point[0]].name) + ":", True, (0, 0, 0))
                    info2 = font3.render(str(infographs[closest_point[0]].list_of_values[j + selected_range]), True, (0, 0, 0))
                    window.blit(info1, (cursor_position[0] - 50, cursor_position[1]))
                    window.blit(info2, (cursor_position[0] - 50, cursor_position[1] + 10))
            else:
                if cursor_position[1] > int(size[1]/2):
                    pygame.draw.rect(window, color, (cursor_position[0], cursor_position[1] - 20, 50, 20))
                    info1 = font3.render(str(infographs[closest_point[0]].name) + ":", True, (0, 0, 0))
                    info2 = font3.render(str(infographs[closest_point[0]].list_of_values[j + selected_range]), True, (0, 0, 0))
                    window.blit(info1, (cursor_position[0], cursor_position[1] - 20))
                    window.blit(info2, (cursor_position[0], cursor_position[1] - 10))
                else:
                    pygame.draw.rect(window, color, (cursor_position[0], cursor_position[1], 50, 20))
                    info1 = font3.render(str(infographs[closest_point[0]].name) + ":", True, (0, 0, 0))
                    info2 = font3.render(str(infographs[closest_point[0]].list_of_values[j + selected_range]), True, (0, 0, 0))
                    window.blit(info1, (cursor_position[0], cursor_position[1]))
                    window.blit(info2, (cursor_position[0], cursor_position[1] + 10))