#!/usr/bin/python3
from sys import argv
from processo import Process
from escalonador import Scheduler
def readArq (filename):
  try:
    file = open(filename) ## faz a tentativa de ler o arquivo
  except:
    print("Erro ao abrir o arquivo %s" %(filename)) ## se der errado é uma exceção
    exit(0)

  data = [line.strip() for line in file.readlines()] ## lista das linhas do arquivo

  for (i, line) in enumerate(data):
    if '#' in line: ## remove as strings a partir do #
      index = line.index('#')
      data[i] = line[0:index]

  dados = []

  for line in data: ## faz a coleta para cada linha
    if len(line) > 0:
      line = line.split(' ')
      processo = {}
      processo['id'] = int(line[0]) ## id do processo 
      processo['tamanho'] = int(line[1]) ## tamanho
      processo['prioridade'] = int(line[2]) ## prioridade
      processo['tempoChegada'] = int(line[3]) ## tempo de chegada
      processo['I_O'] = [] ## lista de eventos de I/O
      for io in line[4:]:
        if len(io) > 0:
          processo['I_O'].append(int(io))

      dados.append(processo)

  return dados ## retorna [dict] com :
  # [{
  #   'id': int
  #   'tamanho': int
  #   'prioridade': int
  #   'tempoChegada': int
  #   'I_O': [int, int, ... , int]
  # }]

if __name__ == "__main__":

  if len(argv) > 1:
    dados = readArq(argv[1])
    processos = []
    for dado in dados:
      processos.append(Process(dado))

    print("\n\t\t\t\tProcesso em espera: \'_\' ")
    print("\t\t\t\tProcesso em execução: \'x\'")
    print("\t\t\t\tProcesso bloqueado: \'*\'")
    print("\t\t\t\tProcesso terminado: \'·\'\n")
    sche = Scheduler(processos)
    # sche.FirstComeFirstServed()
    sche.FirstComeFirstServed()
    sche.ShortestJobFirst()


    # perguntar ao professor sobre o trabalho
    # file, io, bloqueio
    