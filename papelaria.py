import matplotlib.pyplot as plt
import numpy as np
import requests

token = ""
usuarioNome = ""

def titulo(texto, sublinhado="-"):
  print()
  print(texto)
  print(sublinhado*40)

def login():
  titulo("Login do Usuário")

  email = input("E-mail: ")
  senha = input("Senha.: ")

  response = requests.post("http://localhost:3000/login", 
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

  response = requests.post("http://localhost:3000/produtos", 
    json={"nome": nome, "marca": marca, "categoria": categoria, "preco": preco},
    headers={"Authorization": f"Bearer {token}"}
  )

  if response.status_code == 201:
    dados = response.json()
    print(f"Ok... Produto cadastrado com o código {dados['id']}")
  else:
    print(f"Erro... Não foi possível cadastrar o produto")

def grafico():
  titulo("Gráfico comparando Categorias de Produtos")

  categoria1 = input("1ª Categoria: ")
  categoria2 = input("2ª Categoria: ")
  categoria3 = input("3ª Categoria: ")

  # (): significa que é uma tupla (característica: é imutável)
  faixas = ("Escolar", "Escritorio", "Artesanal")
  # {}: significa que é um dicionário (chave: valor)
  produtos = {
      categoria1: [0, 0, 0],
    #   categoria2: [0, 0, 0],
    #   categoria3: [0, 0, 0],
  }

  response = requests.get("http://localhost:3000/produtos")

  if response.status_code != 200:
    print("Erro... Não foi possível conectar com a API")
    return
  
  dados = response.json()

#  print(dados)

  for linha in dados:
    if linha['categoria'] == categoria1:
      if linha['categoria'] == 'Escolar':
        produtos[categoria1][0] += 1
    #   elif linha['categoria'] <= 10:
        # produtos[categoria1][1] += 1          
      else:
        produtos[categoria1][2] += 1   
    elif linha['categoria'] == categoria2:
      if linha['categoria'] == 'Escritorio':
        produtos[categoria2][0] += 1
    #   elif linha['categoria'] <= 10:
        # produtos[categoria2][1] += 1          
      else:
        produtos[categoria2][2] += 1   
    elif linha['categoria'] == categoria3:
      if linha['categoria'] == 'Artesanal':
        produtos[categoria3][0] += 1
    #   elif linha['categoria'] <= 10:
        # produtos[categoria3][1] += 1          
      else:
        produtos[categoria3][2] += 1   
          

  x = np.arange(len(faixas))  # the label locations
  width = 0.25  # the width of the bars
  multiplier = 0

  fig, ax = plt.subplots(layout='constrained')

  for attribute, measurement in produtos.items():
      offset = width * multiplier
      rects = ax.bar(x + offset, measurement, width, label=attribute)
      ax.bar_label(rects, padding=3)
      multiplier += 1

  # Add some text for labels, title and custom x-axis tick labels, etc.
  ax.set_ylabel('Quantidades')
  ax.set_title('Gráfico comparando Categorias de Produtos')
  ax.set_xticks(x + width, faixas)
  ax.legend(loc='upper left', ncols=3)
  ax.set_ylim(0, 5)

  plt.show()

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
  elif opcao == 7:
    grafico()
  else:
    break
