import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options

import chromedriver_autoinstaller

import time

chromedriver_autoinstaller.install()

chrome_options = Options()
chrome_options.add_argument("--headless")

driver = webdriver.Chrome(options=chrome_options)
driver.get("http://www.sei.ufg.br")
#link_sei = input("Link do SEI que deseja acessar: ")
#driver.get(link_sei)

campo_usuario = driver.find_element(By.ID, 'txtUsuario')
campo_senha = driver.find_element(By.ID, 'pwdSenha')

#usuario = input(Nome de usuário: )
#senha = input(Digite de senha: )
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

#nome_unidade_geradora = input("Nome da Unidade Geradora: ")
nome_unidade_geradora = "CDIRH-RC"
for char in nome_unidade_geradora:
    campo_unidade_geradora.send_keys(char)
    time.sleep(0.5)
campo_unidade_geradora.send_keys(Keys.ARROW_DOWN)
campo_unidade_geradora.send_keys(Keys.ENTER)
campo_unidade_geradora.send_keys(Keys.TAB)

# Pesquisa Unidade Geradora

botao_pesquisar = driver.find_element(By.ID, 'sbmPesquisar')
botao_pesquisar.click()

#SALVA OS PROCESSOS EM CSV
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