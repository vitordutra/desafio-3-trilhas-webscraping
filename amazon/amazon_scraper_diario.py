import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from datetime import date
from webdriver_manager.chrome import ChromeDriverManager

def get_url(pesquisa):
    url = f'https://www.amazon.com.br/s?k={pesquisa}&i=electronics&__mk_pt_BR=ÅMÅŽÕÑ&ref=nb_sb_noss_1'
    pesquisa = pesquisa.replace(' ','+')
        
    # adicionando pagina para url
    url += '&page={}'
    
    return url

def extraindo_dados(item):
    
    card = {}
    
    # adicionando descrição
    atag = item.h2.a
    card['Descrição'] = atag.text.strip()
    
    try:
        # adicionando preco
        prince_parent = item.find('span','a-price')
        card['Preço'] = " ".join(prince_parent.find('span','a-offscreen').text.split())

        # ignorando produto caso não tenha preço
    except AttributeError:
        return 
    
    try:
        # adicionando estrlas e total de reviews
        card['Estrelas'] = item.i.text
        card['TotalReviews'] = item.find('span',{'class':'a-size-base'}).text
    
        # caso não tenha estrela e review no produto, definir com vázio
    except AttributeError:
        card['Estrelas'] = 0
        card['TotalReviews'] = 0

    # definindo url
    card['Url'] = 'https://www.amazon.com.br'+atag.get('href')


    card['Data'] = date.today()

    return card

def main(pesquisa):
    
    # Ativando webdriver
    driver = webdriver.Chrome(ChromeDriverManager().install())
    
    cards = []
    url = get_url(pesquisa)

    # Obtendo total de paginas
    driver.get(url)
    soup_sl = BeautifulSoup(driver.page_source, 'html.parser')
    list_pages = soup_sl.find('ul',{'class':'a-pagination'}).findAll('li')
    list_pages.pop()
    list_pages.pop(0)
    total_pages = int(list_pages[-1].getText())
    print(f'total de páginas = {total_pages}')
    
    # passando por todas as páginas
    for page in range(total_pages):
        driver.get(url.format(page+1))
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        results = soup.find_all('div',{'data-component-type':'s-search-result'})
        
        for item in results:
            card = extraindo_dados(item)
            if card:
                cards.append(card)
         
        # Caso pagina tenha mais que 50 paginas, parar na 50        
        if(page==1):
            break
                
    driver.close()
    
    #Salvando dados em csv com pandas
    dataset = pd.DataFrame(cards)
    dataset.to_csv(f'output/dataset_{pesquisa}_date.csv'.replace(' ','_'), sep=';',index = False, encoding = 'utf-8-sig')

main('smartphone')
main('notebook')
