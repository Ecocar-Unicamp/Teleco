#Function creates a file to be used to savve the data
def CreateArq():
    arq_number = 0
    while True:
        try:
            arq_name = "dados telemetria" + str(arq_number) + ".txt"
            arq = open(arq_name)
        except IOError:
            arq = open(arq_name, "w")
            arq.write("Dados telemetria:\n")
            arq.write("Tempo:     Velocidade:\n")
            arq.close()
            return arq_name
        arq_number = arq_number + 1