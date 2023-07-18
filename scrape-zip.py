from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import csv
import os
import chromedriver_autoinstaller

chromedriver_autoinstaller.install()
diretorio_projeto = os.getcwd()

nome_pasta = input("Digite o nome da pasta para os downloads: ")

diretorio_downloads = os.path.join(diretorio_projeto, nome_pasta)

if not os.path.exists(diretorio_downloads):
    os.makedirs(diretorio_downloads)

opcoes_chrome = Options()
opcoes_chrome.add_experimental_option("prefs", {
    "download.default_directory": diretorio_downloads
})

driver = webdriver.Chrome(options=opcoes_chrome)
driver.get("http://www.sei.ufg.br")

campo_usuario = driver.find_element(By.ID, "txtUsuario")
campo_senha = driver.find_element(By.ID, "pwdSenha")

usuario = ''
senha = ''
campo_usuario.send_keys(usuario)
campo_senha.send_keys(senha)

botao_login = driver.find_element(By.ID, "sbmLogin")
botao_login.click()

with open(nome_pasta + '_processo.csv', 'r') as arquivo:
    leitor = csv.reader(arquivo)
    next(leitor)

    for linha in leitor:
        numero_processo = linha[0]

        campo_pesquisa_rapida = driver.find_element(By.ID, "txtPesquisaRapida")
        campo_pesquisa_rapida.clear()
        campo_pesquisa_rapida.send_keys(numero_processo)
        campo_pesquisa_rapida.send_keys(Keys.RETURN)

        driver.implicitly_wait(10)

        campo_visualizacao = WebDriverWait(driver, 30).until(
            lambda d: d.find_element(By.ID, "ifrVisualizacao")
        )
        driver.switch_to.frame(campo_visualizacao)
        campo_arvore_acoes = WebDriverWait(driver, 30).until(
            lambda d: d.find_element(By.XPATH, '//*[@id="divArvoreAcoes"]')
        )
        elementos = campo_arvore_acoes.find_elements(By.XPATH, "*")
        for elemento in elementos:
            outer_html = elemento.get_attribute("outerHTML")
            #if 'href' in outer_html and 'zip' in outer_html:
            if 'procedimento_gerar_zip' in outer_html:
                elemento.click()
                btn_gerar = WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.NAME, "btnGerar"))
                )
                btn_gerar.click()
                break

        driver.switch_to.default_content()

        campo_pesquisa_rapida = driver.find_element(By.ID, "txtPesquisaRapida")

    driver.quit()