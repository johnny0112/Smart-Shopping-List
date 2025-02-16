import pandas as pd
from bs4 import BeautifulSoup
import requests
import pandas as pd
from df_converter import get_food_list

df=pd.read_csv("food_data.csv")
#print(df)
grocery_list=["Coca-Cola 1,5l, vybrané druhy","Cibule žlutá 1 kg"]
#food=input("Co chcete hledat\n").lower()

def get_results_dictionary(grocery_list):
    results = {}
    for one_grocery in grocery_list:
        one_link=df["Url odkaz"][df["Název"]==one_grocery].iloc[0]
        response = requests.get(one_link)
        #print(response)
        soup = BeautifulSoup(response.text, "html.parser")
        shops = soup.find_all(class_="col-12 fs-18 fs-m-15 fw-bold mb-0")
        prices = soup.find_all(class_="fs-20 fw-bold color-red mb-0 d-inline-block")
        partial_results = {}
        i=1
        for one_shop, one_price in zip(shops, prices):
            if i==1:
                i+=1
                one_shop = one_shop.getText()
                one_price = float(one_price.getText().replace("Kč", "").replace("\n", "").strip().replace(",", ".").split("-")[0].replace("*",""))
                highest_price=float(prices[-1].getText().replace("Kč", "").replace("\n", "").strip().replace(",", ".").split("-")[0].replace("*",""))
                highest_price_store=shops[-1].getText()
                # print(one_price)
                # print(highest_price)
                # print(one_shop)
                # print(highest_price_store)
                partial_results[one_shop] = one_price
                partial_results[highest_price_store]=highest_price
        results[one_grocery]=partial_results

    return results

results=get_results_dictionary(grocery_list)
print(results)
def get_prices(results):
    lowest_price=list(results.values())[0]
    lowest_price_store=list(results.keys())[0]
    highest_price=list(results.values())[-1]
    highest_price_store=list(results.keys())[-1]
    return  lowest_price,lowest_price_store,highest_price,highest_price_store
def get_output_string(results):
    output=[]
    total_price=0
    total_discount=0
    for one_result in results:
        i=1
        for shop,price in results[one_result].items():
            if i==1:
                i+=1
                output.append(f"{one_result} Obchod: **{shop}** Cena: **{price} Kč**")
                discount=max(results[one_result].values())-min(results[one_result].values())
                print(discount)
                total_price+=price
                total_discount+=discount
    output.append(f"Celková cena za nákup je **{round(total_price,1)} Kč**.")
    output.append(f"Díky chtrému nákupnímu seznamu jste ušetřili **{round(total_discount,1)} Kč** 🤑")
    return output
output=get_output_string(results)
print(output)










