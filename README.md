# Simulador de algoritmos de escalonamento

Projeto para a matéria de Sistemas Operacionais
Desenvolvido por Dennis Urtubia e Otávio Goes.

Dada um conjunto de configurações de processos, o programa escrito em Python 3 efetua a simulação de algoritmos de escalonamento de processos. Foi implementados os algoritmos First Come First Served, Shortest Job First, Round Robin e Priority.  

# Execução do programa

#### Modo de execução do programa:

Primeiro passo:

```sh
$ cd pasta-do-projeto
```

Segundo passo:

```sh
$ cd src
```

Terceiro passo:

```sh
$ ./main.py ./main.py -f ../test/file.txt -b  -q 
```
###### Onde -b é seguido com um valor inteiro que representa o tempo de bloqueio no qual o processo se encontra quando ocorre um evento de E/S e -q é o valor do quantum para o algoritmo RoundRobin

# License
MIT