

""" 
Ao invés de usar simbolos Unicode aleatórios,
usa o armazem de códigos já feitos, de outros
programas, e até este aqui.
"""

from os import getenv
from os.path import join
from glob import glob
from random import choice, randint

# "armazém" com todos códigos em Python
# no computador.
CAMINHO = join(getenv("HOME"),"Documents/códigos")

# pega arquivo e, cria grande string com
# seus códigos.
def espaguetifica(arquivo):
   linhas = []
   for linha in arquivo:
      linha = linha.strip("\n\r")
      linha = linha.strip("\r")
      linhas.append(linha)
      espaco = randint(10, 27) * ' '
      linhas.append(espaco)
   ...
   arquivo.close()
   return linhas
...

def string_codigo_aleatoria():
   arquivos = glob(join(CAMINHO, "*/*.py"))
   escolha = choice(arquivos)
   if __debug__:
      from os.path import basename
      nome = basename(escolha)
      print("\nnome do arquivo: '%s'" % nome, end="\n\n")
   caracteres = espaguetifica(open(escolha, "rt"))
   return "".join(caracteres)
...


if __name__ == "__main__":
   print(string_codigo_aleatoria())
