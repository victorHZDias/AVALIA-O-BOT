from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import dotenv
import base64
from langchain.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.exceptions import OutputParserException # Importar para melhor import base64

dotenv.load_dotenv()
api_key=os.getenv('GOOGLE_API')

# # Configuração da API Key (boa prática)
os.environ["GOOGLE_API_KEY"] = api_key

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

driver = webdriver.Chrome()
driver.get("https://univirtus.uninter.com/")


driver.find_element(By.ID,"ru").send_keys(input("Informe o RU"))
driver.find_element(By.ID,"senha").send_keys(input("Informe a senha"))


driver.find_element(By.ID,"loginBtn").click()

# element1 = WebDriverWait(driver, 10).until(
#     EC.presence_of_element_located((By.ID, "loginBoxProvas"))
# )
# driver.find_element(By.ID,"loginBoxProvas").click()

element = WebDriverWait(driver, 60).until(
    EC.presence_of_element_located((By.CLASS_NAME, "question"))
)

# 2. Captura de Elemento Específico
def capture_element(driver: webdriver.Chrome, element_css_selector: str, filename: str):

    try:
        # Encontra o elemento usando um seletor CSS
        element = driver.find_element(By.ID, element_css_selector)
        
        # Captura o screenshot do elemento
        element.screenshot(filename)
        print(f"✅ Screenshot do elemento salvo em: {filename}")
        return filename
    except Exception as e:
        print(f"❌ Erro ao capturar elemento: {e}")
        return None

element = WebDriverWait(driver, 60).until(
    EC.presence_of_element_located((By.XPATH, '//*[@id="navegacao"]/div[1]/button'))
)

for i in range(1,11):
    xp=f'//*[@id="navegacao"]/div[{i}]/button'
    time.sleep(0.5)
    driver.find_element(By.XPATH,xp).click()

    capture_element(driver, "viewavaliacaousuariohistorico",f"questao_{i}.jpg")

    # Example using a local image file encoded in base64
    image_file_path = f"questao_{i}.jpg"

    with open(image_file_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode("utf-8")

    message_local = HumanMessage(
        content=[
            {"type": "text", "text": "Avalie a questão na imagem e imforme qual a opção correta, não precisa descrever como chegou na resposta simeplesmente diga qual a opção correta por favor."},
            {"type": "image_url", "image_url": f"data:image/png;base64,{encoded_image}"},
        ]
    )
    result_local = llm.invoke([message_local])
    print(f"Resposta: {result_local.content}")


driver.close()