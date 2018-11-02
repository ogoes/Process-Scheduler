from ordenacoes import *




class Scheduler:
  def __init__ (self, processos):
    self.__processos = processos
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
  def FirstComeFirstServed (self):
    self.initValues()
    filaEspera = [process for process in self.__processos if process.getBegin() == 0]
    filaBloqueado = []
    filaTerminado = []


    count = 0
    while len(filaTerminado) < len(self.__processos):

      while len (filaEspera) == 0:
        self.verifica(filaBloqueado, filaEspera)
        count += 1
      
      process = filaEspera.pop(0)
      if process.getTempoExecutado == 0:
        process.setInicio(count)
      while not process.isFinished() and not process.isBlocked():
                  
        process.executa()

        if process.isBlocked():
          filaBloqueado.append(process)

        for pros in self.__processos:
          self.verifica(filaBloqueado, filaEspera, process, pros)

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
    # filaBloqueado = []
    filaTerminado = []

    count = 0
    while len(filaTerminado) < len(self.__processos):
      ordenaTamanho(filaEspera)

      process = filaEspera.pop(0)
      process.setInicio(count)
      while not process.isFinished():
                  
        process.executa()
        process.appen('x')

        for pros in self.__processos:
          if pros != process:
            if pros.isFinished():
              pros.appen('·')
            elif count >= pros.getBegin():
              pros.appen('_')
            else:
              pros.appen(' ')

        count += 1
        filaEspera += [process for process in self.__processos if process.getBegin() == count]

      process.setFim(count)
      filaTerminado.append(process)


    print("Shortest Job First --> SJF\n")
    self.mostraResultados()


    pass
  def RoundRobin (self, quantum):
    pass
  def Priority (self):
    pass
  def verifica (self, filaBloqueado, filaEspera, processo=None, compare=None):
    if processo != None and compare != None:
      if compare != processo:
        if compare.isFinished():
          compare.appen('·')
        elif compare in filaEspera:
          compare.appen('_')
        elif compare.isBlocked():
          if compare.bloqueio() % 2 == 0:
            compare.unblock()
            filaEspera.append(compare)
            filaBloqueado.pop(filaBloqueado.index(compare))
          compare.appen('*')
        else:
          compare.appen(' ')
      else:
        compare.appen('x')
    else:
      for pros in self.__processos:
        if pros.isFinished():
          pros.appen('·')
        elif pros in filaEspera:
          pros.appen('_')
        elif pros.isBlocked():
          if pros.bloqueio() % 2 == 0:
            pros.unblock()
            filaEspera.append(pros)
            filaBloqueado.pop(filaBloqueado.index(pros))
          pros.appen('*')
        elif pros.getTempoExecutado() < pros.getTamanho():
          pros.appen('x')
        else:
          pros.appen(' ')
