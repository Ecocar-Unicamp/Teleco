#Class for the tabs of diferent infographs. The class holds an index that identifies the tab, a list of the infographs
# avilable and a list of checkboxes used to selecte wich infographs will be shown. The class has a function to create
# new tabs and a class to draw the contents of the tab

class tabs:
    def __init__(self, index, list_of_infographs, selected = False):
        self.index = index
        self.list_of_infographs = list_of_infographs
        self.selected_infographs = []
        self.checkboxes = []
        self.selected = selected

    def create(self):
        for i in range(len(self.list_of_infographs)):
            self.checkboxes.append(Check_box((53, 87, 28), (0, 225, 0), 300, 40 * i + 40, 100))

    def draw(self):
        if self.selected:
            for i in range(len(self.list_of_infographs)):
                self.checkboxes[i].draw(window, (0, 0, 0))
                if self.checkboxes[i].state:
                    if not self.list_of_infographs[i] in self.selected_infographs:
                        self.selected_infographs.append(self.list_of_infographs[i])
                elif not self.checkboxes[i].state:
                    if self.list_of_infographs[i] in self.selected_infographs:
                        self.selected_infographs.remove(self.list_of_infographs[i])
            for j in self.selected_infographs:
                graph(i) #function for creating the graphs
