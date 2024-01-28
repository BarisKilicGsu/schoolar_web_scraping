from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from bs4 import BeautifulSoup

def setup():
    options = Options()
    #options.add_argument('--headless')

    # specifies the path to the chromedriver.exe
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    return driver


def create_linkedin_search_url(name, surname, *additional_terms):
        base_url = "https://www.google.com/search?q=site:linkedin.com/in/+" + name + "+" + surname

        for term in additional_terms:
            base_url += "+" + term

        return base_url

def get_url(name, surname, driver):
    max_page = 5
    all_urls = []


    # always start from page 1
    page = 1

    driver.get(create_linkedin_search_url(name,  surname, "Galatasaray", "Üniversitesi"))

    while True:
        time.sleep(3)
        soup = BeautifulSoup(driver.page_source, "html.parser")

        if "Our systems have detected unusual traffic" in soup.get_text():
            print("Our systems have detected unusual traffic. Please intervene and confirm you are not a robot.")
            user_input = input("Enter 'yes' to continue: ")
            if user_input.lower() != "yes":
                print("Exiting due to user input.")
                break
            driver.get(create_linkedin_search_url(name,  surname))
            soup = BeautifulSoup(driver.page_source, "html.parser")


        # find the urls
        res = soup.select("cite")
        urls = []
        for i in res:
            base = i.get_text().split("›")[0].strip() +  "/in/"
            name = i.select_one("span").get_text().split("›")[-1].strip()
            urls.append(base + name)

        return urls[0]
        

    return all_urls