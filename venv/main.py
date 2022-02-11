import requests
import time
import json
import datetime
from bs4 import BeautifulSoup

import secrets
from twilio.rest import Client

bb_data_prefix = "https://www.bestbuy.ca/ecomm-api/availability/products?accept=application%2Fvnd.bestbuy.standardproduct.v1%2Bjson&accept-language=en-CA&locations=946|948|32%7C948%7C32&postalCode=R3L0H1&skus="
bb_site_prefix = "https://www.bestbuy.ca/en-ca/product/"

#All the real products we want:
bb_pages = ["15689336"]


#The poduct website prefix
pagePrefix = "https://www.memoryexpress.com/Products/"

validTestProductCode = "MX00117188" #Links to some simple RAM that is (most likely) in stock!

#All the real products we want:
pages = ["MX00116013","MX00117476","MX00117931","MX00118491","MX00117403","MX00116063",
         "MX00116071","MX00116072","MX00117588","MX00117402","MX00116164","MX00116154",
         "MX00118344","MX00117401","MX00116163","MX00117400","MX00115013","MX00118026",
         "MX00117683","MX00118342","MX00114926"]

page = requests.get(pagePrefix+"MX00116013")
#print(page.status_code)
#print(page.content)

def check_item_in_stock(pagelink):
    page_html = requests.get(pagelink, headers=secrets.headers)
    soup = BeautifulSoup(page_html.content, 'html.parser')
    #out_of_stock_divs = soup.find_all("span", class_="c-capr-inventory-store__availability InventoryState_OutOfStock")
    #store_stock_divs = soup.find("div", class_="c-capr-inventory-store")
    #store_names = soup.find_all("span", class_="c-capr-inventory-store__name")

    store_list = soup.find("li", {"data-region-name": "Manitoba"})

    possibleOutOfStock = store_list.findChildren("span", class_="c-capr-inventory-store__availability InventoryState_OutOfStock")

    #print(store_list)
    #print(possibleOutOfStock)

    return len(possibleOutOfStock) == 0

def bb_check_item_in_stock(packet):

    response = requests.get(packet, headers=secrets.headers)
    response_formatted = json.loads(response.content.decode('utf-8-sig').encode('utf-8'))

    status = response_formatted['availabilities'][0]['pickup']['status']
    purchasable = response_formatted['availabilities'][0]['pickup']['purchasable']

    out_str = ""

    if not purchasable or status == "ComingSoon":
        # Out Of stock
        print("\tNo Stock Found, Status=" + status)
    else:
        out_str = '\nStatus=' + status + "\n\nPurchasable=" + str(purchasable)
        locations = response_formatted['availabilities'][0]['pickup']['locations']
        if len(locations) > 0:
            out_str += "\n\nLocations="
            for l in locations:
                out_str += "\n" + l['name'] + ":" + str(l['quantityOnHand']) + ","
        else:
            out_str += "No Location Data - "

        print(out_str)

    return out_str

def get_item_name(pagelink):
    page_html = requests.get(pagelink, headers=secrets.headers)
    soup = BeautifulSoup(page_html.content, 'html.parser')

    store_list = soup.find("h1")

    return store_list.text.strip()


def send_email(user, pwd, recipient, subject, body):
    import smtplib

    FROM = user
    TO = recipient if isinstance(recipient, list) else [recipient]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % ("memoryexpresscrawler@gmail.ca", ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(user, pwd)
        server.sendmail(FROM, TO, message)
        server.close()
        print ("successfully sent the mail")
    except:
        print ("failed to send mail")

#send_email(secrets.usr, secrets.password, secrets.usr, "GPU IN STOCK", "Does this work?")

def setup_twilio_client():
    account_sid = secrets.TWILIO_ACCOUNT_SID
    auth_token = secrets.TWILIO_AUTH_TOKEN
    return Client(account_sid, auth_token)

def send_notification(msg):
    twilio_client = setup_twilio_client()
    twilio_client.messages.create(
        body=msg,
        from_=secrets.TWILIO_FROM_NUMBER,
        to=secrets.MY_PHONE_NUMBER
    )

#send_notification("This is a test Twilio Message!")

#print(check_item_in_stock(page))
#print("NEW PRODUCT IN STOCK:   %s    LINK: %s" % (get_item_name(page),page))

#send_notification("\n\nNEW PRODUCT IN STOCK:\n\n%s\n\nLINK:\n%s" % (get_item_name(page), pagePrefix+"MX00116013"))

def gpu_checker():
    while True:
        #try:
        #    mem_checker()
        #except:
        #    print("Error with mem_checker()")
        try:
            bestbuy_checker()
        except:
            print("Error with bestbuy_checker()")

        print("Pausing...")
        time.sleep(180)

def mem_checker():
    print("Checking Memory Express Stock Now")
    for p in pages:
        time.sleep(5)
        pagelink = pagePrefix + p
        print("\tChecking:%s %s" % (get_item_name(pagelink), pagelink))
        if (check_item_in_stock(pagelink)):
            print("NEW PRODUCT IN STOCK")
            send_notification("\nNEW PRODUCT IN STOCK:\n\n%s\n\nLINK:\n%s" % (get_item_name(pagelink), pagelink))
            pages.remove(p)

def bestbuy_checker():
    print("Checking Best Buy Stock Now")
    for p in bb_pages:

        page_real_link = bb_site_prefix + p
        page_link = bb_data_prefix + p
        print("\tChecking:%s" % (get_item_name(page_real_link)))
        out_str = bb_check_item_in_stock(page_link)

        if out_str != "":
            print("NEW PRODUCT IN STOCK: " + page_real_link)
            send_notification("\nNEW PRODUCT IN STOCK:\n\n%s\n\nLINK:\n%s\n\nREADOUT:%s" % (get_item_name(page_real_link),page_real_link,out_str))
            bb_pages.remove(p)
        time.sleep(5)



gpu_checker()
