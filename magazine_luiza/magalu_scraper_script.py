# Este script faz a raspagem de dados de itens da Magazine Luiza
# E faz a exportação desses dados em um csv, para futura análise
# Autor: João Vitor Dutra Pacheco Gois

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from unidecode import unidecode

def personalizar_url(termo_de_pesquisa):
    """
    Função para pesquisar produtos e personalizar a url de pesquisa
    IN: 'smart tv 4k': str
    OUT: https://www.magazineluiza.com.br/busca/iphone 11/?page={}
    """
    template = 'https://www.magazineluiza.com.br/busca/{}/'
    termo_de_pesquisa.replace('', '+')

    # Adicionando o query string da pesquisa na URL
    url = template.format(termo_de_pesquisa)

    # Adicionando o query string da página na URL
    url += '?page={}'

    return url

def extrair_titulo_produto(produto):
    return produto.a.h2.text.strip()

def extrair_url_produto(produto):
    rota_detalhes_produto = produto.a.get('href')
    return f'https://www.magazineluiza.com.br{rota_detalhes_produto}'

def extrair_preco_produto(produto):
    try:
        preco_produto = produto.find('p', {'data-testid':'price-value'}).text.strip()
        preco_produto = unidecode(preco_produto)
        preco_produto_float = float(preco_produto.split()[-1].replace('.','').replace(',','.'))
        return preco_produto_float
    except AttributeError:
        return

def extrair_avaliacao(produto):
    return len(produto.find_all('use', {'xlink:href':'#StarIcon'}))

def extrair_quantidade_avaliacoes(produto):
    try:
        return int(produto.find('span', {'format':'count'}).text.strip())
    except AttributeError:
        return 0

def extrair_informacoes_produto(produto):
    titulo = extrair_titulo_produto(produto)
    preco = extrair_preco_produto(produto)
    avaliacao = extrair_avaliacao(produto)
    quantidade_avaliacoes = extrair_quantidade_avaliacoes(produto)
    url = extrair_url_produto(produto)

    return (titulo, preco, avaliacao, quantidade_avaliacoes, url)

def numero_ultima_pagina(url):
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-blink-features=AutomationControlled')
    driver = webdriver.Chrome(options=options, executable_path=r'C:\SeleniumDrivers\chromedriver.exe')
    driver.get(url.format(1))
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    paginas = soup.find_all('a', {'type':'page'})
    return int(paginas[-1].text)

def extrair_produtos(termo_de_pesquisa=''):
    # Instanciando o driver do navegador
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-blink-features=AutomationControlled')
    driver = webdriver.Chrome(options=options, executable_path=r'C:\SeleniumDrivers\chromedriver.exe')
    # personalizando a url com o termo de pesquisa
    url = personalizar_url(termo_de_pesquisa)
    lista_produtos = []
    for pagina in range(1, numero_ultima_pagina(url) + 1):
        driver.get(url.format(pagina))
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        resultados = soup.find_all('li', {'class':'sc-eCVOVf loRbcV'})
        for produto in resultados:
            informacao = extrair_informacoes_produto(produto)
            if informacao:
                lista_produtos.append(informacao)
    driver.close()
    return lista_produtos

if __name__ == '__main__':
    pesquisa = 'videogame'
    lista_smartphones = extrair_produtos(pesquisa)

    dataset = pd.DataFrame(lista_smartphones, columns = ['descricao', 'preco', 'avaliacao', 'quantidade_avaliacoes', 'URL'])

    dataset.to_csv(f'output/dataset_{pesquisa}.csv'.replace(' ','_'), sep=';', index = False, encoding = 'utf-8-sig')
