#!/usr/bin/python3.8

# bibliotecas:
import os, string, time, sys, curses
from random import choice
import math
# meus módulos:
#from lista_circular import ListaCircular
#from roleta import Roleta
from roleta_anterior import Roleta

# dimensões do terminal que roda tal.
terminal = os.get_terminal_size()
(Y,X) = terminal.lines, terminal.columns

# matriz que "pixela" tela com caractéres.
matriz = [[' ' for i in range(X)] for j in range(Y)]

# variáveis de configuração.
# tempo para descer cada variável num mapa, onde
# quanto maior chave, menor o tempo, consequentemente
# maior a velocidade.
# definições com o programa em execução:
velocidades = {1:200, 2:100, 3:50, 4:10, 5:5, 6:3}
mostra_barra_status = True # visualizar barra de status?
rainbow_mode = True # fileiras multi-coloridas.
# definições ao iniciar o programa:
unica_direcao = False# fileiras vão numa única direção.
fileiras_espacos = 4 # espaços entre fileiras.

# barra de progresso da velocidade:
def barra_velocidade(velocidade_atual):
   barra = '.' * len(velocidades) # um pontinho para cada nível.
   progresso = barra[1:velocidade_atual] + '#' + barra[velocidade_atual:]
   return '- %s +' % progresso

# mostra, em tempo real, a barra de status e suas configurações.
def barra_status_visor(janela, nivel,numero):
   cor = curses.A_BOLD
   texto = 'LIN={} COLS={}'
   texto_i = 'ESPAÇOS={}'
   texto_ii = 'FILEIRAS={}'
   janela.addstr(Y-1,0, texto_i.format(fileiras_espacos))
   janela.addstr(Y-1, X-18,texto.format(Y,X))
   janela.addstr(Y-1, 15, barra_velocidade(nivel), cor)
   janela.addstr(Y-1, 30, texto_ii.format(numero), cor)

def imprime_matriz(janela):
   # imprimindo a matriz dentro do "curses".
   if rainbow_mode:
      _paletas = [curses.color_pair(i % 7)| curses.A_BOLD 
                  for i in range(X-2)]
      for k in range(X-2):
         cor = _paletas[k]
         for i in range(Y): janela.addch(i,k,matriz[i][k],cor)
   else:
      for i in range(Y):
         for j in range(X-2): 
            cor = curses.color_pair(3) | curses.A_BOLD
            janela.addch(i,j,matriz[i][j],cor) 

def main(janela):
   global mostra_barra_status, unica_direcao
   # execução da janela:
   janela = curses.initscr() # criando uma janela.
   curses.start_color() # inicializando cores do sistema.
   curses.curs_set(False) # desabilitando cursor.
   #curses.use_default_colors()
   curses.noecho() # tirando echo ao digitar.

   # paletas de cores:
   for i in range(0, 8): 
      curses.init_pair(i+1,i,curses.COLOR_BLACK)

   # dados de configuração:
   n = int(math.floor(X / fileiras_espacos))
   # lista com roletas.
   if unica_direcao:
      para_baixo = choice([False, True]) # direção original?
      roletas = [Roleta(para_baixo, (fileiras_espacos*i),matriz) 
                 for i in range(1, n)]
   else:
      roletas = [Roleta(choice([False,True]), (fileiras_espacos*i),
                        matriz) 
                 for i in range(1,n)]
   # tecla ativida para algumans configurações.
   janela.nodelay(True) # não interroper loop por causa do input.
   tecla,v = -1, 3 # só "declarando" variável.
   # até for interrompido com o teclado, ficar
   # alternando entre as roletas, dado uma 
   # limite de tempo.
   while tecla != ord('s'):
      # alterando as configurações:
      if tecla == ord('+') and v <= len(velocidades)-1: 
         v += 1 # aumenta velocidade.

      elif tecla == ord('-') and v > 1: 
         v-=1 # diminui velocidade.

      elif tecla == ord('b'): 
         # se estiver desativdo, então ativa.
         if not mostra_barra_status: 
            mostra_barra_status = True
         else: mostra_barra_status = False

      elif tecla == ord('r'):
         # ativa e desativa modo arco-íris.
         global rainbow_mode
         if not rainbow_mode: 
            rainbow_mode = True
         else: 
            rainbow_mode = False

      elif tecla == curses.KEY_RESIZE:
         # executa o programa, para se 
         # adequar a nova dimensão.
         curses.napms(600)
         # terminando antigo...
         curses.endwin() 
         # interpletador python.
         programa = "/usr/bin/python3"
         # meu código no diretório.
         codigo = "./matrix.py"
         os.execv(programa, ("-B", codigo,))

      tecla = janela.getch() # obtendo entrada.
      for obj in roletas: 
         obj.um_deslizamento()
      janela.refresh() # atualizando tela.
      imprime_matriz(janela) # imprime matriz.
      # pausa(definindo velocidade)
      curses.napms(velocidades[v])       
      # atual dimensão do terminal na tela.
      if mostra_barra_status: 
         barra_status_visor(janela,v,n)
   curses.endwin() # finalizando...

# execução de testes.
if __name__ == '__main__':
   curses.wrapper(main)
   print("programa finalizado.")

