#!/usr/bin/python3
from sys import argv
from processo import Process
from escalonador import Scheduler
def readArq (filename):
  """ Description
  Função que faz abertura e leitura dos dados contidos no arquivo com a configuração dos processos e passados para uma 
  estrutura de tipo dicionário (dict) que será retornado para a execução dos métodos da classe Scheduler
  
  :type filename: str
  :param filename: Caminho de diretório do arquivo

  :rtype: dict
  """
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

fileError = "src/main.py ... -f [[Arquivo]] ... "
quantumError = "src/main.py ... -q [[Quantum(integer)]] ... "
blockTimeError = "src/main.py ... -b [[Tempo de Bloqueio para IO (integer)]] ... "

if __name__ == "__main__":
  #Caso não seja passado na linha de comando o quantum e o Block time, será padrão 4 e 2 respectivamente
  quantum = 4
  blockTime = 2
  dados = []

  fileVerify = False
  quantumVerify = False
  blockTimeVerify = False

  if len(argv) > 1:
    for (i, args) in enumerate(argv):
      if args == '-f' and not fileVerify:
        try:
          if argv[i+1][0] == '-':
            print(fileError)
            exit(0)
          file = argv[i+1]
        except:
          print("erro no parâmetro do arquivo\n\t", fileError)
          exit(0)

        dados = readArq(file)
        fileVerify = True
      elif args == '-q' and not quantumVerify:
        try:
          if argv[i+1][0] == '-':
            print(quantumError)
            exit(0)
          quantum = int(argv[i+1])
        except:
          print("erro no parâmetro do quantum\n\t", quantumError)  
          exit(0)
        quantumVerify = True
      elif args == '-b' and not blockTimeVerify:
        try:
          if argv[i+1][0] == '-':
            print(blockTimeError)
            exit(0)
          blockTime = int(argv[i+1])
        except:
          print("erro no parâmetro do tempo de bloqueio\n\t", blockTimeError)
          exit(0)

        blockTimeVerify = True

  if '-f' not in argv:
    print("Uma arquivo de configuração deve ser informado:\n\t ./main.py ... -f [[Arquivo]] ... ")
    exit(0)
  processos = []
  for dado in dados:
    processos.append(Process(dado))

  #Printa os símbolos dos estados dos processos
  print("\n\t\t\t\tProcesso em espera: \'_\' ")
  print("\t\t\t\tProcesso em execução: \'x\'")
  print("\t\t\t\tProcesso bloqueado: \'*\'")
  print("\t\t\t\tProcesso terminado: \'·\'\n")
  if blockTime <= 0:
    blockTime = 1
  #Instância da classe Scheduler
  sche = Scheduler(processos, blockTime)
  #Chamada dos métodos dos algoritmos de escalonamento
  sche.FirstComeFirstServed()
  sche.ShortestJobFirst()
  sche.RoundRobin(quantum)
  sche.Priority()