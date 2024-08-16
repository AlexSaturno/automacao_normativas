from selenium.webdriver.common.by import By
import datetime


def extrair_dados_cvm(driver, dados_extraidos, data_limite):
    try:
        itens = driver.execute_script("return document.querySelectorAll('article')")

        for item in itens:
            try:
                # Extrair o elemento link
                link_element = item.find_element(By.TAG_NAME, "a")
                titulo = link_element.text
                link = link_element.get_attribute("href")

                # Extrair a data, o tipo e a tag do texto
                data_tipo_tag_element = item.find_element(By.CLASS_NAME, "infoItem")
                # Obtém o texto e realiza o split
                data_tipo_tag_string = data_tipo_tag_element.text
                partes = data_tipo_tag_string.split("\n")
                # Preenche as variáveis com base no comprimento da lista
                data_str = partes[0] if len(partes) > 0 else "Não foi localizada data"
                tipo = partes[1] if len(partes) > 1 else "Não foi localizado tipo"
                tag = partes[2] if len(partes) > 2 else "Não foi localizada tag"

                data_str = data_str.split(":")[-1].strip()
                # Converter a data extraída em objeto datetime
                data = datetime.datetime.strptime(
                    data_str, "%d/%m/%Y"
                )  # Ajuste o formato conforme a data no título
                # Verificar se a data é mais antiga do que a data limite
                if data < data_limite:
                    print(
                        "A data limite foi atingida na extração. Abaixo o resultado:\n"
                    )
                    return False

                # Extrair o tipo
                tipo = tipo.split(":")[-1].strip()

                # Extrair a tag
                tag = tag.split(":")[-1].strip()

                # Extrair o assunto
                assunto_element = item.find_element(By.CLASS_NAME, "contentDesc")
                assunto = assunto_element.text.strip()

                dados_extraidos[titulo].append(
                    {
                        "data": data,
                        "assunto": assunto,
                        "tipo": tipo,
                        "tag": tag,
                        "link": link,
                    }
                )
            except Exception as e:
                print(f"Erro ao processar um item: {e}")
    except Exception as e:
        print(f"Erro ao extrair dados: {e}")
