class Scheduler:
  """ Classe para o escalonador de processos."""
  def __init__ (self, processos, blockTime):  
    """ Description
    :type self: Scheduler (class)

    :type processos: list
    :param processos: Vetor com os dados de todos os processos lidos no arquivo na main

    :type blockTime: int
    :param blockTime: Tempo de bloqueio para o processo quando ocorre evento de E/S

    :rtype:
    """
    self.__blockTime = blockTime
    self.__processos = processos
    
  def initValues (self):
    """ Método que faz inicialização das variáveis dos processos"""
    for process in self.__processos:
      process.init()

    self.__maxFilaEspera = 0
    self.__maxFilaBloqueado = 0
    self.__medFilaEspera = 0
    self.__medFilaBloqueado = 0
    self.__clock = 0
    self.__tempoOcioso = 0

  def mostraResultados (self):
    """ Método que mostra as medições e estatísticas referentes a cada algoritmo de escalonamento """
    for p in self.__processos:
      p.printa()

    string = ''
    print("\n\t\tTempo Total de Espera (TTE): ", end='')
    soma = 0
    for (i, p) in enumerate(self.__processos):
      string += '%i' %(p.getEspera())
      if i < len(self.__processos)-1:
        string += ' + '
      soma += (p.getEspera())

    print('%s = %it' %(string, soma))
    print('\t\tTempo Médio de Espera (TME): ', end='')
    print('(%s)/%i = %ft' %(string, len(self.__processos), soma/len(self.__processos)))

    print('\t\tTamanho máximo da fila de Espera (Apto/Pronto): %i'%(self.__maxFilaEspera))
    print("\t\tTamanho médio da fila de Espera (Apto/Pronto): %f" %(self.__medFilaEspera/self.__clock))
    print('\t\tTamanho máximo da fila de Bloqueio (Suspenso): %i'%(self.__maxFilaBloqueado))
    print('\t\tTamanho médio da fila de Bloqueio (Suspenso): %f' %(self.__medFilaBloqueado/self.__clock))
    print("\t\tTempo de ociosidade da CPU: %it" %(self.__tempoOcioso))

  def FirstComeFirstServed (self):
    """ Description
    Método que simula o algoritmo de escalonamento First Come First Served
    :type self: Scheduler (Class)

    :rtype: None
    """
    self.initValues()
    filaEspera = [process for process in self.__processos if process.getBegin() == 0]
    filaBloqueado = []
    filaTerminado = [] 

    while len(filaTerminado) < len(self.__processos):
      
      while len (filaEspera) == 0:
        self.__medFilaBloqueado += len(filaBloqueado)
        self.__tempoOcioso += 1
        self.__verifica__(filaBloqueado, filaEspera)
        self.__clock += 1
        filaEspera += [process for process in self.__processos if process.getBegin() == self.__clock]
      
      process = filaEspera.pop(0)
      if process.getTempoExecutado() == 0:
        process.setInicio(self.__clock)
      while not process.isFinished() and not process.isBlocked():

        if len(filaEspera) > self.__maxFilaEspera:
          self.__maxFilaEspera = len(filaEspera)
        if len(filaBloqueado) > self.__maxFilaBloqueado:
          self.__maxFilaBloqueado = len(filaBloqueado)

        self.__medFilaBloqueado += len(filaBloqueado)
        self.__medFilaEspera += len(filaEspera)

        process.executa()

        if process.isBlocked():
          filaBloqueado.append(process)

        self.__verifica__(filaBloqueado, filaEspera, process)

        self.__clock += 1
        filaEspera += [process for process in self.__processos if process.getBegin() == self.__clock]

      if process.isFinished():
        process.setFim(self.__clock)
        filaTerminado.append(process)

    print("First Come, First Served --> FCFS\n")
    self.mostraResultados()
    return None

  def ShortestJobFirst (self):
    """ Description
    :type self: Scheduler (class)

    :rtype: None
    """
    self.initValues()
    filaEspera = [process for process in self.__processos if process.getBegin() == 0]
    filaBloqueado = []
    filaTerminado = []

    while len(filaTerminado) < len(self.__processos):
      
      while len (filaEspera) == 0:
        self.__verifica__(filaBloqueado, filaEspera)
        self.__medFilaBloqueado += len(filaBloqueado)
        self.__tempoOcioso += 1
        self.__clock += 1
        filaEspera += [process for process in self.__processos if process.getBegin() == self.__clock]
      
      filaEspera.sort(key = lambda x: x.getPicoCPU())

      process = filaEspera.pop(0)
      if process.getTempoExecutado() == 0:
        process.setInicio(self.__clock)
      while not process.isFinished() and not process.isBlocked():

        if len(filaEspera) > self.__maxFilaEspera:
          self.__maxFilaEspera = len(filaEspera)
        if len(filaBloqueado) > self.__maxFilaBloqueado:
          self.__maxFilaBloqueado = len(filaBloqueado)

        self.__medFilaBloqueado += len(filaBloqueado)
        self.__medFilaEspera += len(filaEspera)

        process.executa()

        if process.isBlocked():
          filaBloqueado.append(process)

        self.__verifica__(filaBloqueado, filaEspera, process)

        self.__clock += 1
        filaEspera += [process for process in self.__processos if process.getBegin() == self.__clock]

      if process.isFinished():
        process.setFim(self.__clock)
        filaTerminado.append(process)

    print("Shortest Job First --> SJF\n")
    self.mostraResultados()
    return None

  def RoundRobin (self, quantum):
    """Description
    :type self: Scheduler (class)
  
    :type quantum: int
    :param quantum: Tempo máximo que um processo pode executar em sequência

    :rtype: None
    """
    self.initValues()
    filaEspera = [process for process in self.__processos if process.getBegin() == 0]
    filaBloqueado = []
    filaTerminado = []

    if quantum > 0:

      while len(filaTerminado) < len(self.__processos):

        while len(filaEspera) == 0:
          self.__verifica__(filaBloqueado, filaEspera)
          self.__medFilaBloqueado += len(filaBloqueado)
          self.__tempoOcioso += 1
          self.__clock += 1
          filaEspera += [process for process in self.__processos if process.getBegin() == self.__clock]


        process = filaEspera.pop(0)
        process.setTempoEmExecucao()
        if process.getTempoExecutado() == 0:
          process.setInicio(self.__clock)
        while not process.isFinished() and not process.isBlocked():

          if process.getTempoEmExecucao() == (quantum):
            process.setTempoEmExecucao()
            filaEspera.append(process)
            break

          if len(filaEspera) > self.__maxFilaEspera:
            self.__maxFilaEspera = len(filaEspera)
          if len(filaBloqueado) > self.__maxFilaBloqueado:
            self.__maxFilaBloqueado = len(filaBloqueado)

          self.__medFilaBloqueado += len(filaBloqueado)
          self.__medFilaEspera += len(filaEspera)

          process.executa()
          if process.isBlocked():
            filaBloqueado.append(process)
          


          self.__verifica__(filaBloqueado, filaEspera, process)

          self.__clock += 1
          filaEspera += [process for process in self.__processos if process.getBegin() == self.__clock]

        if process.isFinished():
          process.setFim(self.__clock)
          filaTerminado.append(process)

      print("Round Robin --> RR\n")
      self.mostraResultados()
    return None

  def Priority (self):
    """ Description
    :type self: Scheduler (class)

    :rtype: None
    """
    self.initValues()
    filaEspera = [process for process in self.__processos if process.getBegin() == 0]
    filaBloqueado = []
    filaTerminado = []


    while len(filaTerminado) < len(self.__processos):
      
      while len (filaEspera) == 0:
        self.__verifica__(filaBloqueado, filaEspera)
        self.__medFilaBloqueado += len(filaBloqueado)
        self.__tempoOcioso += 1
        self.__clock += 1
        filaEspera += [process for process in self.__processos if process.getBegin() == self.__clock]

      
      filaEspera.sort(key = lambda x: x.getPriori() * -1)

      process = filaEspera.pop(0)
      if process.getTempoExecutado() == 0:
        process.setInicio(self.__clock)


      if len(filaEspera) > self.__maxFilaEspera:
        self.__maxFilaEspera = len(filaEspera)
      if len(filaBloqueado) > self.__maxFilaBloqueado:
        self.__maxFilaBloqueado = len(filaBloqueado)

      self.__medFilaBloqueado += len(filaBloqueado)
      self.__medFilaEspera += len(filaEspera)
      
      process.executa()

      if process.isBlocked():
        filaBloqueado.append(process)

      self.__verifica__(filaBloqueado, filaEspera, process)
      self.__clock += 1

      filaEspera += [process for process in self.__processos if process.getBegin() == self.__clock]


      if process.isFinished():
        process.setFim(self.__clock)
        filaTerminado.append(process)
      elif not process.isBlocked():
        filaEspera.insert(0, process)

    print("Prioridade --> P\n")
    self.mostraResultados()
    return None

  def __verifica__ (self, filaBloqueado, filaEspera, processo=None, quantum=None):
    """ Description
    Método que percorre os processos do escalonador verificando se é o processo que está em execução ou não.
    Se for o processo em execução, o "buffer" do vetor é marcado com um 'x'
    Caso contrário será marcado com o respectivo estado do processo. Símbolos que representam os estados dos processos: 
    Processo em espera: '_',
    Processo bloqueado: '*',
    Processo terminado: '·'

    :type self: Scheduler (class)
  
    :type filaBloqueado: list 
    :param filaBloqueado: Fila de processos bloqueados
  
    :type filaEspera: list 
    :param filaEspera: Fila de processos em espera
  
    :type processo: Process (class)
    :param processo: Processo em execução no momento da chamada da função
  
    :rtype: None
    """
    for pros in self.__processos:
      if pros != processo:
        if pros.isFinished():
          pros.appen('·')
        elif pros in filaEspera:
          pros.appen('_')
        elif pros.isBlocked():
          if pros.bloqueio() % self.__blockTime == 0:
            pros.unblock()
            filaEspera.append(pros)
            filaBloqueado.pop(filaBloqueado.index(pros))
          pros.appen('*')
        else:
          pros.appen(' ')
      else:
          pros.appen('x')

