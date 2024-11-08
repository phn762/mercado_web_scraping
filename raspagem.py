import requests
from bs4 import BeautifulSoup
import time

# Define o user agent
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
}

# Solicita o produto
produto = input('Digite o produto: ')
produto = produto.replace(' ', '-')

# URL base (sem "_Desde_" para iniciar na primeira página)
url = f'https://lista.mercadolivre.com.br/{produto}_Desde_'

# Contagem inicial de página (página 1 é sem o parâmetro "_Desde_")
pagina = 1

# Loop para navegar entre as páginas
while True:
    url_final = url +str(pagina)+ '_NoIndex_True'
    
    print(f'Acessando: {url_final}')

    # Requisição
    r = requests.get(url_final, headers=headers)
    print(f'Status da requisição: {r.status_code}')
    
    # Verifica se a requisição foi bem-sucedida
    if r.status_code != 200:
        print("Erro ao acessar a página, encerrando o loop.")
        break

    # Faz o parsing do HTML
    site = BeautifulSoup(r.content, 'html.parser')

    # Extrai descrições, preços e links dos produtos
    descricoes = site.find_all('h2', class_='ui-search-item__title ui-search-item__group__element')
    precos = site.find_all('span', class_='andes-money-amount__fraction')
    links = site.find_all('a', class_='ui-search-link')

    # Verifica se há produtos na página
    if not descricoes:
        print("Não há mais produtos, encerrando o loop.")
        break

    # Imprime os resultados
    for descricao, preco, link in zip(descricoes, precos, links):
        print("Descrição:", descricao.get_text())
        print("Preço: R$", preco.get_text())
        print("Link:", link.get('href'))
        print('-' * 40)

    # Incrementa para a próxima página e faz uma pausa para evitar sobrecarga no servidor
    pagina += 50
    print('outra pagina')
    time.sleep(2)  # Pausa de 2 segundos entre as requisições
