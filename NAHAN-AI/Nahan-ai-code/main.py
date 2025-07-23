import speech_recognition as sr
import pyttsx3 as pt
import webbrowser
import openai
from openai import OpenAI
from congi import apiky
import time
import os
from datetime import datetime

chatStr = ""

def chat(query):
    global chatStr
    print(chatStr)
    chatStr += f"Rehan : {query}\nNAHAN : "

    # Get current date to include in the system prompt
    current_date = datetime.now().strftime("%B %d, %Y")

    client = OpenAI(
        api_key=apiky,
        base_url="https://openrouter.ai/api/v1"
    )

    messages = [
        {"role": "system", "content": f"You are NAHAN, a helpful AI assistant. Today is {current_date}. Answer accordingly."},
        {"role": "user", "content": f"Rehan: {query}"}
    ]

    response = client.chat.completions.create(
        model="mistralai/mistral-7b-instruct",  # You can replace with openai/gpt-4o if available
        messages=messages,
        temperature=0.7,
        max_tokens=125
    )

    response_text = response.choices[0].message.content
    say(response_text)
    chatStr += f"{response_text}\n"

    # Save chat to file
    if not os.path.exists("openai"):
        os.mkdir("openai")
    filename = f"openai/prompt-{int(time.time())}.txt"
    with open(filename, "w") as f:
        f.write(f"openai Response: {query}\n***************************\n\n{response_text}")

    return response_text


def ai(prompt):
    client = OpenAI(
        api_key=apiky,
        base_url="https://openrouter.ai/api/v1"
    )

    current_date = datetime.now().strftime("%B %d, %Y")
    messages = [
        {"role": "system", "content": f"You are NAHAN, a helpful assistant. The date today is {current_date}."},
        {"role": "user", "content": prompt}
    ]

    response = client.chat.completions.create(
        model="mistralai/mistral-7b-instruct",
        messages=messages,
        temperature=0.7,
        max_tokens=125
    )

    response_text = response.choices[0].message.content
    print("\nAI Response:\n")
    print(response_text)


def say(text):
    engine = pt.init()
    engine.say(text)
    engine.runAndWait()


def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1
        audio = r.listen(source)
        try:
            query = r.recognize_google(audio, language='en-in')
            print(query)
            return query
        except Exception:
            return "Some Error, Sorry From NAHAN"


if __name__ == "__main__":
    print("NAHAN")
    say("Hello, I am Nahan AI")
    while True:
        print("Say Anything....")
        query = takecommand()

        # Open websites
        sites = [
            ["youtube", "https://www.youtube.com"],
            ["google", "https://www.google.com"],
            ["wikipedia", "https://www.wikipedia.org/"]
        ]

        for site in sites:
            if f"open {site[0]}" in query.lower():
                say(f"Opening {site[0]}")
                webbrowser.open(site[1])
                break

        # Open Camera
        if "open camera" in query.lower():
            say("Opening camera")
            os.system("start microsoft.windows.camera:")
            time.sleep(5)

        # Ask NAHAN (AI)
        elif "open ai" in query.lower():
            ai(prompt=query)

        # All other questions go to chat
        else:
            chat(query)
