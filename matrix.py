#!/usr/bin/python3.8 -BO

# bibliotecas:
from curses import (
   napms, initscr, init_pair, wrapper,
   A_BOLD, color_pair, start_color,
   curs_set, noecho, COLOR_BLACK,
   KEY_RESIZE, endwin, error as CursesError
)
from os import get_terminal_size, execv
from random import choice
from math import floor
from time import time
from sys import argv
from enum import IntEnum
# meus módulos:
from roleta import Roleta
from array import array as Array

# dimensões do terminal que roda tal.
terminal = get_terminal_size()
(Y,X) = terminal.lines, terminal.columns

# matriz que "pixela" tela com caractéres.
matriz = [Array('u', [' '] * X) for _ in range(Y)]

# variáveis de configuração.
# tempo para descer cada variável num mapa, onde
# quanto maior chave, menor o tempo, consequentemente
# maior a velocidade.
# definições com o programa em execução:
velocidades = {1:200, 2:100, 3:50, 4:10, 5:5, 6:3}
# visualizar barra de status?
MOSTRA_BARRA_STATUS = True
# fileiras multi-coloridas.
RAINBOW_MODE = True
# espaços entre fileiras.
FILEIRAS_ESPACOS = 4

class Velocidades(IntEnum):
   # valores significam milisegundos.
   MUITO_BAIXA = 200
   BAIXA = 100
   MEDIA_BAIXA = 50
   MEDIA_ALTA = 10
   ALTA = 5
   MUITO_ALTA = 3
...

class Referencia:
   def __init__(self, dado):
      self._dado = dado
   def retorna(self):
      return self._dado
   def altera(self, novo_valor):
      self._dado = novo_valor
   def deleta(self):
      print("destrói referência.")
      del self
   valor = property(retorna, altera, deleta, "simples referência de dado")
...


# barra de progresso da velocidade:
def barra_velocidade(velocidade):
   velocidade_atual = indice_velocidade(velocidade)
   # um pontinho para cada nível.
   barra = '.' * len(Velocidades)
   progresso = (
      barra[1:velocidade_atual]
            + '#' +
      barra[velocidade_atual:]
   )
   return '- %s +' % progresso
...

# mostra, em tempo real, a barra de status e suas configurações.
def barra_status_visor(janela, nivel, numero):
   cor = A_BOLD
   texto = 'LIN={} COLS={}'
   texto_i = 'ESPAÇOS={}'
   texto_ii = 'FILEIRAS={}'
   janela.addstr(Y-1,0, texto_i.format(FILEIRAS_ESPACOS))
   janela.addstr(Y-1, X-18,texto.format(Y,X))
   janela.addstr(Y-1, 15, barra_velocidade(nivel), cor)
   janela.addstr(Y-1, 30, texto_ii.format(numero), cor)
...

def imprime_matriz(janela):
   # imprimindo a matriz dentro do "curses".
   if RAINBOW_MODE:
      paletas = [
         color_pair(i % 7) | A_BOLD
         for i in range(X-2)
      ]
      for k in range(X-2):
         cor = paletas[k]
         for i in range(Y):
            char = matriz[i][k]
            if char.isprintable():
               janela.addch(i, k, char,cor)
            else:
               janela.addch(i, k, '#', cor)
         ...
      ...
   else:
      for i in range(Y):
         for j in range(X-2):
            cor = color_pair(3) | A_BOLD
            char = matriz[i][j]
            janela.addch(i, j, char, cor)
         ...
      ...
   ...
...

def proxima_velocidade(atual):
   indice = None
   total = len(Velocidades)
   velocidade = None
   tabela = {}

   for (i, e) in enumerate(Velocidades):
      if e is atual:
         indice = i
      ...
      tabela[i] = e
   ...

   return tabela[(indice + 1) % total]
...

def velocidade_anterior(atual):
   indice = None
   total = len(Velocidades)
   velocidade = None
   tabela = {}

   for (i, e) in enumerate(Velocidades):
      if e is atual:
         indice = i
      ...
      tabela[i] = e
   ...

   return tabela[(indice - 1) % total]
...

def indice_velocidade(v):
   for (i, e) in enumerate(Velocidades):
      if e is v:
         return (i + 1)
      ...
   ...
...

