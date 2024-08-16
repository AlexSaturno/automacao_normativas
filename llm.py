from langchain_openai import AzureChatOpenAI
from langchain.prompts import PromptTemplate

import os
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())

llm = AzureChatOpenAI(
    azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
    model=os.getenv("AZURE_OPENAI_MODEL"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    openai_api_type="azure",
)

prompt = PromptTemplate.from_template(
    """
Você analisará um arquivo pdf que contém extrações de três fontes: BACEN, SUSEP e CVM.
Analise individualmente cada fonte.
Sua resposta deve estar obrigatoriamente e somente no seguinte formato:

####
Segue anexado ao e-mail o relatório das extrações realizadas.

Resumo abaixo.

BACEN: 
    Total de {quantidade_dados_bacen} tópicos listados.
    Resumo dos tópicos: [um resumo dos assuntos]

SUSEP: 
    Total de {quantidade_dados_susep} tópicos listados.
    Resumo dos tópicos: [um resumo dos assuntos]

CVM: 
    Total de {quantidade_dados_cvm} tópicos listados.
    Resumo dos tópicos: [um resumo dos assuntos]

Obrigado!
####

Arquivo pdf: {data}
"""
)

chain = prompt | llm
