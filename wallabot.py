from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
import pickle
import os
import smtplib
from email.message import EmailMessage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

url_array_reus = ['https://es.wallapop.com/app/search?min_sale_price=40&max_sale_price=120&keywords=iphone%20X&order_by=newest&latitude=41.15214&longitude=1.1081&filters_source=default_filters&distance=30000',
             'https://es.wallapop.com/app/search?min_sale_price=50&max_sale_price=200&keywords=iphone%2011&order_by=newest&latitude=41.15214&longitude=1.1081&filters_source=default_filters&distance=30000',
             'https://es.wallapop.com/app/search?min_sale_price=100&max_sale_price=250&keywords=iphone%2011%20pro&order_by=newest&latitude=41.15214&longitude=1.1081&filters_source=default_filters&distance=30000',
             'https://es.wallapop.com/app/search?min_sale_price=100&max_sale_price=320&keywords=iphone%2011%20pro%20max&order_by=newest&latitude=41.15214&longitude=1.1081&filters_source=default_filters&distance=30000',
             'https://es.wallapop.com/app/search?min_sale_price=150&max_sale_price=320&keywords=iphone%2012&order_by=newest&latitude=41.15214&longitude=1.1081&filters_source=default_filters&distance=30000',
             'https://es.wallapop.com/app/search?min_sale_price=200&max_sale_price=420&keywords=iphone%2012%20pro&order_by=newest&latitude=41.15214&longitude=1.1081&filters_source=default_filters&distance=30000',
             'https://es.wallapop.com/app/search?min_sale_price=250&max_sale_price=450&keywords=iphone%2012%20pro%20max&order_by=newest&latitude=41.15214&longitude=1.1081&filters_source=default_filters&distance=30000',
             'https://es.wallapop.com/app/search?min_sale_price=300&max_sale_price=430&keywords=iphone%2013&order_by=newest&latitude=41.15214&longitude=1.1081&filters_source=default_filters&distance=30000',
             'https://es.wallapop.com/app/search?min_sale_price=300&max_sale_price=500&keywords=iphone%2013%20pro&order_by=newest&latitude=41.15214&longitude=1.1081&filters_source=default_filters&distance=30000',
             'https://es.wallapop.com/app/search?min_sale_price=300&max_sale_price=600&keywords=iphone%2013%20pro%20max&order_by=newest&latitude=41.15214&longitude=1.1081&filters_source=default_filters&distance=30000',
             'https://es.wallapop.com/app/search?min_sale_price=250&max_sale_price=400&keywords=iphone%2013%20mini&order_by=newest&latitude=41.15214&longitude=1.1081&filters_source=default_filters&distance=30000']

url_array_esp = ['https://es.wallapop.com/app/search?min_sale_price=40&max_sale_price=100&keywords=iphone%20X&order_by=newest&latitude=40.41955&longitude=-3.69196&filters_source=default_filters',
             'https://es.wallapop.com/app/search?min_sale_price=50&max_sale_price=180&keywords=iphone%2011&order_by=newest&latitude=40.41955&longitude=-3.69196&filters_source=default_filters',
             'https://es.wallapop.com/app/search?min_sale_price=100&max_sale_price=250&keywords=iphone%2011%20pro&order_by=newest&latitude=40.41955&longitude=-3.69196&filters_source=default_filters',
             'https://es.wallapop.com/app/search?min_sale_price=100&max_sale_price=300&keywords=iphone%2011%20pro%20max&order_by=newest&latitude=40.41955&longitude=-3.69196&filters_source=default_filters',
             'https://es.wallapop.com/app/search?min_sale_price=150&max_sale_price=300&keywords=iphone%2012&order_by=newest&latitude=40.41955&longitude=-3.69196&filters_source=default_filters',
             'https://es.wallapop.com/app/search?min_sale_price=200&max_sale_price=420&keywords=iphone%2012%20pro&order_by=newest&latitude=40.41955&longitude=-3.69196&filters_source=default_filters',
             'https://es.wallapop.com/app/search?min_sale_price=250&max_sale_price=450&keywords=iphone%2012%20pro%20max&order_by=newest&latitude=40.41955&longitude=-3.69196&filters_source=default_filters',
             'https://es.wallapop.com/app/search?min_sale_price=250&max_sale_price=430&keywords=iphone%2013&order_by=newest&latitude=40.41955&longitude=-3.69196&filters_source=default_filters',
             'https://es.wallapop.com/app/search?min_sale_price=250&max_sale_price=500&keywords=iphone%2013%20pro&order_by=newest&latitude=40.41955&longitude=-3.69196&filters_source=default_filters',
             'https://es.wallapop.com/app/search?min_sale_price=300&max_sale_price=600&keywords=iphone%2013%20pro%20max&order_by=newest&latitude=40.41955&longitude=-3.69196&filters_source=default_filters',
             'https://es.wallapop.com/app/search?min_sale_price=250&max_sale_price=400&keywords=iphone%2013%20mini&order_by=newest&latitude=40.41955&longitude=-3.69196&filters_source=default_filters']

