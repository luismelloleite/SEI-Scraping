import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

import time

chrome_options = Options()
chrome_options.add_argument("--headless")

driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
#driver.get("http://www.sei.ufcat.edu.br")
driver.get("") # Adicione aqui o link do SEI! desejado.


campo_usuario = driver.find_element(By.ID, 'txtUsuario')
campo_senha = driver.find_element(By.ID, 'pwdSenha')

usuario = ''
senha = ''
campo_usuario.send_keys(usuario)
campo_senha.send_keys(senha)

botao_login = driver.find_element(By.ID, 'sbmLogin')
botao_login.click()

campo_pesquisa_rapida = driver.find_element(By.ID, "txtPesquisaRapida")
campo_pesquisa_rapida.send_keys("")
campo_pesquisa_rapida.send_keys(Keys.RETURN)

opcao_pesquisar_processos = driver.find_element(By.CSS_SELECTOR, "input#optProcessos")
opcao_pesquisar_processos.click()

campo_unidade_geradora = driver.find_element(By.CSS_SELECTOR, "input#txtUnidade")
campo_unidade_geradora.click()

nome_unidade_geradora = "CDIRH-RC"
for char in nome_unidade_geradora:
    campo_unidade_geradora.send_keys(char)
    time.sleep(0.5)
campo_unidade_geradora.send_keys(Keys.ARROW_DOWN)
campo_unidade_geradora.send_keys(Keys.ENTER)
campo_unidade_geradora.send_keys(Keys.TAB)

botao_pesquisar = driver.find_element(By.ID, 'sbmPesquisar')
botao_pesquisar.click()

driver.implicitly_wait(5)

while True:
    divInfraAreaTelaD = driver.find_element(By.XPATH, '//*[@id="divInfraAreaTelaD"]')
    conteudo = driver.find_element(By.XPATH, '//*[@id="conteudo"]')
    tabelas = conteudo.find_elements(By.CLASS_NAME, "resultado")
    nome_csv = nome_unidade_geradora + "_processo.csv"

    with open(nome_csv, mode='a', newline='') as arquivo:
        escrever = csv.writer(arquivo)
        for tabela in tabelas:
            td_elemento = tabela.find_element(By.CLASS_NAME, "resTituloEsquerda")
            texto = td_elemento.text
            texto_formatado = texto[-20:]
            escrever.writerow([texto_formatado])

    try:
        next_link = driver.find_element(By.XPATH, '//span[@class="pequeno"]/a[contains(text(), "Próxima")]')
        next_link.click()
    except NoSuchElementException:
        driver.quit()
        print("Sucesso")
        break
exit()
