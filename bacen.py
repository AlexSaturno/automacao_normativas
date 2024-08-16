from selenium.webdriver.common.by import By


def extrair_dados_bacen(driver, dados_extraidos):
    try:
        itens = driver.find_elements(By.CSS_SELECTOR, "li.resultado-item")

        for item in itens:
            try:
                link_element = item.find_element(By.TAG_NAME, "a")
                titulo = link_element.text.strip()
                link = link_element.get_attribute("href")

                texto_item = item.text

                data = (
                    texto_item.split("Data/Hora Documento:")[-1]
                    .split("Assunto:")[0]
                    .strip()
                )
                assunto = (
                    texto_item.split("Assunto:")[-1].split("Responsável:")[0].strip()
                )
                responsavel = (
                    texto_item.split("Responsável:")[-1].strip()
                    if "Responsável:" in texto_item
                    else "Responsável não encontrado"
                )

                dados_extraidos[titulo].append(
                    {
                        "data": data,
                        "assunto": assunto,
                        "responsavel": responsavel,
                        "link": link,
                    }
                )
            except Exception as e:
                print(f"Erro ao processar um item: {e}")
    except Exception as e:
        print(f"Erro ao extrair dados: {e}")
