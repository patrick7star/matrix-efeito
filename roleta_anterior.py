import random, string
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
		str0 += random.choice("".join(opcoes))
	return str0

# uma string com espaços em branco formada de 
# forma aleatória.
def string_branca_CA():
	return " " * random.randint(5, 18)

# roleta que simula uma string infinita, rolando pela 
# matriz, sendo está uma representação da tela.
class Roleta:
# construtor.
   def __init__(self,  direcao, coluna, matriz):
      def strings_longas():
         i, _str = 1, ""
         while i <= 10:
            _str += (string_branca_CA()+string_aleatoria(30) + 
            string_branca_CA() + string_aleatoria(20) + 
            string_branca_CA())
            i += 1
         return _str
      # string com quantia pre-definida de caractéres.
      self.str0 = strings_longas()
      # define se a string vai para cima
      # ou para baixo. Verdadeiro, para cima
      # "falso" para baixo.
      self.direcao = direcao
      # coluna onde girar a string.
      self.coluna = coluna
      # posição.
      self.p = 0
      # matriz que onde será impressa.
      self.matriz = matriz
      # computando suas dimensões...
      self.Y, self.X = len(matriz), len(matriz[0])

	# realiza um, e apenas um deslizamento de coluna.
   def um_deslizamento(self):
      Y = self.Y
      if self.direcao:
         i = 0
         for c in self.str0[self.p:Y+self.p]: 
            self.matriz[i][self.coluna] = c
            i+=1
      else:
         i = Y - 1
         for c in self.str0[self.p:(Y+self.p)]: 
            self.matriz[i][self.coluna] = c 
            i -= 1
      # ir com o límite indexador da esquerda, uma posição a 
      #frente, ou seja, a direita.
      self.p += 1
      # voltando do começo novamente..
      if self.p / len(self.str0) >= 0.95: self.p = 0
