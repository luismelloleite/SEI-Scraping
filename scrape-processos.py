# Importação de bibliotecas necessárias
import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

# Configurações para executar o navegador em modo "headless" (sem interface gráfica)
chrome_options = Options()
chrome_options.add_argument("--headless")

# Inicialização do navegador Chrome
driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

# URL do SEI! desejado (insira a URL no campo vazio)
url_sei = ""
if not url_sei:
    raise ValueError("A URL do SEI! não foi fornecida.")

driver.get(url_sei)

# Localização e preenchimento dos campos de usuário e senha
campo_usuario = driver.find_element(By.ID, 'txtUsuario')
campo_senha = driver.find_element(By.ID, 'pwdSenha')
usuario = ''
senha = ''

if not usuario or not senha:
    raise ValueError("Usuário e senha são obrigatórios.")
    
campo_usuario.send_keys(usuario)
campo_senha.send_keys(senha)

# Clique no botão de login
botao_login = driver.find_element(By.ID, 'sbmLogin')
botao_login.click()

# Preenchimento do campo de pesquisa rápida e seleção da opção de pesquisa de processos
campo_pesquisa_rapida = driver.find_element(By.ID, "txtPesquisaRapida")
campo_pesquisa_rapida.send_keys("")
campo_pesquisa_rapida.send_keys(Keys.RETURN)
opcao_pesquisar_processos = driver.find_element(By.CSS_SELECTOR, "input#optProcessos")
opcao_pesquisar_processos.click()

# Interagir com o campo de unidade geradora
campo_unidade_geradora = driver.find_element(By.CSS_SELECTOR, "input#txtUnidade")
campo_unidade_geradora.click()
nome_unidade_geradora = ""

if not nome_unidade_geradora:
    raise ValueError("O nome da unidade geradora é obrigatório.")

# Preenchimento gradual do campo de unidade geradora
for char in nome_unidade_geradora:
    campo_unidade_geradora.send_keys(char)
    time.sleep(0.5)

# Seleção da opção e pressionar teclas TAB
campo_unidade_geradora.send_keys(Keys.ARROW_DOWN)
campo_unidade_geradora.send_keys(Keys.ENTER)
campo_unidade_geradora.send_keys(Keys.TAB)

# Clique no botão de pesquisa
botao_pesquisar = driver.find_element(By.ID, 'sbmPesquisar')
botao_pesquisar.click()

# Aguardar implicitamente por 5 segundos
driver.implicitly_wait(5)

# Loop para extrair dados de todas as páginas
while True:
    # Localizar elementos na página
    divInfraAreaTelaD = driver.find_element(By.XPATH, '//*[@id="divInfraAreaTelaD"]')
    conteudo = driver.find_element(By.XPATH, '//*[@id="conteudo"]')
    tabelas = conteudo.find_elements(By.CLASS_NAME, "resultado")
    nome_csv = nome_unidade_geradora + "_processo.csv"

    # Escrever dados em um arquivo CSV
    with open(nome_csv, mode='a', newline='') as arquivo:
        escrever = csv.writer(arquivo)
        for tabela in tabelas:
            td_elemento = tabela.find_element(By.CLASS_NAME, "resTituloEsquerda")
            texto = td_elemento.text
            texto_formatado = texto[-20:]
            escrever.writerow([texto_formatado])

    try:
        # Tentar encontrar e clicar no link "Próxima"
        next_link = driver.find_element(By.XPATH, '//span[@class="pequeno"]/a[contains(text(), "Próxima")]')
        next_link.click()
    except NoSuchElementException:
        # Se não houver mais páginas, encerrar o navegador e imprimir "Sucesso"
        driver.quit()
        print("Sucesso")
        break

# Finalizar o programa
exit()
