from openai import OpenAI
import os
import google.generativeai as genai


def get_grok_api_key():
    try:
        with open("api_key.txt","r") as file:
            grok_api_key=file.read()
            return grok_api_key
    except FileNotFoundError:
        raise FileNotFoundError("Grok API key not found.")

def get_gemini_api_key():
    try:
        with open("gemini_api_key.txt") as file:
            gemini_api_key=file.read()
            return gemini_api_key
    except FileNotFoundError:
        return  FileNotFoundError("Gemini API key not found")

gemini_api_key=get_gemini_api_key()

def client_configuration(api_key):
    client=OpenAI(api_key=api_key,
              base_url="https://api.x.ai/v1")
    return client

def get_grok_response(client,food):
    response=client.chat.completions.create(model="grok-2-latest",
                                        messages=[{"role":"system","content":"Budeš odpovídat pouze v češtině, tvým úkolem bude pouze vypsat suroviny na zadaný pokrm. Každá tvoje odpověď bude začínat slovem Suroviny: Následovat bude seznam surovin na zadaný pokrm. Je zakázáno psát cokoliv jiného než seznam surovin. Pokud uživatel zadá cokoliv jiného než název jídla napiš Takovéto jídlo neexistuje.První slovo Suroviny musí být tučně."},
                                                  {"role":"user","content":f"{food}"}])
    return  response.choices[0].message.content

def get_gemini_response(food):
    genai.configure(api_key=gemini_api_key)
    model=genai.GenerativeModel("gemini-2.0-flash-exp")
    response=model.generate_content(f"Budeš odpovídat pouze v češtině, tvým úkolem bude pouze vypsat suroviny na zadaný pokrm. Každá tvoje odpověď bude začínat slovem Suroviny: Následovat bude seznam surovin na zadaný pokrm. Je zakázáno psát cokoliv jiného než seznam surovin. Pokud uživatel zadá cokoliv jiného než název jídla napiš Takovéto jídlo neexistuje.První slovo Suroviny musí být tučně. Uživatel požádal o recept na: {food}")
    return  response.text


# api_key=get_api_key()
# client=client_configuration(api_key)
# response=get_response(client,food="Guláš")
# print(response)