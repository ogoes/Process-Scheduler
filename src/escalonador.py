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
    # filaBloqueado = []
    filaTerminado = []


    count = 0
    while len(filaTerminado) < len(self.__processos):
      ordenaTempoChegada(filaEspera)

      process = filaEspera.pop(0)
      process.setInicio(count)
      while not process.isFinished():
                  
        process.executa()
        process.appen('x')

        for pros in self.__processos:
          if pros != process:
            if pros.isFinished():
              pros.appen('·')
            elif pros in filaEspera:
              pros.appen('_')
            else:
              pros.appen(' ')

        count += 1
        filaEspera += [process for process in self.__processos if process.getBegin() == count]

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