import random

class Process:
  def __init__ (self, dados):
    self.__id = dados['id']
    self.__tamanho = dados['tamanho']
    self.__prioridade = dados['prioridade']
    self.__tempoChegada = dados['tempoChegada']
    self.__inOut = dados['I_O']

    self.init()
  def init (self):
    self.__tempoExecutado = 0
    self.__tempoBloqueado = 0
    self.__tempoInicio = 0
    self.__tempoFim = 0
    self.__tempoEspera = random.choice([1, 2])
    self.__isFinished = False
    self.__isBlocked = False
    self.__string = ''
  def getEspera (self):
    self.__tempoEspera = self.__tempoFim - self.__tempoChegada - self.__tempoExecutado - self.__tempoBloqueado
    return self.__tempoEspera
  def getBegin (self):
    return self.__tempoChegada
  def getPriori (self):
    return self.__prioridade
  def getTamanho (self):
    return self.__tamanho
  def getId (self):
    return self.__id
  def getTempoExecutado (self):
    return self.__tempoExecutado
  def getInicio (self):
    return self.__tempoInicio
  def bloqueio (self):
    self.__tempoBloqueado += 1
    return self.__tempoBloqueado
  def unblock (self):
    self.__isBlocked = False
  def setInicio (self, inicio):
    self.__tempoInicio = inicio
  def setFim (self, fim):
    self.__tempoFim = fim
  def isFinished (self):
    return self.__isFinished
  def appen (self, dado):
    self.__string += dado
  def isBlocked (self):
    return self.__isBlocked
  def executa (self):
    self.__tempoExecutado += 1

    if self.__tempoExecutado in self.__inOut:
      self.__isBlocked = True

    if self.__tempoExecutado == self.__tamanho:
      self.__isFinished = True
  def printa (self):
    self.__string += '|'
    print("\tProcesso[%s] |%s -> ini = %i, fim = %i" %(self.__id, self.__string, self.__tempoInicio, self.__tempoFim))
    # print(self.__dados)
