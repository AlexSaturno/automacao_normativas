# ----------------------------------
# Selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# ----------------------------------
# PDF
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit
import textwrap

# ----------------------------------
# E-mail genérico
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import smtplib

# ----------------------------------
# # Outlook
# import win32com.client as win32


# # Função para enviar email pelo Outlook
# def enviar_email_outlook(destinatario, assunto, corpo, caminho_arquivo):
#     outlook = win32.Dispatch("outlook.application")
#     mail = outlook.CreateItem(0)  # 0: olMailItem
#     mail.To = destinatario
#     mail.Subject = assunto
#     mail.Body = corpo

#     # Adiciona o anexo
#     mail.Attachments.Add(caminho_arquivo)

#     # Envia o e-mail
#     try:
#         mail.Send()
#     except Exception as e:
#         print(f"Erro ao enviar e-mail: {e}")


def enviar_email(com_anexo, destinatario, assunto, corpo, caminho_arquivo):
    # Configurações do servidor SMTP (exemplo com Gmail)
    smtp_server = "smtp.gmail.com"  # "smtp.office365.com"
    smtp_port = 587
    remetente = "ccosta.ricardo@gmail.com"
    senha = "ddrj kcaz yevd ycqw"
    # remetente = "normativas.hml@gmail.com"
    # senha = "ozxx msoj ijai ziqi"

    # Cria o objeto de mensagem
    mensagem = MIMEMultipart()
    mensagem["From"] = remetente
    mensagem["To"] = destinatario
    mensagem["Subject"] = assunto

    # Anexa o corpo do e-mail
    mensagem.attach(MIMEText(corpo, "plain"))

    # Anexa o arquivo PDF
    with open(caminho_arquivo, "rb") as anexo:
        parte = MIMEApplication(anexo.read(), _subtype="pdf")
        parte.add_header(
            "Content-Disposition", f"attachment; filename={caminho_arquivo}"
        )
        mensagem.attach(parte)

    # Envia o e-mail
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as servidor:
            servidor.starttls()  # Inicia a conexão segura
            servidor.login(remetente, senha)  # Faz login no servidor
            servidor.sendmail(remetente, destinatario.split(","), mensagem.as_string())
            print("E-mail enviado com sucesso!")
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")


def salvar_em_pdf(dados, nome_arquivo):
    """Recebe todos os dados extraídos e o nome do arquivo a ser salvo. E salva em um arquivo de PDF"""
    c = canvas.Canvas(nome_arquivo, pagesize=A4)
    largura, altura = A4
    margem_esquerda = 40
    margem_direita = largura - 40
    y = altura - 40
    linha_altura = 15
    fonte_padrao = "Helvetica"
    fonte_negrito = "Helvetica-Bold"

    for fonte, dados_fonte in dados.items():
        c.setFont(fonte_negrito, 14)
        c.drawString(margem_esquerda, y, f"Fonte: {fonte}")
        y -= 20

        if not dados_fonte:  # Verifica se não há dados para a fonte
            c.setFont(fonte_padrao, 12)
            c.drawString(margem_esquerda, y, "Sem extrações no período.")
            y -= 20
            if y < 50:
                c.showPage()
                y = altura - 40
            continue

        for topico, itens in dados_fonte.items():
            c.setFont(fonte_negrito, 12)
            c.drawString(margem_esquerda, y, f"Tópico: {topico}")
            y -= 20

            for item in itens:
                for chave, valor in item.items():
                    texto = f"{chave.capitalize()}: {valor}"
                    linhas = simpleSplit(
                        texto, fonte_padrao, 10, margem_direita - margem_esquerda
                    )
                    for linha in linhas:
                        c.setFont(fonte_padrao, 10)
                        if len(linha) > largura:
                            wrap_text = textwrap.wrap(linha, width=(int(largura) - 6))
                            c.drawString(margem_esquerda, y, wrap_text[0])
                            c.drawString(margem_esquerda, y, wrap_text[1])
                            y -= 2 * linha_altura
                        else:
                            c.drawString(margem_esquerda, y, linha)
                            y -= linha_altura
                        if y < 50:  # Se a página estiver cheia, criar nova página
                            c.showPage()
                            y = altura - 40

                c.drawString(margem_esquerda, y, "-" * 80)
                y -= 20

                if y < 50:  # Se a página estiver cheia, criar nova página
                    c.showPage()
                    y = altura - 40

    c.save()


def formatar_data(d):
    """Função para formatar a data no formato DD/MM/YYYY"""
    return f"{d.day:02d}/{d.month:02d}/{d.year}"


def configurar_driver():
    """Função para configurar o WebDriver do Selenium para Google Chrome"""
    ### Local ###
    # chrome_options = Options()
    # chrome_options.add_argument(
    #     "--headless"
    # )  # Executa o navegador em modo headless (sem interface gráfica)
    # service = Service(
    #     r"C:\Users\alexa\.wdm\drivers\chromedriver\win64\122.0.6261.128\chromedriver-win32\chromedriver.exe"
    # )
    # return webdriver.Chrome(service=service, options=chrome_options)

    ### VM ###
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")  # Melhor para headless
    chrome_options.add_argument(
        "--no-sandbox"
    )  # Para evitar alguns problemas de sandbox em sistemas baseados em Linux

    service = Service(r"/usr/lib/chromium-browser/chromedriver")
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.set_page_load_timeout(2500)
    return driver
