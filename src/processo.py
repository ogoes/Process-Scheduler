class Process:
  def __init__ (self, dados):
    """ Description
    Método construtor da classe Process
    
    :type self: Process (class)

    :type dados: dict
    :param dados: Estrutura contendo todas as informações coletadas na main.py do arquivo. 
    """
    self.__id = dados['id']
    self.__tamanho = dados['tamanho']
    self.__prioridade = dados['prioridade']
    self.__tempoChegada = dados['tempoChegada']
    self.__inOut = dados['I_O']

    self.init()
  def init (self):
    """Description
    Método que incializa os atributos da classe Process
    """
    self.__tempoExecutado = 0
    self.__tempoBloqueado = 0
    self.__tempoInicio = 0
    self.__tempoFim = 0
    self.__tempoEspera = 0
    self.__isFinished = False
    self.__isBlocked = False
    self.__tempoEmExecucao = 0
    self.__picoIndex = 0
    self.__string = ''
  def getEspera (self):
      """ Description
      Método que calcula o tempo de espera de um processo fazendo a subtração do tempo do clock da última execução do processo
      com o tempo de chegada, tempo executado e tempo bloqueado.
      
      :type self: Process (class)
    
      :rtype: int
      """
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
  def getPicoCPU (self):
    tempo = self.__tamanho - self.__tempoExecutado

    for i in self.__inOut:
      if i > self.__tempoExecutado:
        tempo = i - self.__tempoExecutado
        break
    return tempo
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
  def getTempoEmExecucao (self):
    return self.__tempoEmExecucao
  def setTempoEmExecucao (self):
    self.__tempoEmExecucao = 0
  def executa (self):
    """ Description
    Método que faz a execução em si do processo, incrementando seu tempo executado e o tempo em execução.
    Também faz a comparação do tempo executado com o tempo do respectivo processo de entrada e saída, quando a condição é verdadeira o processo tem seu estado
    mudado para Bloqueado.
    Por último faz a comparação do tempo executado com seu tamanho, quando a condição é verdadeiro o processo tem seu estado mudado para Terminado.
    
    :type self: Process (class)

    :rtype: None
    """
    self.__tempoExecutado += 1
    self.__tempoEmExecucao += 1

    if self.__tempoExecutado in self.__inOut:
      self.__isBlocked = True

    if self.__tempoExecutado == self.__tamanho:
      self.__isFinished = True
    return None

  def printa (self):
    """ Description
    Método que printa o id e as informações relativas dos estados dos respectivos processos.
    
    :type self: Process (class)

    :rtype: None
    """
    self.__string += '|'
    print("\tProcesso[%s] |%s" %(self.__id, self.__string))
    return None
    # print(self.__dados)
