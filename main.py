from collections import defaultdict
import time
import datetime
from utils import *
from llm import chain
from bacen import extrair_dados_bacen
from susep import extrair_dados_susep
from cvm import extrair_dados_cvm

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime
import json


class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        return super().default(obj)


# ==================================================
# BACEN
# ==================================================
def bacen_extraction():
    hoje = datetime.datetime.today()
    quantidade_dias_atras = hoje - datetime.timedelta(days=1)
    contador_paginas = 1

    url = f"https://www.bcb.gov.br/estabilidadefinanceira/buscanormas?dataInicioBusca={formatar_data(quantidade_dias_atras)}&dataFimBusca={formatar_data(hoje)}&tipoDocumento=Todos"

    driver = configurar_driver()
    driver.get(url)
    time.sleep(10)  # Aguarda o carregamento da página

    dados_extraidos = defaultdict(list)

    extrair_dados_bacen(driver, dados_extraidos)

    while True:
        try:
            proxima_pagina = driver.find_element(
                By.CSS_SELECTOR, "li.page-item a[aria-label='Próxima']"
            )
            proxima_pagina.click()
            time.sleep(10)  # Aguarda o carregamento da nova página
            extrair_dados_bacen(driver, dados_extraidos)
            contador_paginas += 1
        except Exception as e:
            mensagem_erro = str(e)
            if "no such element" in mensagem_erro:
                print(
                    f"Não foi possível encontrar o botão de próxima página. Total de páginas: {contador_paginas}\n"
                )
            else:
                print(
                    f"Ocorreu um erro ao tentar clicar no botão de próxima página: {e}"
                )
            break

    driver.quit()

    quantidade_dados_extraidos = len(dados_extraidos.values())
    return dados_extraidos, quantidade_dados_extraidos


# ==================================================
# SUSEP
# ==================================================
def susep_extraction():
    ainda_tem_itens = True
    hoje = datetime.datetime.today()
    quantidade_dias_atras = hoje - datetime.timedelta(days=1)
    contador_paginas = 1

    url = f"https://www2.susep.gov.br/safe/bnportal/internet/pt-BR/search?exp=%22%7B2024-2024%7D%22%2Fanodoc"

    driver = configurar_driver()
    driver.get(url)
    time.sleep(30)  # Aguarda o carregamento da página

    dados_extraidos = defaultdict(list)
    ainda_tem_itens = extrair_dados_cvm(driver, dados_extraidos, quantidade_dias_atras)

    while ainda_tem_itens == True:
        try:
            print(f"Contador de páginas: {contador_paginas}")
            # Encontre o botão "Próxima" usando um seletor CSS específico
            proxima_pagina = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//*[@id="paginacao"]/li[4]/button[text()="Próxima"]')
                )
            )
            proxima_pagina.click()
            time.sleep(30)  # Aguarda o carregamento da nova página
            ainda_tem_itens = extrair_dados_susep(
                driver, dados_extraidos, quantidade_dias_atras
            )
            contador_paginas += 1
        except Exception as e:
            mensagem_erro = str(e)
            if "no such element" in mensagem_erro:
                print(
                    f"Não foi possível encontrar o botão de próxima página. Total de páginas: {contador_paginas}"
                )
            else:
                print(
                    f"Ocorreu um erro ao tentar clicar no botão de próxima página: {e}"
                )
            break

    driver.quit()

    quantidade_dados_extraidos = len(dados_extraidos.values())
    return dados_extraidos, quantidade_dados_extraidos


# ==================================================
# CVM
# ==================================================
def cvm_extraction():
    ainda_tem_itens = True
    hoje = datetime.datetime.today()
    quantidade_dias_atras = hoje - datetime.timedelta(days=1)
    contador_paginas = 1

    url = f"https://conteudo.cvm.gov.br/legislacao/index.html?numero=&lastNameShow=&lastName=&filtro=todos&dataInicio=01%2F04%2F2024&dataFim={formatar_data(hoje)}&categoria0=%2Flegislacao%2Finstrucoes%2F&categoria1=%2Flegislacao%2Fpareceres-orientacao%2F&categoria2=%2Flegislacao%2Fdeliberacoes%2F&categoria3=%2Flegislacao%2Fdecisoesconjuntas%2F&categoria4=%2Flegislacao%2Foficios-circulares%2F&categoria5=%2Flegislacao%2Fleis-decretos%2F&categoria6=%2Flegislacao%2Fnotas-explicativas%2F&buscado=false&contCategoriasCheck=7"

    driver = configurar_driver()
    driver.get(url)
    time.sleep(10)  # Aguarda o carregamento da página

    dados_extraidos = defaultdict(list)

    total_paginas_element = driver.find_element(By.CLASS_NAME, "spacePage")
    total_paginas = int(total_paginas_element.text.split("/")[-1].strip())

    ainda_tem_itens = extrair_dados_cvm(driver, dados_extraidos, quantidade_dias_atras)

    while ainda_tem_itens == True:
        try:
            if contador_paginas >= total_paginas:
                ainda_tem_itens = False
                continue

            print(f"Contador de páginas: {contador_paginas}")
            # Encontre o botão "Próxima" usando um XPATH específico
            proxima_pagina = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//*[@id="paginacao"]/li[4]/button[text()="Próxima"]')
                )
            )
            proxima_pagina.click()
            time.sleep(30)  # Aguarda o carregamento da nova página
            ainda_tem_itens = extrair_dados_cvm(
                driver, dados_extraidos, quantidade_dias_atras
            )
            contador_paginas += 1
        except Exception as e:
            mensagem_erro = str(e)
            if "no such element" in mensagem_erro:
                print(
                    f"Não foi possível encontrar o botão de próxima página. Total de páginas: {contador_paginas}\n"
                )
            else:
                print(
                    f"Ocorreu um erro ao tentar clicar no botão de próxima página: {e}"
                )
            break

    driver.quit()

    quantidade_dados_extraidos = len(dados_extraidos.values())
    return dados_extraidos, quantidade_dados_extraidos


if __name__ == "__main__":
    dados_bacen, quantidade_dados_bacen = bacen_extraction()
    dados_susep, quantidade_dados_susep = susep_extraction()
    dados_cvm, quantidade_dados_cvm = cvm_extraction()

    dados_completos = {"BACEN": dados_bacen, "SUSEP": dados_susep, "CVM": dados_cvm}

    hoje = datetime.datetime.today()
    nome_arquivo_pdf = f"extracao_{hoje.day:02}_{hoje.month:02}_{hoje.year:04}.pdf"
    salvar_em_pdf(dados_completos, nome_arquivo_pdf)

    destinatario = "carlos.quinteiro@safra.com.br,joao.sena@safra.com.br,denise.siqueira@safra.com.br,ccosta.ricardo@safra.com.br,alexander.saturno@safra.com.br,fabio.panunto@safra.com.br,eric.rocha@safra.com.br"
    assunto = "Relatório de Extração de Dados"

    # Convert the dictionary to a JSON string to pass as a single parameter
    dados_completos_str = json.dumps(
        dados_completos, ensure_ascii=False, indent=4, cls=DateTimeEncoder
    )
    corpo_email = chain.invoke(
        {
            "data": dados_completos_str,
            "quantidade_dados_bacen": quantidade_dados_bacen,
            "quantidade_dados_susep": quantidade_dados_susep,
            "quantidade_dados_cvm": quantidade_dados_cvm,
        }
    )
    print(corpo_email.content)

    enviar_email(True, destinatario, assunto, corpo_email.content, nome_arquivo_pdf)
