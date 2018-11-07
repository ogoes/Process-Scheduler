# Simulador de algoritmos de escalonamento

Projeto para a matéria de Sistemas Operacionais
Desenvolvido por Dennis Urtubia e Otávio Goes.

Dada um conjunto de configurações de processos, o programa escrito em Python 3 efetua a simulação de algoritmos de escalonamento de processos. Foram implementados os algoritmos First Come First Served, Shortest Job First, Round Robin e Priority.  

# Execução do programa

#### Modo de execução do programa:

Primeiro passo:

```sh
$ cd Process-Scheduler
```

Segundo passo:

```sh
$ cd src
```

Terceiro passo:

```sh
$ -f ../test/file.txt
-f é seguido do diretório do caminho para o arquivo de configurações dos processos
```
```sh
$ -b 2
-b é seguido com um valor inteiro que representa o tempo de bloqueio no qual o processo se encontra quando ocorre um evento de E/S
```
```sh
$ -q 4
-q é seguido com um valor inteiro que representa o quantum para o algoritmo RoundRobin
```

```sh
Exemplo:
$ ./main.py -f ../test/file.txt -b 2 -q 4 
```
### Caso não sejam passados os valores de -b e -q será utilizado 2 e 4 respectivamente como padrão.

# License
MIT