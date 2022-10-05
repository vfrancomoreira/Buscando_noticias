from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

# Pesquisando

pesquisa = input('Digite a pesquisa: ')

print('Iniciando a pesquisa')
time.sleep(2)

driver = webdriver.Edge('D:\\edgedriver_win64\\msedgedriver.exe')
driver.get('https://www.google.com')

campo = driver.find_element_by_xpath("//input[@aria-label='Pesquisar']") # Buscando pela propriedade arial-label
campo.send_keys(pesquisa) # Enviando o texto digitado pelo usuário
campo.send_keys(Keys.ENTER) # Simula a tecla ENTER

# Recuperando a quantidade de resultados encontrados
resultados = driver.find_element_by_xpath("//div[@id='result-stats']").text
print(resultados)

# Recuperando números de paginas
numeros_resultados = int(resultados.split('Aproximadamente ')[1].split(' resultados')[0].replace('.',''))
max_paginas = numeros_resultados / 10
pagina_alvo = input(f'{max_paginas} páginas encontradas, até qual página quer ir?:')

# Navegando entre as páginas do GOOGLE
url_pagina = driver.find_element_by_xpath("//a[@aria-label='Page 2']").get_attribute("href")

pagina_atual = 0
start = 10
lista_resultados = []

while pagina_atual <= int(pagina_alvo) - 1:
    if pagina_atual == 0:
        url_pagina = url_pagina.replace("start=%s" % start, "start=%s" % (start + 10))
        start += 10
        driver.get(url_pagina)
    elif pagina_atual == 1:
        driver.get(url_pagina)
    pagina_atual += 1

    divs = driver.find_elements_by_xpath("//div[@class='g']") # 'elements' porque é uma lista
    for div in divs:
        nome = div.find_element_by_tag_name("h3")
        link = div.find_element_by_tag_name("a")
        resultado = f"SITE: {nome.text}; LINK: {link.get_attribute('href')}"
        print(resultado)
        lista_resultados.append(resultado)

with open('resultados.txt', 'w') as arquivo:
    for resultado in lista_resultados:
        arquivo.write(f'{resultado}\n')
    arquivo.close()

print(f'{len(lista_resultados)} resultados encontrados do Google e salvos no arquivo resultados.txt')

driver.close()
