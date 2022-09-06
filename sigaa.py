from __future__ import print_function
from distutils.command.config import config
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.common.by import By

options = webdriver.ChromeOptions()
options.add_argument("--headless")
navegador = webdriver.Chrome(chrome_options=options)
navegador.get("https://sig.cefetmg.br/sigaa/verTelaLogin.do")
try:
    navegador.find_element(
        By.XPATH, '//*[@id="conteudo"]/div[4]/form/table/tbody/tr[1]/td/input'
    ).send_keys("12610740689")
    navegador.find_element(
        By.XPATH, '//*[@id="conteudo"]/div[4]/form/table/tbody/tr[2]/td/input'
    ).send_keys("310505Mateus")
    navegador.find_element(
        By.XPATH, '//*[@id="conteudo"]/div[4]/form/table/tfoot/tr/td/input'
    ).click()
except:
    navegador.find_element(
        By.XPATH, '//*[@id="conteudo"]/div[5]/form/table/tbody/tr[1]/td/input'
    ).send_keys("12610740689")
    navegador.find_element(
        By.XPATH, '//*[@id="conteudo"]/div[5]/form/table/tbody/tr[2]/td/input'
    ).send_keys("310505Mateus")
    navegador.find_element(
        By.XPATH, '//*[@id="conteudo"]/div[5]/form/table/tfoot/tr/td/input'
    ).click()
    navegador.find_element(By.XPATH, '//*[@id="fechar-painel-erros"]/a').click()


def abre_boletim():
    # Exibir nota de cada matéria separadamente
    # A ideia era poder apresentar a porcentagem de aproveitamento em cada matéria a partir das notas já lançadas
    # no estilo notas do aluno/total de pontos já distribuídos, mas os professores não organizam essa área de forma
    # padronizada. Fica como desafio pra outro momento
    # navegador.find_element(
    #     By.XPATH, '//*[@id="form_acessarTurmaVirtualj_id_1"]/a').click()
    # navegador.find_element(
    #     By.XPATH, '//*[@id="formMenu:j_id_jsp_311393315_88"]/div[1]').click()
    # navegador.find_element(
    #     By.XPATH, '//*[@id="formMenu:j_id_jsp_311393315_88"]/div[3]/table/tbody/tr/td/a[3]').click()

    # Exibir boletim
    ensino = navegador.find_element(
        By.XPATH,
        '//*[@id="menu_form_menu_discente_j_id_jsp_161879646_98_menu"]/table/tbody/tr/td[1]',
    )
    emitir_boletim = navegador.find_element(
        By.XPATH, '//*[@id="cmSubMenuID1"]/table/tbody/tr[1]'
    )
    ActionChains(navegador).move_to_element(ensino).click(emitir_boletim).perform()
    navegador.find_element(By.XPATH, '//*[@id="form"]/table/tbody/tr[3]/td[3]').click()
    linhas_tabela = len(
        navegador.find_elements(By.XPATH, '//*[@id="relatorio"]/table[3]/tbody/tr')
    )
    dicio = {}
    for i in range(3, linhas_tabela):

        path = '//*[@id="relatorio"]/table[3]/tbody/tr[' + str(i) + "]/td[1]"
        materia = navegador.find_element(By.XPATH, path).text.split("- ")[1]
        colunas = '//*[@id="relatorio"]/table[3]/tbody/tr[' + str(i) + "]/td"
        #   print(materia + "   -   " )
        notas = navegador.find_elements(By.XPATH, colunas)
        soma = 0.0
        for s in range(1, 5):
            if notas[s].text != "-":

                notas[s] = notas[s].text.replace(",", ".")
                notas[s] = float(notas[s])
                soma += notas[s]
        dicio[materia] = soma
    dicio["faltas"] = navegador.find_element(
        By.XPATH, '//*[@id="relatorio"]/table[4]/tbody/tr[1]/td[2]'
    ).text
    # print(navegador.find_element(By.XPATH, colunas +
    #       '[2]').text, navegador.find_element(By.XPATH, colunas + '[3]').text)
    return dicio


def pega_atividades():
    itens = navegador.find_elements(
        By.XPATH, '//*[@id="avaliacao-portal"]/table/tbody/tr'
    )
    dicio = {}
    for i in range(1, len(itens) + 1):
        estado = navegador.find_element(
            By.XPATH, '//*[@id="avaliacao-portal"]/table/tbody/tr[' + str(i) + "]/td[1]"
        ).accessible_name
        if estado == "":
            atividade = navegador.find_element(
                By.XPATH,
                '//*[@id="avaliacao-portal"]/table/tbody/tr['
                + str(i)
                + "]/td[3]/small",
            ).text
            materia = atividade.split("-")
            enunciado = atividade.split(": ")
            data = navegador.find_element(
                By.XPATH,
                '//*[@id="avaliacao-portal"]/table/tbody/tr[' + str(i) + "]/td[2]",
            ).text
            data = data.split("(")[0]
            atividade = materia[0] + ":\n" + enunciado[1]

            dicio[atividade] = data
    return dicio


# print(pega_atividades(), abre_boletim())
