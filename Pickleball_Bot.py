

import openai
from gtts import gTTS
import datetime
import os
import playsound



key = "YOUR API KEY"    

openai.api_key = key


# This function(speak) is only for demo purposes
def speak(text):
    tts = gTTS(text, lang='en') 

    filename = "Pickleballbot_voice.mp3"
    tts.save(filename)
    playsound.playsound(filename)
    os.remove(filename)



greetings = {
    "morning": "Good Morning",
    "afternoon": "Good Afternoon",
    "evening": "Good Evening"
}

def greet():
    # Get current hour
    hour = int(datetime.datetime.now().hour)
    # Determine appropriate greeting based on time of day
    if hour >= 0 and hour < 12:
        greeting = greetings["morning"]
    elif hour >= 12 and hour < 18:
        greeting = greetings["afternoon"]
    else:
        greeting = greetings["evening"]
    # Greet user
    message = greeting + " , how may I help you 😃"
    print(message)
    message = message.replace("😃", "")  
    speak(message)

def chat(message_log):
        response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=message_log,   
                max_tokens=3000,        
                stop=None,           
                temperature=0.9, 
                top_p=1,
        )

        return response.choices[0].message.content



# read info about product catalog from this file
with open("product_catalog.txt",encoding="utf-8") as f:  
    product_info = f.read()

# Questions about pickeball as sport
with open("pickleball_sport.txt",encoding="utf-8") as f:  
    pickleball_info = f.read()

# Questions about our company
with open("our_company.txt",encoding="utf-8") as f:
    company_info = f.read()

    

def main():
    personality = f"You are a helpful assistant  , Your name is GLIDEz and you answer questions in related to{product_info},{company_info},{pickleball_info}"
    time = datetime.datetime.now().strftime("%I:%M %p")
    message_log = [
        {"role": "system", "content": personality },
        {"role": "system", "content": f"Current/now time is {time}" },
        {"role": "system", "content": f"Any question about product {product_info}" },
        {"role": "system", "content": f"Any question about pickleball sport {pickleball_info}" },
        {"role": "system", "content": f"Any question about our company {company_info}" },
        {"role": "system", "content": f"Deny request unrelated to {product_info}, {pickleball_info},{company_info}" }
    ]

    while True:
        ask = input("Ask any thing...")
    
        message_log.append({"role": "user", "content": ask})

        response = chat(message_log)
        message_log.append({"role": "system", "content": response})

        print(f"GLIDEz: {response}\n")
        speak(response)

        if ask.lower() == "exit":
            break
        

if __name__ == "__main__":
    greet()
    main()
