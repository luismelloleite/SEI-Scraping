# Importação de bibliotecas necessárias
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import csv
import os
from webdriver_manager.chrome import ChromeDriverManager

# Instalação automática do ChromeDriver usando webdriver_manager
webdriver.Chrome(ChromeDriverManager().install())

# Obtém o diretório do projeto
diretorio_projeto = os.getcwd()

# Solicita ao usuário o nome da pasta para os downloads
nome_pasta = input("Digite o nome da pasta para os downloads: ")

# Verifica se o nome da pasta foi fornecido
if not nome_pasta:
    raise ValueError("O nome da pasta para downloads não foi fornecido.")

# Cria o caminho completo para o diretório de downloads
diretorio_downloads = os.path.join(diretorio_projeto, nome_pasta)

# Se o diretório de downloads não existir, cria-o
if not os.path.exists(diretorio_downloads):
    os.makedirs(diretorio_downloads)

# Configurações do Chrome para definir o diretório de downloads
opcoes_chrome = Options()
opcoes_chrome.add_experimental_option("prefs", {
    "download.default_directory": diretorio_downloads
})

# Inicializa o navegador Chrome com as opções configuradas
driver = webdriver.Chrome(options=opcoes_chrome)
driver.get("http://www.sei.ufcat.edu.br")

# Localiza os campos de usuário e senha
campo_usuario = driver.find_element(By.ID, "txtUsuario")
campo_senha = driver.find_element(By.ID, "pwdSenha")

# Informações de usuário e senha (a serem preenchidas)
usuario = input("Digite o nome de usuário: ")
senha = input("Digite a senha: ")

# Verifica se usuário e senha foram fornecidos
if not usuario or not senha:
    raise ValueError("Usuário e senha são obrigatórios.")

# Preenche os campos de usuário e senha
campo_usuario.send_keys(usuario)
campo_senha.send_keys(senha)

# Clica no botão de login
botao_login = driver.find_element(By.ID, "sbmLogin")
botao_login.click()

# Abre o arquivo CSV e lê os dados (ignora o cabeçalho)
with open(nome_pasta + '_processo.csv', 'r') as arquivo:
    leitor = csv.reader(arquivo)
    next(leitor)

    # Para cada linha no arquivo CSV
    for linha in leitor:
        # Obtém o número do processo
        numero_processo = linha[0]

        # Verifica se o número do processo foi fornecido
        if not numero_processo:
            raise ValueError("O número do processo não foi fornecido.")

        # Localiza e preenche o campo de pesquisa rápida com o número do processo
        campo_pesquisa_rapida = driver.find_element(By.ID, "txtPesquisaRapida")
        campo_pesquisa_rapida.clear()
        campo_pesquisa_rapida.send_keys(numero_processo)
        campo_pesquisa_rapida.send_keys(Keys.RETURN)

        # Aguarda implicitamente por 10 segundos
        driver.implicitly_wait(10)

        # Muda para o frame de visualização do processo
        campo_visualizacao = WebDriverWait(driver, 30).until(
            lambda d: d.find_element(By.ID, "ifrVisualizacao")
        )
        driver.switch_to.frame(campo_visualizacao)

        # Localiza o campo de árvore de ações e seus elementos
        campo_arvore_acoes = WebDriverWait(driver, 30).until(
            lambda d: d.find_element(By.XPATH, '//*[@id="divArvoreAcoes"]')
        )
        elementos = campo_arvore_acoes.find_elements(By.XPATH, "*")

        # Itera sobre os elementos da árvore de ações
        for elemento in elementos:
            outer_html = elemento.get_attribute("outerHTML")
            
            # Verifica se o elemento possui o atributo 'procedimento_gerar_zip'
            if 'procedimento_gerar_zip' in outer_html:
                # Clica no elemento
                elemento.click()

                # Aguarda a presença do botão 'btnGerar'
                btn_gerar = WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.NAME, "btnGerar"))
                )
                
                # Clica no botão 'btnGerar'
                btn_gerar.click()
                
                # Sai do loop, pois já encontrou o elemento desejado
                break

        # Retorna ao conteúdo padrão fora do frame
        driver.switch_to.default_content()

        # Localiza novamente o campo de pesquisa rápida para a próxima iteração

# Encerra o navegador
driver.quit()
