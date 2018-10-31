def ordenaId (processos):
  for i in range( len(processos)-1 ):
    j = i + 1
    while j > 0 and processos[j].getId() < processos[j-1].getId():
      aux = processos[j]
      processos[j] = processos[j-1]
      processos[j-1] = aux
      j -= 1

  return processos

def ordenaTempoChegada (processos):
  
  for i in range( len(processos)-1 ):
    j = i + 1
    while j > 0 and processos[j].getBegin() < processos[j-1].getBegin():
      aux = processos[j]
      processos[j] = processos[j-1]
      processos[j-1] = aux
      j -= 1

  return processos

def ordenaPrioridade (processos):
  for i in range( len(processos)-1 ):
    j = i + 1
    while j > 0 and processos[j].getPriori() > processos[j-1].getPriori():
      aux = processos[j]
      processos[j] = processos[j-1]
      processos[j-1] = aux
      j -= 1

  return processos
  
def ordenaTamanho (processos):
  for i in range( len(processos)-1 ):
    j = i + 1
    while j > 0 and processos[j].getTamanho() < processos[j-1].getTamanho():
      aux = processos[j]
      processos[j] = processos[j-1]
      processos[j-1] = aux
      j -= 1
  return processos
  