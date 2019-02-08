#Dennis Felipe Urtubia e Otavio Silva Goes
import view
from time import sleep
class Scheduler:
  """ Classe para o escalonador de processos."""
  def __init__ (self, processos, blockTime):  
    """ Description
    Método construtor da classe Scheduler
    :type self: Scheduler (class)

    :type processos: list
    :param processos: Vetor com os dados de todos os processos lidos no arquivo na main

    :type blockTime: int
    :param blockTime: Tempo de bloqueio para o processo quando ocorre evento de E/S

    :rtype: None
    """
    

    self.__blockTime = blockTime
    self.__processos = processos
    return None
    
  def initValues (self):
    """ Método que faz inicialização das variáveis dos processos e do escalonador """
    for process in self.__processos:
      process.init()

    self.__view = view.Viewer(self.__processos)
    ## variaveis que geram algumas estatísticas de cada algoritmo
    self.__maxFilaEspera = 0
    self.__maxFilaBloqueado = 0
    self.__medFilaEspera = 0
    self.__medFilaBloqueado = 0

    ## variavel responsavel por representar o tempo no algoritmo
    self.__clock = 0
    ## tempo ocioso do processador, caso não haja processos executando ou na fila de espera (aptos)
    self.__tempoOcioso = 0

  def mostraResultados (self):
    """ Método que mostra as medições e estatísticas referentes a cada algoritmo de escalonamento """
    for p in self.__processos:
      p.printa()

    string = '' ## string responsavel por mostrar a série da soma dos tempos de espera dos processos
    soma = 0
    for (i, p) in enumerate(self.__processos):
      ## coleta dos tempos de espera de todos os processos
      string += '%i' %(p.getEspera())
      if i < len(self.__processos)-1:
        string += ' + '
      soma += (p.getEspera())

    print('\n\t\tTempo Total de Espera (TTE): %s = %i t' %(string, soma))
    print('\t\tTempo Médio de Espera (TME): ', end='')
    print('(%s)/%i = %f t' %(string, len(self.__processos), soma/len(self.__processos))) ### TME = TTE/qtdeProcessos

    print("\t\tProcessos executados por unidade de tempo: %f" %(len(self.__processos)/self.__clock))
    print('\t\tTamanho máximo da fila de Espera (Apto/Pronto): %i'%(self.__maxFilaEspera))
    print("\t\tTamanho médio da fila de Espera (Apto/Pronto): %f" %(self.__medFilaEspera/self.__clock))
    print('\t\tTamanho máximo da fila de Bloqueio (Suspenso): %i'%(self.__maxFilaBloqueado))
    print('\t\tTamanho médio da fila de Bloqueio (Suspenso): %f' %(self.__medFilaBloqueado/self.__clock))
    print("\t\tTempo de ociosidade da CPU: %i t" %(self.__tempoOcioso))

  def FirstComeFirstServed (self):
    """ Description
    Método que simula o algoritmo de escalonamento First Come First Served
    :type self: Scheduler (Class)

    :rtype: None
    """
    self.initValues()
    filaEspera = [process for process in self.__processos if process.getBegin() == 0] ## coleta os proecessos que chegaram na CPU no tempo zero
    filaBloqueado = []
    filaTerminado = [] 

    while len(filaTerminado) < len(self.__processos): ## a fila de terminados é menor que a de todos processos
      
      while len (filaEspera) == 0: ## caso a fila de espera esteja vazia, 
        self.__medFilaBloqueado += len(filaBloqueado)
        self.__tempoOcioso += 1 ## aumenta o tempo de ociosidade do processador
        self.__verifica__(filaBloqueado, filaEspera) ## mostra os simbolos correspondentes para cada processo, caso um processo saia de bloquado, vai para a fila de espera
        self.__clock += 1
        filaEspera += [process for process in self.__processos if process.getBegin() == self.__clock] ## coleta os processos que chegaram na CPU no mesmo tempo de clock
        self.__view.show(filaEspera, filaBloqueado, filaTerminado)
        sleep(0.5)

      
      process = filaEspera.pop(0) ## o primeiro da fila (chegou primeiro) é o que executará
      if process.getTempoExecutado() == 0:
        process.setInicio(self.__clock) ## define o tempo que o processo começou a executar
      while not process.isFinished() and not process.isBlocked(): ## permanece executando até finalizar ou ser bloqueado para IO


        ## estatísticas das filas
        if len(filaEspera) > self.__maxFilaEspera:
          self.__maxFilaEspera = len(filaEspera)
        if len(filaBloqueado) > self.__maxFilaBloqueado:
          self.__maxFilaBloqueado = len(filaBloqueado)

        self.__medFilaBloqueado += len(filaBloqueado)
        self.__medFilaEspera += len(filaEspera)


        ## execução de um ciclo do processo
        process.executa()

        ## caso ele execute e seja bloquado vai para a fila de bloqueados
        if process.isBlocked():
          filaBloqueado.append(process)

        ## adiciona o simbolo correspondente para cada processo
        ## se um processo saia do bloqueio ele volta para a fila de espera (apto)
        self.__verifica__(filaBloqueado, filaEspera, process)

        self.__clock += 1 ## veriavel de tempo
        ## pega os processos que chegaram a CPU naquele tempo
        filaEspera += [process for process in self.__processos if process.getBegin() == self.__clock]
        
        self.__view.show(filaEspera, filaBloqueado, filaTerminado)
        sleep(0.5)

      if process.isFinished():
        ## define o tempo que o processo terminou a sua execução
        process.setFim(self.__clock)
        filaTerminado.append(process) ## poe na fila de processos terminados

    print("First Come, First Served --> FCFS\n")
    # self.mostraResultados() ## informa as estatísticas deste algoritmo
    return None


  """
  Os algoritmos seguem o mesmo padrão do First Come, First Served, assim não será necessário explica-los a fundo:

  Diferenças:

      SJF: é preciso ordenar a fila de espera para que o processo com menor de ciclo de CPU possa executar previamente
      Round Robin: O processo para de executar quando o quantum é "atingido", assim da espaço para que outro processo possa executar

      Prioridade: Os processos não mais executam mais que um ciclo por vez, assim a verificação de prioridade é feita a todo ciclo de clock
                  A fila de espera é ordenado com base na prioridade dos processos.
  """

  
  def ShortestJobFirst (self):
    """ Description
    Método que simula o algoritmo de escalonamento SJF
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
    Método que simula o algoritmo de escalonamento Round Robin
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
          self.__medFilaBloqueado += len(filaBloqueado)
          self.__tempoOcioso += 1
          self.__clock += 1
          self.__verifica__(filaBloqueado, filaEspera)
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
          



          self.__clock += 1
          self.__verifica__(filaBloqueado, filaEspera, process)
          filaEspera += [process for process in self.__processos if process.getBegin() == self.__clock]

        if process.isFinished():
          process.setFim(self.__clock)
          filaTerminado.append(process)

      print("Round Robin --> RR\n")
      self.mostraResultados()
    return None

  def Priority (self):
    """ Description
    Método que simula o algoritmo de escalonamento de Prioridade
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

  def __verifica__ (self, filaBloqueado, filaEspera, processo=None):
    """ Description
    Método que percorre os processos do escalonador verificando se é o processo que está em execução ou não.
    Se for o processo em execução, o "buffer" do vetor é marcado com um 'x'
    Caso contrário será marcado com o respectivo estado do processo. Símbolos que representam os estados dos processos: 
    Processo em espera: '_'
    Processo bloqueado: '*'
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
    for pros in self.__processos: ## percorre toda a lista de processos existentes
      if pros != processo: ## caso não seja o processo que esteja executando no momento
        ## insere o simbolo correspondente ao estado do processo 
        if pros.isFinished(): 
          pros.appen('·') ## terminado
        elif pros in filaEspera:
          pros.appen('_') ## em espera (apto)
        elif pros.isBlocked():
          if pros.bloqueio() % self.__blockTime == 0:## ficou bloqueado em io o tempo especificado
            pros.unblock() ## desbloqueia o processo
            filaEspera.append(pros) ## insere na fila de espera (aptos)
            filaBloqueado.pop(filaBloqueado.index(pros)) ## tira da fila de bloqueio
          pros.appen('*')## bloqueado
        else:
          pros.appen(' ') ## caso não esteja esperando/bloqueado/executando
      else:
          pros.appen('x') ## simbolo referente a uma execução do processo