def main(janela):
   # execução da janela:
   janela = initscr()
   # configuração do 'curses'.
   start_color()
   curs_set(False)
   #curses.use_default_colors()
   noecho()

   # paletas de cores:
   for i in range(0, 8):
      init_pair(i+1, i, COLOR_BLACK)

   # dados de configuração:
   n = int(floor(X / FILEIRAS_ESPACOS))
   roletas = [
      Roleta(
         # direção para baixo ou cima
         # da 'Roleta'.
         choice([False, True]),
         FILEIRAS_ESPACOS * i,
         matriz
      )
      for i in range(1, n)
   ]
   # tecla ativida para algumans configurações.
   # não interroper loop por causa do input.
   janela.nodelay(True)

   # só "declarando" variável.
   tecla = None
   v = Referencia(Velocidades.MEDIA_BAIXA)
   # até for interrompido com o teclado, ficar
   # alternando entre as roletas, dado uma
   # limite de tempo.
   total = len(Velocidades)
   while tecla != ord('s'):
      # mudando atributos de acordo com a
      # tecla pressionada.
      controle(janela, tecla, v)
      tecla = janela.getch()

      # rolando cada tira uma vez.
      for obj in roletas:
         obj.um_deslizamento()

      janela.refresh()
      imprime_matriz(janela)
      napms(int(v.valor))

      if MOSTRA_BARRA_STATUS:
         barra_status_visor(janela, v.valor, n)
   ...

   # finalizando...
   endwin()
...

# baseado nos argumentos passados
# definir o melhor modo de execução.
def menu():
   global RAINBOW_MODE, MOSTRA_BARRA_STATUS

   if "classico" in argv or "arco-iris" in argv:
      if "classico" in argv:
         RAINBOW_MODE = False
      elif "arco-íris" in argv:
         RAINBOW_MODE = True
   ...

   if "sem-status" in argv:
      MOSTRA_BARRA_STATUS = False
...

# tomas algumas ações, ou alteras valores dado
# a tecla pressionada.
def controle(janela, tecla, v):
   # proposições:
   atingiu_teto = v.valor is not Velocidades.MUITO_ALTA
   atingiu_piso = v.valor is not Velocidades.MUITO_BAIXA

   global MOSTRA_BARRA_STATUS, RAINBOW_MODE
   if tecla == ord('+') and atingiu_teto:
      # aumenta velocidade.
      v.valor = proxima_velocidade(v.valor)
   elif tecla == ord('-') and atingiu_piso:
      # diminui velocidade.
      v.valor = velocidade_anterior(v.valor)
   elif tecla == ord('b'):
      # se estiver desativdo, então ativa.
      if not MOSTRA_BARRA_STATUS:
         MOSTRA_BARRA_STATUS = True
      else:
         MOSTRA_BARRA_STATUS = False
   elif tecla == ord('r'):
      # ativa e desativa modo arco-íris.
      if not RAINBOW_MODE:
         RAINBOW_MODE = True
      else:
         RAINBOW_MODE = False
   elif tecla == KEY_RESIZE:
      (y, x) = janela.getmaxyx()
      # reexecuta o programa, para se
      # adequar a nova dimensão.
      # terminando antigo...
      mensagem = "redimensionando no momento ...".upper()
      y = y // 2
      x = x // 2 - len(mensagem)
      n = int(floor(X / FILEIRAS_ESPACOS))
      roletas = [
         Roleta(
            # direção para baixo ou cima
            # da 'Roleta'.
            choice([False, True]),
            FILEIRAS_ESPACOS * i,
            matriz
         )
         for i in range(1, n)
      ]
      # redimensionando "roletas" idem.
      # interpletador python.
      programa = "/usr/bin/python3"
      # meu código no diretório.
      codigo = "matrix.py"
      execv(programa, ("-B", codigo))
   ...
...


# execução de testes.
if __name__ == '__main__':
   menu()
   ti = time()
   wrapper(main)
   tf = int(abs(ti - time()))

   if __debug__:
      print("\n\n")
      for v in Velocidades:
         proxima = proxima_velocidade(v)
         print(v, proxima, sep="==>")
      ...
      print("\n\n")
      for v in Velocidades:
         proxima = velocidade_anterior(v)
         print(v, proxima, sep="==>")
      ...
      print("\n\n")
   ...

   def legivel(segundos):
      if segundos >= 60 and segundos <= 3600:
         return str(segundos // 60) + "min"
      elif segundos >= 3600:
         return str(segundos // 3600) + "h"
      else:
         return "%iseg" % segundos
   ...

   print("programa finalizado.")
   print("duração de %s." % legivel(tf))
...

