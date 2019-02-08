import os
from time import sleep
import math

# Prontos, Em Espera, Bloqueados, Concluídos
class Viewer():
  def __init__(self, process):
    self.__process = process

    self.__numberOfProcess = len(self.__process)

    self.__dimensions = {
      "cellMin": 14,
      "cellMax": None,
      "spaceBetween": 4
    }

    self.__paddings = {
      "left": 10,
      "right": 10,
      "top": 1,
      "bottom": 3      
    }

    self.__ANSICodes = {
      "fgBlack": '\x1b[0;30m',
      "fgRed": '\x1b[0;31m',
      "fgGreen": '\x1b[0;32m',
      "fgYellow": '\x1b[0;33m',
      "fgBlue": '\x1b[0;34m',
      "fgMagenta": '\x1b[0;35m',
      "fgCyan": '\x1b[0;36m',
      "fgWhite": '\x1b[0;37m',
      "bgBlack": '\x1b[0;40m',
      "bgRed": '\x1b[0;41m',
      "bgGreen": '\x1b[0;42m',
      "bgYellow": '\x1b[0;43m',
      "bgBlue": '\x1b[0;44m',
      "bgMagenta": '\x1b[0;45m',
      "bgCyan": '\x1b[0;46m',
      "bgWhite": '\x1b[0;47m',
      
      "clearScreen": '\x1b[2J',
      "moveCursorTopRight": '\x1b[1;1H',
      "endc": '\x1b[0;0m'
    }

    pass

  def show(self, waitingList, blockedList, finishedList):
    self.__showHeaders()
    self.__showContent(waitingList, blockedList, finishedList)
    self.__showGraph()
    pass

  def __showGraph (self):
    print('\n' * self.__paddings['top'])
    for process in self.__process:
      process.printa()
    print('\n' * self.__paddings['bottom'])
    
    pass

  def __showHeaders (self):
    self.__headers = [
      ('Em  Espera', self.__ANSICodes['fgCyan']),
      ('Bloqueados', self.__ANSICodes['fgRed']),
      ('Concluídos', self.__ANSICodes['fgGreen'])
    ]


    print(self.__ANSICodes['clearScreen'] + self.__ANSICodes['moveCursorTopRight'])
    self.__calculateDimentions()
    print('\n' * self.__paddings['top'], end='')
    print(' ' * self.__paddings['left'], end='')
    
    for header in range(3):
      print(self.__headers[header][1] + '+', end='')
      print('-' * (self.__dimensions['cellMax'] - 2), end='')
      print('+', end='')
      print(self.__ANSICodes['endc'], end='')
      if (header < 3):
        print(' ' * self.__dimensions['spaceBetween'], end='')

    print(' ' * self.__paddings['right'])
    
    print(' ' * self.__paddings['left'], end='')

    for header in range(3):
      text = self.__headers[header][0]
      spaces = (self.__dimensions['cellMax'] - len(text) - 1) // 2
      print(self.__headers[header][1] + '|', end='')
      print(' ' * spaces, end='')
      print(self.__headers[header][0], end='')      
      print(' ' * spaces, end='')
      print('|', end='')
      print(self.__ANSICodes['endc'], end='')
      if (header < 3):
        print(' ' * self.__dimensions['spaceBetween'], end='')

    print(' ' * self.__paddings['right'])

    print(' ' * self.__paddings['left'], end='')
    
    for header in range(3):
      print(self.__headers[header][1] + '+', end='')
      print('-' * (self.__dimensions['cellMax'] - 2), end='')
      print('+', end='')
      print(self.__ANSICodes['endc'], end='')
      if (header < 3):
        print(' ' * self.__dimensions['spaceBetween'], end='')

    print(' ' * self.__paddings['right'])


  def __showContent (self, waitingList, blockedList, finishedList):
    queues = [waitingList, blockedList, finishedList]
    for process in range(self.__numberOfProcess):
      print(' ' * self.__paddings['left'], end='')

      for header in range(3):
        if len(queues[header]) > process:
          # tamanho = math.ceil(math.log10(queues[header][process]))
          spaces = (self.__dimensions['cellMax'] - 2) // 2 - 1
          print(self.__headers[header][1] + '|', end='')
          print(' ' * spaces, end='')
          print(self.__ANSICodes['endc'], end='')
          print("%2i" %(queues[header][process].getId()), end='')      
          print(' ' * spaces, end='')
          print(self.__headers[header][1] + '|', end='')
          print(self.__ANSICodes['endc'], end='')
        else:
          print(self.__headers[header][1] + '|', end='')
          print(' ' * (self.__dimensions['cellMax'] - 2), end='')
          print('|', end='')
          print(self.__ANSICodes['endc'], end='')
        if (header < 3):
          print(' ' * self.__dimensions['spaceBetween'], end='')


      print(' ' * self.__paddings['right'], end='')

    print(' ' * self.__paddings['left'], end='')
    
    for header in range(3):
      print(self.__headers[header][1] + '+', end='')
      print('-' * (self.__dimensions['cellMax'] - 2), end='')
      print('+', end='')
      print(self.__ANSICodes['endc'], end='')
      if (header < 3):
        print(' ' * self.__dimensions['spaceBetween'], end='')

    print(' ' * self.__paddings['right'])
    print('\n' * self.__paddings['bottom'])


  def __calculateDimentions (self):
    self.__terminalColumns = os.get_terminal_size().columns
    self.__terminalLines = os.get_terminal_size().lines
    


    
    remainerHSpace = self.__terminalColumns - self.__paddings['left'] - self.__paddings['right']

    cellAmount = 3
    spacesBetween = cellAmount - 1

    cellWidth = (remainerHSpace - (spacesBetween * self.__dimensions['spaceBetween'])) // cellAmount
    
    self.__dimensions['cellMax'] = self.__dimensions['cellMin'] if cellWidth <= self.__dimensions['cellMin'] else cellWidth
    if self.__dimensions['cellMax'] % 2 != 0:
      self.__dimensions['cellMax'] += 1

    self.__dimensions['spaceBetween'] = math.ceil(self.__dimensions['cellMax'] / 12)
    pass
  
