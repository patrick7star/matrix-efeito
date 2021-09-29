# biblioteca do Python:
from random import randint, choice
import string
# minha biblioteca:
from lista_circular import ListaCircular
# cria e retorna string com tal comprimento
# de caractéres.
def string_aleatoria(comprimento):
	str0 = ''
	opcoes = [x for x in string.__dict__.keys() if not x.startswith('_')] 
	opcoes.remove('Formatter')
	opcoes.remove('Template')
	# adicionando alfabeto grego.
	opcoes.append(''.join([chr(v) for v in range(0x03a9,0x03b1)]))
	# adicionando alfabetos arábes.
	opcoes.append("".join([chr(v) for v in range(0x0620,0x64A)]))
	# adicionando alfabeto japonês.
	#opcoes.append("".join([chr(v) for v in range(0x30a1, 0x30fb)]))
	for i in range(comprimento):
		str0 += choice("".join(opcoes))
	return str0

# uma string com espaços em branco formada de 
# forma aleatória.
def string_branca_CA():
	return " " * randint(5, 18)

def string_longa():
   i, _str = 1, ""
   while i <= 10:
      _str += (string_branca_CA()+string_aleatoria(30) + 
             string_branca_CA() + string_aleatoria(20) + 
             string_branca_CA())
      i += 1
   return _str

# roleta que simula uma string infinita, rolando pela 
# matriz, sendo está uma representação da tela.
class Roleta:
# construtor.
   def __init__(self,  direcao, coluna, matriz):
      # string com quantia pre-definida de caractéres.
      # também colocando a string na "lista circular".
      #self.str0 = strings_longas()
      self.lista = ListaCircular()
      for c in string_longa(): self.lista.adicionar(c)
      # define se a string vai para cima
      # ou para baixo. Verdadeiro, para cima
      # "falso" para baixo.
      self.direcao = direcao
      # coluna onde girar a string.
      self.coluna = coluna
      # endereço da matriz.
      self.matriz = matriz
      # computa dimensão da "tela"
      self.Y,self.X = len(matriz),len(matriz[0])
   # realiza um, e apenas um deslizamento de coluna.
   def um_deslizamento(self):
      substr = str(self.lista)[0:self.Y-1]
      # colocando na atual coluna da matriz
      # até preenche-la.
      for i, c in zip(range(self.Y), substr):
         self.matriz[i][self.coluna] = c
      if self.direcao: self.lista.girar()
      else: self.lista.girar_inverso()
