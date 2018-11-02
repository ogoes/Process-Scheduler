from ordenacoes import *




class Scheduler:
  def __init__ (self, processos, blockTime):
    self.__blockTime = blockTime
    self.__processos = processos
    self.__maxFilaEspera = 0
    self.__maxFilaBloqueado = 0
    self.__medFilaEspera = 0
    self.__medFilaBloqueado = 0
  def initValues (self):
    for process in self.__processos:
      process.init()
    pass
  def mostraResultados (self):
    ordenaId(self.__processos)
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

    print('%s =' %(string), soma, 't')
    print('\t\tTempo Médio de Espera (TME): ', end='')
    print('(%s)/%i = %f' %(string, len(self.__processos), soma/len(self.__processos)), 't\n')

    print('\t\tTamanho máximo da fila de Espera (Apto/Pronto): %i'%(self.__maxFilaEspera))
    print('\t\tTamanho máximo da fila de Bloqueio (Suspenso): %i'%(self.__maxFilaBloqueado))
    print("")
  def FirstComeFirstServed (self):
    self.initValues()
    filaEspera = [process for process in self.__processos if process.getBegin() == 0]
    filaBloqueado = []
    filaTerminado = []


    count = 0
    while len(filaTerminado) < len(self.__processos):
      if len(filaEspera) > self.__maxFilaEspera:
        self.__maxFilaEspera = len(filaEspera)
      if len(filaBloqueado) > self.__maxFilaBloqueado:
        self.__maxFilaBloqueado = len(filaBloqueado)
      while len (filaEspera) == 0:
        self.__verifica__(filaBloqueado, filaEspera)
        count += 1
      
      process = filaEspera.pop(0)
      if process.getTempoExecutado == 0:
        process.setInicio(count)
      while not process.isFinished() and not process.isBlocked():
                  
        process.executa()

        if process.isBlocked():
          filaBloqueado.append(process)

        self.__verifica__(filaBloqueado, filaEspera, process)

        count += 1
        filaEspera += [process for process in self.__processos if process.getBegin() == count]

      if process.isFinished():
        process.setFim(count)
        filaTerminado.append(process)

    print("First Come, First Served --> FCFS\n")
    self.mostraResultados()
  def ShortestJobFirst (self):
    self.initValues()

    filaEspera = [process for process in self.__processos if process.getBegin() == 0]
    filaBloqueado = []
    filaTerminado = []

    count = 0
    while len(filaTerminado) < len(self.__processos):
      while len (filaEspera) == 0:
        self.__verifica__(filaBloqueado, filaEspera)
        count += 1
      
      ordenaTamanho(filaEspera)

      process = filaEspera.pop(0)
      process.setInicio(count)
      while not process.isFinished() and not process.isBlocked():
                  
        process.executa()
        if process.isBlocked():
          filaBloqueado.append(process)
          
        self.__verifica__(filaBloqueado, filaEspera, process)

        count += 1
        filaEspera += [process for process in self.__processos if process.getBegin() == count]

      if process.isFinished():
        process.setFim(count)
        filaTerminado.append(process)


    print("Shortest Job First --> SJF\n")
    self.mostraResultados()


    pass
  def RoundRobin (self, quantum):
    pass
  def Priority (self):
    pass
  def __verifica__ (self, filaBloqueado, filaEspera, processo=None):
    if processo != None:
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
    else:
      for pros in self.__processos:
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
        elif pros.getTempoExecutado() < pros.getTamanho():
          pros.appen('x')
        else:
          pros.appen(' ')
