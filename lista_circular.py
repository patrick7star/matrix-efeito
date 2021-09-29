
# Tentando uma implementação própria da
# estrutura de dados "lista ligada circular".

# item que a lista armazena, ele aceita apenas uma
# string de um único caractére.
class Item:
   def __init__(self, dado):
      # dado que o item carrega.
      self.dado = dado
      # seta que endereça outro item, ou nenhum.
      self.seta = None
   def __str__(self):
      return str(self.dado)
   # habilitando a concatenação de strings.
   def __add__(self, _str):
      if type(_str) == str:
         return str(self.dado) + _str
      elif type(_str) == Item:
        return str(self.dado) + str(_str)
      else: raise Exception("aceita apenas concatenação(à esquerda)")
   def __radd__(self, _str):
      if type(_str) == str:
         return str(self.dado)+_str
      elif type(_str) == Item:
         return str(self.dado) + str(_str)
      else: raise Exception("aceita apenas concatenação(à direita)")
   def __repr__(self):
      return str(self.dado)

class ListaCircular:
   # operadores de sobrecarga.
   def __init__(self):
      # endereçador do primeiro elemento.
      self.comeco = None
      # contador de elementos.
      self.qtd = 0
   # retorna a quantia de itens da lista.   
   def __len__(self):
      return self.qtd
   # adiciona um item a lista circular,
   # no começo, o caso.
   def adicionar(self, *dados):
      if len(dados) == 1:
         i = Item(dados[0])
         if self.qtd == 0:
            self.comeco = i
         elif self.qtd == 1:
            self.comeco.seta = i
            i.seta = self.comeco
         else:
            atual = self.comeco
            while atual.seta != self.comeco:
               atual = atual.seta
            i.seta = self.comeco
            self.comeco = i
            atual.seta = self.comeco
         self.qtd += 1
      else:
         for x in dados: self.adicionar(x)
      pass
   # gira a posição do primeiro objeto endereçado
   # para um objeto adiante.
   def girar(self):
      """ faz giro da roleta no sentido anti-horário"""
      atual = self.comeco
      while atual.seta != self.comeco:
         atual = atual.seta
      #atual.seta = self.comeco
      self.comeco = atual
   def girar_inverso(self):
      """ faz giro da roleta no sentido horário."""
      # último nó. 
      no_seguinte = self.comeco.seta
      self.comeco = no_seguinte

   # mostra/converte dados da lista em string. 
   def __str__(self):
      if self.qtd == 0: return ''
      else:
         string, q = "", 1
         atual = self.comeco
         while q <= self.qtd:
            string += str(atual)
            atual = atual.seta
            q += 1
         return string
   # indexa um tal elemento da lista.
   def __getitem__(self, indice):
      I = self.comeco # referência o primeiro.
      for i in range(self.qtd):
         if i == indice: return I # endereço do atual item-índice.
         I = I.seta # um adiante.
   def __repr__(self):
      return self.__str__()

if __name__ == '__main__':
   LC1 = ListaCircular()
   for x in 'abcde':
      LC1.adicionar(x)
      print(LC1)
   print("girando no sentido anti-horário...")
   LC1.girar()
   print(LC1)
   LC1.girar()
   print(LC1)
   LC1.girar()
   print(LC1)
   LC1.girar()
   print(LC1)
   LC1.girar()
   print(LC1)

   # inverso.
   print("girando no sentido horário...")
   LC1.girar_inverso()
   print(LC1)
   LC1.girar_inverso()
   print(LC1)
   LC1.girar_inverso()
   print(LC1)
   LC1.girar_inverso()
   print(LC1)
   LC1.girar_inverso()
   print(LC1)














