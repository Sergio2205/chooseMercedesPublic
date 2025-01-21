import time
import openai
import requests
import re
import os
from dotenv import load_dotenv
from openai import OpenAI

# Cargar las variables del archivo .env
load_dotenv()

# Leer las claves desde las variables de entorno
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

# Verificar que las claves no estén vacías
if not OPENAI_API_KEY:
    raise ValueError("Missing OpenAI API Key. Ensure it's set in the .env file.")
if not TELEGRAM_TOKEN:
    raise ValueError("Missing Telegram Token. Ensure it's set in the .env file.")

# Configurar OpenAI
openai = OpenAI(api_key=OPENAI_API_KEY)

# Diccionario para limitar la frecuencia de mensajes por usuario
user_last_message_time = {}

def get_updates(offset):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getUpdates"
    params = {"timeout": 100, "offset": offset}
    response = requests.get(url, params=params)
    return response.json().get("result", [])

def send_messages(chat_id, text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    params = {"chat_id": chat_id, "text": text}
    response = requests.post(url, params=params)
    return response

def sanitize_input(user_input):
    # Elimina caracteres potencialmente peligrosos
    sanitized = re.sub(r"[^\w\s,.!?-]", "", user_input)
    return sanitized.strip()

def rate_limit(chat_id):
    current_time = time.time()
    if chat_id in user_last_message_time:
        if current_time - user_last_message_time[chat_id] < 2:  # 2 segundos entre mensajes
            return False
    user_last_message_time[chat_id] = current_time
    return True

def get_openai_response(prompt):
    try:
        system = '''
           You are a personal assistant that helps the user make the decision to change their vehicle to an electric one.
            '''
        response = openai.chat.completions.create(
            model='ft:gpt-4o-mini-2024-07-18:personal:chooseelectric:ApIrUrZq',
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            n=1,
            temperature=0
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error processing with OpenAI: {e}")
        return "Sorry, an error occurred while processing your request."

def main():
    first_text = '''
    Greetings, I'm "chooseElectric." You can rely on me to advise you on whether purchasing an electric vehicle 
    will enhance your mobility and help the environment simultaneously. I would first like to know the model of your actual
    car as well as the approximate number of kilometers you drive each month.
    '''
    offset = 0
    updates = get_updates(offset)
    if updates:
        chat_id = updates[0]["message"]["chat"]['id']
        send_messages(chat_id, first_text)
        offset = updates[0]["update_id"] + 1
    while True:
        updates = get_updates(offset)
        if updates:
            for update in updates:
                offset = update["update_id"] + 1
                chat_id = update["message"]["chat"]['id']
                user_message = update["message"]["text"]

                # Sanitizar y validar entrada
                user_message = sanitize_input(user_message)
                if not rate_limit(chat_id):
                    send_messages(chat_id, "Please wait a moment before sending another message.")
                    continue

                print(f"Received sanitized message: {user_message}")
                GPT = get_openai_response(user_message)
                send_messages(chat_id, GPT)
        else:
            time.sleep(1)

if __name__ == '__main__':
    main()
