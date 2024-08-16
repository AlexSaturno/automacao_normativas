from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import datetime


def extrair_dados_susep(driver, dados_extraidos, data_limite):
    try:
        timeout = 10
        itens = WebDriverWait(driver, timeout).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".ct-book"))
        )

        for i, item in enumerate(itens, start=1):
            try:
                # Extrair o título, que está dentro da tag <a> com a classe "titulo"
                titulo_element = item.find_element(By.XPATH, ".//h3//span")
                titulo = titulo_element.text

                # Extrair a data, o tipo e a tag do texto
                # data_element = item.find_element(By.XPATH, './/dt[normalize-space()="Data de Publicação:"]/following-sibling::dd/span')
                data_str = titulo.split("de")[-1].strip()
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
                tipo_element = item.find_element(By.CLASS_NAME, f"ct-book-location")
                tipo = tipo_element.text.split(":")[-1].strip()

                # Extrair o assunto, que está dentro da tag <span> com a classe "assunto"
                assunto_element = item.find_element(
                    By.XPATH,
                    './/dt[normalize-space()="Ementa:"]/following-sibling::dd/span',
                )
                assunto = assunto_element.text.strip()

                try:
                    # Encontre o elemento <bnp-book-btn-documents>
                    button_element = item.find_element(
                        By.XPATH, ".//bnp-book-btn-documents"
                    )

                    # Verifique se há um link <a> dentro do <div>
                    try:
                        link = button_element.find_element(
                            By.XPATH, ".//div[@uk-tooltip]/a"
                        )
                        has_link = True
                    except NoSuchElementException:
                        has_link = False

                    # Verificar o estado do atributo aria-expanded
                    try:
                        tooltip_div = button_element.find_element(
                            By.XPATH, ".//div[@uk-tooltip]"
                        )
                        aria_expanded = tooltip_div.get_attribute("aria-expanded")

                        if aria_expanded == "false":
                            # Alterar o atributo aria-expanded para true usando JavaScript
                            driver.execute_script(
                                "arguments[0].setAttribute('aria-expanded', 'true');",
                                tooltip_div,
                            )
                    except NoSuchElementException:
                        aria_expanded = False
                    # Tomar ação com base nas verificações
                    if has_link:
                        # Clique no elemento se o link estiver presente e aria-expanded for true
                        link.click()
                        # Aguarde a nova aba/janela abrir
                        WebDriverWait(driver, 30).until(EC.number_of_windows_to_be(2))
                        # Troque para a nova aba/janela
                        driver.switch_to.window(driver.window_handles[1])
                        # Obtenha a URL da nova aba/janela
                        link = driver.current_url
                        # Fechar a aba atual
                        driver.close()
                        # Volte para a aba/janela original
                        driver.switch_to.window(driver.window_handles[0])
                    else:
                        link = "Não há link associado a este tópico"
                except TimeoutException:
                    link = "O elemento <bnp-book-btn-documents> não foi encontrado no tempo limite."

                dados_extraidos[titulo].append(
                    {"data": data, "assunto": assunto, "tipo": tipo, "link": link}
                )
            except Exception as e:
                print(f"Erro ao processar um item: {e}")
    except Exception as e:
        print(f"Erro ao extrair dados: {e}")
