#Function creates a file to be used to savve the data
import datetime

def CreateArq(list_of_infographs):
    #Creates the file name with current the date and time
    date = datetime.datetime.today()
    arq_name = "telemetry data" + str(date.day) + str(date.month) + str(date.year) + str(date.hour) + str(date.minute) + str(date.second)+ ".txt"

    #Creates the file and returns file name. If a file with this name already exists prints error menssage
    try:
        arq = open(arq_name, "w")

        arq.write("Data collection started at: " + str(date.day) + str(date.month) + str(date.year) + str(date.hour) + str(date.minute) + str(date.second) + "\n")
        arq.write("time ")
        for i in list_of_infographs:
            arq.write(i.name + " ")
            arq.write("\n")
        arq.close()

        return arq_name

    except IOError:
        print("ERROR: save file with this name already exists")

def Save_data(arq_name, list_of_infographs, time):
    #opens file
    arq = open(arq_name, "a")

    #writes the new data for each infograph in the file
    arq.write(str(time))
    for i in list_of_infographs:
        arq.write(" ; ")
        arq.write(i.list_of_values[-1])
    arq.write("\n")

    #closes the file
    arq.close()
