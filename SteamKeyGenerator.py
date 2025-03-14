import requests
import random
import string
import json
import tkinter as tk
from tkinter import messagebox

def generate_code():
    part1 = random.choice(string.ascii_uppercase) + ''.join(random.choices(string.digits, k=4))

    part2 = ''.join(random.choices(string.ascii_uppercase, k=2)) + \
            ''.join(random.choices(string.digits, k=1)) + \
            ''.join(random.choices(string.ascii_uppercase, k=2))

    part3 = ''.join(random.choices(string.digits + string.ascii_uppercase, k=4))

    code = f"{part1}-{part2}-{part3}"
    return code

def sende_nachricht(webhook_url, nachricht):
    daten = {
        "content": nachricht
    }
    
    response = requests.post(webhook_url, json=daten)
    
    if response.status_code == 204:
        print(f"VALID!: '{nachricht}' successfully sent!")
    else:
        print(f"ERROR!: {response.status_code} Key {nachricht} couldn't be sent!")

def code_generator(webhook_url, keys):
    for _ in range(keys):
        code = generate_code()
        sende_nachricht(webhook_url, code)

def lade_config():
    try:
        with open('config.json', 'r') as config_file:
            config = json.load(config_file)
            return config
    except FileNotFoundError:
        messagebox.showerror("ERROR!", "config.json couldn't be found!")
        return None
    except json.JSONDecodeError:
        messagebox.showerror("ERROR!", "config.json is invalid!")
        return None

def on_generate_button_click():
    try:
        keys = int(entry_keys.get())
        if keys <= 0:
            messagebox.showerror("ERROR!", "Please enter a number over 0!")
            return
    except ValueError:
        messagebox.showerror("ERROR!", "Please enter a valid number!")
        return
    
    config = lade_config()
    
    if config:
        webhook_url = config.get("webhook_url")
        
        if not webhook_url:
            messagebox.showerror("ERROR", "Webhook-URL is missing.")
            return
        
        print(f"Generiere {keys} Keys und sende sie an {webhook_url}...")
        code_generator(webhook_url, keys)

root = tk.Tk()
root.title("Steam Key Generator")
root.geometry("400x400")
root.config(bg="#9e9e9e")

label_title = tk.Label(root, text="Steam Key Generator", font=("Helvetica", 24), fg="#fffff2", bg="#9e9e9e")
label_title.pack(pady=50)

label_keys = tk.Label(root, text="Number of Keys.", font=("Helvetica", 16), fg="#ffffff", bg="#9e9e9e")
label_keys.pack(pady=10)

label_keys = tk.Label(root, text="dont forget the webhook url in config.json", font=("Helvetica", 12), fg="#ffffff", bg="#9e9e9e")
label_keys.pack(pady=10)

entry_keys = tk.Entry(root, font=("Helvetica", 16), width=10)
entry_keys.pack(pady=10)

generate_button = tk.Button(root, text="Start", font=("Helvetica", 16), command=on_generate_button_click, bg="#4CAF50", fg="#ffffff")
generate_button.pack(pady=20)

root.mainloop()
