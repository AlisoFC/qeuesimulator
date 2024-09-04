import sys
from randomNumberGenerator import NextRandom
import time

count = 100000
fila = []
tempo_global = 0
times = []
clientes_perdidos = 0
primeira_chegada = True
tempo_primeira_chegada = 2.0

def CHEGADA():
    global fila, clientes_perdidos, primeira_chegada

    if primeira_chegada and tempo_global < tempo_primeira_chegada:
        return
    primeira_chegada = False

    if len(fila) < K:
        fila.append(tempo_atendimento())
    else:
        clientes_perdidos += 1

def SAIDA(servidor_idx):
    global fila
    if fila:
        fila.pop(0)

def NextEvent():
    return NextRandom() < 0.5

def tempo_chegada():
    return int(min_chegada + (max_chegada - min_chegada) * NextRandom())

def tempo_atendimento():
    return int(min_atendimento + (max_atendimento - min_atendimento) * NextRandom())

def inicializar_simulacao(args):
    global num_servidores, K, times, min_chegada, max_chegada, min_atendimento, max_atendimento

    if len(args) != 6:
        sys.exit(1)

    _, config, min_chegada_str, max_chegada_str, min_atendimento_str, max_atendimento_str = args
    partes = config.split("/")
    
    if len(partes) != 4 or partes[0] != "G" or partes[1] != "G":
        sys.exit(1)

    num_servidores = int(partes[2])
    K = int(partes[3])

    min_chegada = int(min_chegada_str)
    max_chegada = int(max_chegada_str)
    min_atendimento = int(min_atendimento_str)
    max_atendimento = int(max_atendimento_str)

    times = [0] * (K + 1)

def simulador():
    global tempo_global, count

    servidores = [0] * num_servidores

    while count > 0:
        evento_chegada = NextEvent()

        if evento_chegada:
            CHEGADA()
        else:
            for i in range(num_servidores):
                if servidores[i] == 0 and fila:
                    servidores[i] = fila.pop(0)
                if servidores[i] > 0:
                    servidores[i] -= 1
                    if servidores[i] == 0:
                        SAIDA(i)

        times[len(fila)] += 1
        tempo_global += 1
        count -= 1
        time.sleep(0.01)

    for i in range(K + 1):
        print(f"{i}: {times[i]} ({times[i] / tempo_global * 100:.2f}%)")

    print(f"Clientes perdidos: {clientes_perdidos}")
    print(f"Tempo total da simulação: {tempo_global}")

if __name__ == "__main__":
    inicializar_simulacao(sys.argv)
    simulador()
