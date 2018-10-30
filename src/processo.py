

class Process:
  def __init__(self, dados):
    self.__id = dados['id']
    self.__tamanho = dados['tamanho']
    self.__prioridade = dados['prioridade']
    self.__tempoChegada = dados['tempoChegada']
    self.__inOut = dados['I_O']

    self.__tempoExecutado = 0
    self.__tempoTotal = 0
    self.__isFinished = False

    
  