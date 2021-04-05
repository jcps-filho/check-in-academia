import re
import os.path
import telegram_send
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.headless = True
driver = webdriver.Chrome("C:\\Users\\Home\\Downloads\\chromedriver.exe", chrome_options=options)
print('Acessando site da academia')
driver.get("https://www.sevenacademia.com.br/")
print('Obtendo link do formulário de check-in')
elem = driver.find_element_by_id("comp-kasly63l4")

match = re.search(r'href=[\'"]?([^\'" >]+)', elem.get_attribute('innerHTML'))
if match:
    print(match.group(1))
    print('Acessando formulario')
    driver.get(match.group(1))
    print('Obtendo data do formulario')
    checkInDate = driver.title.split(' ')[1]
    driver.quit()
    if os.path.isfile("C:\\Users\\Home\\Desktop\\Check-in-academia\\ultimadata.txt"):
        arquivo = open("C:\\Users\\Home\\Desktop\\Check-in-academia\\ultimadata.txt", "r")
        ultimaData = arquivo.readline(10)
        print('Verificando se a notificação já foi enviada hoje')
        if(ultimaData != checkInDate):
            print('Enviando notificação')
            telegram_send.send(messages=['Check-in do dia '+ checkInDate + ' diponivel!'])
            arquivo.close()
            print('Atualização do arquivo de ultima data')
            arquivo = open("C:\\Users\\Home\\Desktop\\Check-in-academia\\ultimadata.txt", "w")
            arquivo.write(checkInDate)
            arquivo.close()
            exit()
        else:
            arquivo.close()
            print('A notificação já foi enviada hoje \n')
            print('Encerrando...')
            exit()
    else:
        print('Enviando notificação')
        telegram_send.send(messages=['Check-in do dia '+ checkInDate + ' diponivel!'])
        arquivo = open("ultimadata.txt", "w")
        arquivo.write(checkInDate)
        arquivo.close()
        exit()