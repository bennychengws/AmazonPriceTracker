import requests
from bs4 import BeautifulSoup
import time
import smtplib
import random

# Prepare multiple user agents from https://developers.whatismybrowser.com/useragents/explore/
# Copy and paste the user agent on user_agent_list_prepared -> str
user_agent_list_prepared = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36",
]

# Search the product's code on amazon jp
# paste the code at the end of the link: https://www.amazon.co.jp/gp/product/
# Input the website link as the key of the URL_dict -> str
# Input the benchmark of the price as the value -> float/int
URL_dict = {
    "https://www.amazon.co.jp/dp/B00EVGE2FS/": 1000,
    "https://www.amazon.co.jp/gp/product/B07YY9T1FQ/": 2000,
}

# Enter the email address for logging in the email server and sending the notification email -> str
sender = ""
# Enter the email address for receiving the notification email -> str
receiver = ""
# Enter the password for the above entered email account -> str
pw = ""


def trackPrice(key):
    price = getPrice(user_agent_list_prepared, key)
    if price == -1:
        trackPrice(key)
    elif price == -2:
        pass
    else:
        wanted_price = URL_dict[key]
        if price >= wanted_price:
            diff = price - wanted_price
            print(f"It is still {diff} dollars higher than the benchmark\n")
        else:
            print("Cheaper!!")
            sendMail(key)
    
def getPrice(user_agent_list, URL):
    user_agent = random.choice(user_agent_list)
    converted_price = ""

    headers = {"User-Agent": user_agent}
    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")
    with open('test.html', 'w', encoding="utf-8") as f:
        f.write(str(soup))

    try:
        title = soup.find(id="productTitle", class_="a-size-large product-title-word-break").get_text().strip()
    except AttributeError:
        print("You may be detected by Amazon as a bot!")
        converted_price = -1
        return converted_price

    availability = soup.find(class_="a-size-medium a-color-price").get_text().strip()
    print(f"User-Agent Sent: {user_agent}")
    print(title)
    if availability == "この商品は現在お取り扱いできません。" or availability == "Currently unavailable.":
        print("Not available right now!\n")
        converted_price = -2
        return converted_price
    else:
        try:
            price = soup.find(id="priceblock_ourprice").get_text().strip()
        except AttributeError:
            price = soup.find(class_="a-size-base a-color-price").get_text().strip()
        for i in range(len(price)):
            if price[i].isnumeric():
                converted_price += price[i]
            else:
                pass 
        converted_price = float(converted_price)
        print(price)
        print(converted_price)
        return converted_price

def sendMail(key):
    subject = "Amazon Price Has Dropped!"
    body = f"Check the amazon link: {key}"
    mailtext = f"Subject: {subject}\n\n{body}"

    server = smtplib.SMTP(host="smtp.gmail.com", port=587)
    server.ehlo()
    server.starttls()
    server.login(sender, pw)
    server.sendmail(
        sender, 
        receiver, 
        mailtext
    )
    print("An email has been sent\n")
    server.quit()

def timeinterval():
    # Define the number of seconds for the sleep time of the program
    time_seconds = 300
    sign = ["+", "-"]
    if random.choice(sign) == "+":
        time_seconds = 300 + (random.random() * (200 * random.random()))
    else:
        time_seconds = 300 - (random.random() * (200 * random.random()))        
    print(f"The program will sleep for {time_seconds} seconds\n\n")
    time_requited = time.sleep(time_seconds)
    return time_requited

if __name__ == "__main__":
    while True:
        for key in URL_dict:
            try:
                trackPrice(key)
            except OSError:
                trackPrice(key)
        timeinterval()