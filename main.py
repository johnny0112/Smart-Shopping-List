import streamlit as st
from bs4 import BeautifulSoup
import requests
from llm_api import get_grok_api_key,get_gemini_api_key,client_configuration,get_grok_response,get_gemini_response
from real_time_price_scraper import get_results_dictionary,get_prices,get_output_string
from df_converter import get_food_list

api_key=get_grok_api_key
client=client_configuration(api_key)
food_list,price_list,link_list=get_food_list()

st.set_page_config(page_title="Chytrý nákupní seznam",page_icon="logo.png")

st.sidebar.title("Menu")
st.sidebar.markdown("---")
menu = st.sidebar.radio("Navigace:",
    ["Vyhledat potraviny", "Vyhledat suroviny na pokrm","Historie vyhledávání","Souhrn"])

if menu == "Vyhledat potraviny":
    left,right=st.columns(2)
    left.image("picture.png")
    #st.title("Vyhledejte, kde mají nejlevnější potraviny ")
    grocery=st.multiselect("Zvolte potraviny",options=food_list,placeholder="Zadejte potraviny a náš algoritmus se o vše postará")
    #left, middle, right = st.columns(3)
    if(st.button("Odeslat",help="Hned po kliknutí se naše umělá inteligence postará o ty nejlepší výsledky")):
        results = get_results_dictionary(grocery)
        output=get_output_string(results)
        st.subheader("Váš vytvořený nákupní seznam:")
        for one_output in output:
            st.write(one_output)
        st.subheader("Nechte si zaslat Váš vytvořený nákupní seznam!")
        st.text_input("Vyplňte telefonní číslo a nákupní seznam máte hned v SMS ")
        st.button("Zaslat bezplatně SMS")
        # st.write(f"Rajče: obchod {lowest_price_store} - cena {lowest_price} kč.")
        # st.write("\n")
        # discount=highest_price-lowest_price
        # st.write(f"Ušetřili jste {int(discount)} kč 🤑")



elif menu == "Vyhledat suroviny na pokrm":
    st.title("Vyhledání receptu ")
    if "food" not in st.session_state:
        st.session_state.food=""
    if "response" not in st.session_state:
        st.session_state.response=""
    if "grocery" not in st.session_state:
        st.session_state.grocery = []
    if "output" not in st.session_state:
        st.session_state.output=[]

    st.session_state.food=st.text_input("Zadejte pokrm pro který chcete vyhledat suroviny.")
    if st.button("Odeslat",help="Hned po kliknutí se naše umělá inteligence postará o ty nejlepší výsledky"):
        st.session_state.response = get_gemini_response( st.session_state.food)

    if st.session_state.response:
        st.write(st.session_state.response)
        st.subheader(f"Chybí vám doma na {st.session_state.food} nějaké suroviny?")
        st.session_state.grocery = st.multiselect("Zvolte potraviny", options=food_list,default=st.session_state.grocery,placeholder="Zadejte potraviny, které chcete dokoupit")
        if (st.button("Odeslat",key="Zvolte potraviny", help="Hned po kliknutí se naše umělá inteligence postará o ty nejlepší výsledky")):
            results = get_results_dictionary(st.session_state.grocery)
            st.session_state.output = get_output_string(results)
    if st.session_state.output:
        st.subheader(f"Váš seznam chybějících surovin na {st.session_state.food}:")
        for one_output in st.session_state.output:
            st.write(one_output)

elif menu == "Historie vyhledávání":
    st.subheader("Pro historii vyhledávání je třeba se nejprve přihlásit.")
    st.write(" ")
    left,right=st.columns(2)
    if left.button("Přihlásit se.",use_container_width=True):
        st.text_input("Zadejte uživatelské jméno.")
        st.text_input("Zadejte heslo")
        st.button("Přihlásit se")
    if right.button("Vytvořit účet",use_container_width=True):
        st.text_input("Zadejte uživatelské jméno.")
        st.text_input("Zadejte e-mailovou adresu")
        st.text_input("Zadejte heslo")
        st.button("Zaregistrovat se")


elif menu == "Souhrn":
    st.subheader("Pro zobrazení souhrnu je třeba se nejprve přihlásit.")
    st.write(" ")
    left, right = st.columns(2)
    if left.button("Přihlásit se.", use_container_width=True):
        st.text_input("Zadejte uživatelské jméno.")
        st.text_input("Zadejte heslo")
        st.button("Přihlásit se")
    if right.button("Vytvořit účet", use_container_width=True):
        st.text_input("Zadejte uživatelské jméno.")
        st.text_input("Zadejte e-mailovou adresu")
        st.text_input("Zadejte heslo")
        st.button("Zaregistrovat se")