iphone_index = {
    "0": "iphonex",
    "1": "iphone11",
    "2": "iphone11pro",
    "3": "iphone11promax",
    "4": "iphone12",
    "5": "iphone12pro",
    "6": "iphone12promax",
    "7": "iphone13",
    "8": "iphone13pro",
    "9": "iphone13promax",
    "10": "iphone13mini"
}

def scrapeOffers(driver, e):
    offers_found = []
    sleep(3)
    elements = driver.find_elements(By.TAG_NAME, 'a')
    if(elements is not None):
        for i in elements:
            try:
                precio = i.find_element(By.CLASS_NAME, 'ItemCard__price').text
                titulo = i.find_element(By.CLASS_NAME, 'ItemCard__title').text.lower()
                enlace = i.get_attribute('href')
                id = enlace.split('-')[-1]
                titulo_nospaces = titulo.replace(" ", "")
                if iphone_index[str(e)] in titulo_nospaces:
                    offers_found.append({'ID': id,'TITULO': titulo, 'PRECIO': precio, 'LINK': enlace})
                    #print('- TÍTULO: {} --> PRECIO: {} --> LINK: {} --> ID: {}'.format(titulo,precio,enlace,id))
            except:
                pass
    print(len(offers_found))
    return offers_found

def sendEmail(result, i):
    myEmail = 'jolete1964@gmail.com'
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    msg = EmailMessage()
    msg.set_content(result)
    if(i == 0):
        msg['Subject'] = '*New iPhone/s Found in REUS*'
        print('Email Sent for Reus!')
    else:
        msg['Subject'] = '*New iPhone/s Found in SPAIN*'
        print('Email Sent for Spain!')
    msg['From'] = myEmail
    msg['To'] = myEmail
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(myEmail, 'eiaisfgwblvkuxhw')
    server.send_message(msg)
    server.quit()

if __name__=="__main__":
    offersToSend = []
    data = []
    options = webdriver.ChromeOptions()
    options.add_argument("log-level=3")
    options.add_experimental_option('detach', True)
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    driver = webdriver.Chrome(options=options)
    for i in range(2):
        already_read = False
        for e in range(len(iphone_index)):
            if(i == 0):
                filename = 'offers.pickle'
                driver.get(url_array_reus[e])
            else:
                filename = 'offersglobal.pickle'
                driver.get(url_array_esp[e])
            if(i==0 and e==0):
                    sleep(1)
                    accept_terms_button = driver.find_element(By.ID,'onetrust-accept-btn-handler')
                    if(accept_terms_button is not None):
                        accept_terms_button.send_keys(Keys.RETURN)
            offers = scrapeOffers(driver, e)
            if os.path.exists(filename):
                with open(filename, 'rb') as f:
                    while not already_read:
                        try:
                            line = pickle.load(f)
                        except EOFError:
                            break
                        else:
                            data.append(line)
                    already_read = True
                    for offer in offers:
                        if offer['ID'] not in data:
                            offersToSend.append(offer)
                            with open(filename, 'ab') as f:
                                pickle.dump(offer['ID'], f, pickle.HIGHEST_PROTOCOL)
            else:
                with open(filename, 'ab') as f:
                    for m in offers:
                        pickle.dump(m['ID'], f, pickle.HIGHEST_PROTOCOL)
                offersToSend = offers
        result = ['- TÍTULO: {} --> PRECIO: {} --> LINK: {}'.format(n['TITULO'],n['PRECIO'],n['LINK']) for n in offersToSend]
        if result:
            sendEmail('\n\n'.join(result), i)
    driver.quit()