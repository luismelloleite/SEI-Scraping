# Scripts de Automação SEI!

Este repositório contém scripts em Python para automatizar tarefas no Sistema Eletrônico de Informações (SEI!), utilizando a biblioteca Selenium.

## Script 1: scrape-processos.py

### Propósito

Automatiza a pesquisa de processos no SEI!, extraindo informações relevantes e salvando-as em um arquivo CSV.

### Como Usar

1. **Configurar o Selenium WebDriver e Acessar o SEI!**
   - Instale as bibliotecas: selenium, webdriver_manager.
     ```bash
     pip install csv selenium webdriver_manager
     ```
   - Configure o WebDriver e acesse o SEI! fornecendo o link desejado.

2. **Autenticar no SEI!**
   - Forneça suas credenciais e faça login.

3. **Pesquisar Processos**
   - Realize a pesquisa preenchendo os campos necessários.

4. **Extrair Dados e Gerar CSV**
   - Extraia dados da página, formate-os e salve-os em um arquivo CSV, navegando por várias páginas.

## Script 2: scrape-zip.py

### Propósito

Automatiza o download de documentos associados aos processos do SEI!, com base em um arquivo CSV.

### Como Usar

1. **Configurar o Selenium WebDriver e Acessar o SEI!**
   - Instale as bibliotecas: selenium, webdriver_manager.
     ```bash
     pip install csv selenium webdriver_manager
     ```
   - Configurar o Diretório de Downloads
     - Forneça um nome de pasta para os downloads e configure as opções do Chrome.

2. **Autenticar no SEI!**
   - Forneça suas credenciais e faça login.

3. **Baixar Processos**
   - Leia os números dos processos no arquivo CSV e faça o download dos documentos, alternando entre frames.

**Observação:**
Certifique-se de ter as bibliotecas Python necessárias instaladas antes de executar os scripts. Além disso, configure os scripts com o link SEI! específico e credenciais antes da execução.

---
