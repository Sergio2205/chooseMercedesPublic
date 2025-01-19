import time
import openai
import requests
from openai import OpenAI

openai = OpenAI(api_key='INSERT OPENAI API KEY')
TOKEN = "INSERT TELEGRAM BOT TOKEN"

def get_updates(offset):
    url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
    params = {"timeout": 100, "offset": offset}
    response = requests.get(url, params=params)
    return response.json()["result"]

def send_messages(chat_id, text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    params = {"chat_id": chat_id, "text": text}
    response = requests.post(url, params=params)
    return response

def get_openai_response(prompt):
    system = '''
       You are a personal assistant that helps the user make the decision to change their vehicle to an Mercedes-Benz electric one.
        '''
    response = openai.chat.completions.create(
		model='ft:gpt-4o-mini-2024-07-18:personal:choosemercedes:ArNjSTEz',
		messages=[
            {"role": "system", "content" :f'{system}'},
            {"role": "user", "content" : f'{prompt}'}],
		max_tokens=350,
		n=1,
		temperature=0)    
    return response.choices[0].message.content.strip()

def main():
    first_text = '''
    Greetings, I'm "chooseMercedes." I will help you decide if you should change your old and not Eco-Friendly car and have instead a Mercedes-Benz electric or
    hybrid vehicle und save the environment as well you save your money.
'''
    offset = 0
    updates = get_updates(offset)
    if updates:
        chat_id = updates[0]["message"]["chat"]['id']
        send_messages(chat_id, first_text)
        offset = updates[0]["update_id"] +1
    while True:
        updates = get_updates(offset)
        if updates :
            for update in updates:
                offset = update["update_id"] +1
                chat_id = update["message"]["chat"]['id']
                user_message = update["message"]["text"]
                print(f"Received message: {user_message}")
                GPT = get_openai_response(user_message)
                send_messages(chat_id, GPT)
        else:
            time.sleep(1)

if __name__ == '__main__':
    main()
