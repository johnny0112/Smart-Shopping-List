import pandas as pd

def get_food_list():
    df=pd.read_csv("food_data.csv")
    food_list = list(df["Název"])
    price_list = list(df["Cena"])
    link_list = list(df["Url odkaz"])
    return food_list,price_list,link_list