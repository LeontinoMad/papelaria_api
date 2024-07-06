import matplotlib.pyplot as plt
import numpy as np
import requests
import os

token = ""
usuarioNome = ""

url = "http://localhost:3000/"

def limparTerminal():
    os.system("cls")

def titulo(texto, sublinhado="-"):
  print()
  print(texto)
  print(sublinhado*40)

def login():
  titulo("Login do Usuário")

  # Login real:
#   email = input("E-mail: ")
#   senha = input("Senha.: ")

  # Login preguiçoso:
  email = "Pedro@gmail.com"
  senha = "Pedro@123"

  response = requests.post(url + "/login", 
    json={"email": email, "senha": senha}
  )

  if response.status_code != 200:
    print("Erro... Login ou Senha inválidos")
    return
  
  dados = response.json()

  # para indicar que a variável aqui atribuída é a global 
  # (e não uma nova variável criada nesta função)
  global token 
  global usuarioNome
  token = dados['token']
  usuarioNome = dados['nome']
  print(f"Bem-vindo ao sistema: {usuarioNome}")

def inclusao():
  titulo("Inclusão de Produtos")

  if token == "":
    print("Erro... Você deve logar-se primeiro")
    return

  nome = input("Nome do Produto: ")
  marca = input("Marca..........: ")
  categoria = input("Material.........: ")
  preco = float(input("Preço..: "))

  response = requests.post(url + "/produtos", 
    json={"nome": nome, "marca": marca, "categoria": categoria, "preco": preco},
    headers={"Authorization": f"Bearer {token}"}
  )

  if response.status_code == 201:
    dados = response.json()
    print(f"Ok... Produto cadastrado com o código {dados['id']}")
  else:
    print(f"Erro... Não foi possível cadastrar o produto")

def listar():
    titulo("Listagem dos Produtos Cadastrados")

    if token == "":
        print("Erro... Você deve logar-se primeiro")
        return

    response = requests.get(url + "/produtos")

    if response.status_code == 200:
      listagem = response.json()
    
      for i in range(len(listagem)):
        print()
        print   (f"Código.....: {listagem[i]['id']}")
        print   (f"Produto....: {listagem[i]['nome']}")
        print   (f"Marca......: {listagem[i]['marca']}")
        print   (f"Categoria..: {listagem[i]['categoria']}")
        print   (f"Preço......: R${listagem[i]['preco']}")

    elif response.status_code == 404:
        print("Lista não encontrada.")

def alterar():

    if token == "":
        print("Erro... Você deve logar-se primeiro")
        return

    listar()
    titulo("Alterar um ou mais Produtos Cadastrados")


    idProduto = input("Qual o id do Produto que você deseja alterar? ")

    # Valida se o ID inserido é válido
    response = requests.get(url + "/produto")
    idValido = False
    if response.status_code == 200:
        validaId = response.json()

        for i in range(len(validaId)):
            if idProduto == validaId[i]['id']:
                idValido = True

    if idValido == False:
        print("Por favor, insira um ID válido.")
        return
    
    print("Insira as informações que você deseja alterar .")
    nome = input("Nome do Produto: ")
    marca = input("Marca..........: ")
    categoria = input("Material.........: ")
    preco = float(input("Preço..: "))

    response = requests.put ((url + "/produto" + idProduto),
            json={"nome": nome, "marca": marca, "categoria": categoria, "preco": preco},
            headers={"Authorization": f"Bearer {token}"}
    )

    if response.status_code == 200:
        print()
        print(f"Sucesso! O produto {idProduto} foi alterado com sucesso!")
    else:
        print("Não foi possível alterar o produto. Tente novamente.")

def grafico():
  titulo("Gráfico comparando Categorias de Produtos")

  # Insert das Categorias:
#   categoria1 = input("1ª Categoria: ")
#   categoria2 = input("2ª Categoria: ")
#   categoria3 = input("3ª Categoria: ")

  # Insert Preguiçoso:
  categoria1 = "Escolar"
  categoria2 = "Escritorio"
  categoria3 = "Artesanal"

  response = requests.get(url + "/produtos")

  if response.status_code != 200:
    print("Erro... Não foi possível conectar com a API")
    return
  
  dados = response.json()

  countCategoria1 = 0
  countCategoria2 = 0
  countCategoria3 = 0

  for linha in dados:
    if linha['categoria'] == categoria1:
        countCategoria1 += 1
    elif linha['categoria'] == categoria2:
        countCategoria2 += 1
    elif linha['categoria'] == categoria3:
        countCategoria3 += 1



  labels = categoria1, categoria2, categoria3
  sizes = [countCategoria1, countCategoria2, countCategoria3]
#   sizes = [1, 5, 45]

  fig, ax = plt.subplots()
  def func(pct, allvals):
        print(f"PCT: {pct}")
        print(f"Allvals: {allvals}")
        teste = 1*sum(allvals)
        absolute = int(pct/100.*sum(allvals))
        print(f"Absolute: {absolute}")
        print(f"Teste: {teste}")
        return "{:d}".format(absolute)

  ax.pie(sizes, labels=labels, autopct=lambda pct: func(pct, sizes))


  plt.show()

limparTerminal()
# ----------------------------------- Programa Principal
while True:
  if token: 
    titulo(f"Cadastro de Produtos  - Usuário {usuarioNome}", "=")
  else:
    titulo("Cadastro de Produtos ", "=")
  print("1. Fazer Login")
  print("2. Incluir Produtos")
  print("3. Listar Produtos")
  print("4. Alterar Dados")
  print("5. Excluir Produto")
  print("6. Agrupar por Categoria")
  print("7. Gráfico Relacionando Faixas Etárias")
  print("8. Finalizar")
  opcao = int(input("Opção: "))
  if opcao == 1:
    login()
  elif opcao == 2:
    inclusao()
  elif opcao == 3:
    listar()
  elif opcao == 4:
    alterar()
  elif opcao == 7:
    grafico()
  elif opcao == 8:
    break
  elif opcao == 9:
    limparTerminal()
  else:
    print("Insira uma opção válida.")
