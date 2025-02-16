from bs4 import BeautifulSoup
import requests
import pandas as pd

base_url="https://www.akcniceny.cz/"

def number_of_scraped_pages():
    response=requests.get(f"https://www.akcniceny.cz/zbozi/")
    soup=BeautifulSoup(response.text,"html.parser")

    number_of_sites=soup.find_all("a",{"class":"page-link"})

    number_list=[]

    for one_number in number_of_sites:
        one_number=str(one_number.get("href"))
        one_number=one_number.replace("/zbozi/strana-","").replace("/","")
        if one_number.isdigit():
            number_list.append(int(one_number))
    max_number=max(number_list)
    return max_number

max_number=get_number_of_pages()


def scrape_pages(max_number):
    article_list = []
    price_list = []
    link_list = []
    for i in range(1, max_number + 1):
        if i == 1:
            response = requests.get("https://www.akcniceny.cz/zbozi/")
        else:
            response = requests.get(f"https://www.akcniceny.cz/zbozi/strana-{i}/")
            # print(response.text)
            soup = BeautifulSoup(response.text, "html.parser")

            article = soup.find_all(class_="col-md-6 col-12 text-start text-md-start pe-0")
            price = soup.find_all(class_="fs-20 fs-m-15 fw-bold color-red mb-1")
            link = soup.find_all("a", {"class": "fs-18 fs-m-15 fw-bold mb-1"})
            for one_article in article:
                one_article = one_article.getText()
                article_list.append(one_article)
                # print(one_article)
            for one_price in price:
                one_price = one_price.getText().split(" - ")[0].replace(",", ".")
                price_list.append(one_price)
            for one_link in link:
                one_link = one_link.get("href")
                one_link = base_url + one_link
                link_list.append(one_link)
    return article_list, price_list, link_list


article_list, price_list, link_list = scrape_pages(max_number)

def get_dataframe(article_list,price_list,link_list):
  df=pd.DataFrame({"Název":article_list,"Cena":price_list,"Url odkaz":link_list})
  df.to_csv("results.csv",index=False,encoding="utf-8")
  return df
df=get_dataframe(article_list,price_list,link_list)

# link=soup.find_all("a",{"class":"fs-18 fs-m-15 fw-bold mb-1"})
#
# for one_link in link:
#     one_link=one_link.get("href")
#     one_link=base_url+one_link
#     print(one_link)