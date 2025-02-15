import os
import requests
import base64
import asyncio
import csv
import google.generativeai as genai
from dotenv import load_dotenv
from oksana.tools import *

load_dotenv()

gemini_api_key = os.environ['dev_api_key']

chat_history = {}
genai.configure(api_key=gemini_api_key)

tools = [get_weather, get_stock_price, get_stock_saleInfo, get_stock_info]

def model_init():
    settings = load_json(name="settings/settings")
    model_name = settings["model"]
    generation_config = settings["generation_config"]
    safety_settings = settings["safety_settings"]
    model = genai.GenerativeModel(model_name=model_name, generation_config=generation_config, safety_settings=safety_settings, tools=tools)
    return model

'''
def log(p,r):
    data = csv.writer(open("data/log.csv", 'a+'))
    #data.writerow('')
    data.writerow([f"input: {p}",f"output: {r}"])
'''

def calling_Oksana(prompt, id, ctx=None, img=None):
  system_prompt = load_file(name="settings/system_prompt")
  #print(system_prompt)
  prompt_parts = [
    system_prompt,
    f"input: {prompt}"
  ]

  if str(id) not in chat_history:
    model = model_init()
    chat = chat_history.setdefault(str(id),model.start_chat())
    if img is not None:
        response = chat.send_message([prompt_parts, *img])
    else:
        response = chat.send_message(prompt_parts)
    #print("new chat")
  else:
    chat = chat_history[str(id)]
    if img is not None:
        response = chat.send_message([prompt, *img])
    else:
        response = chat.send_message(prompt)
    #print("read from old chat")
  #print(chat)
  fc_rs = {}
  for part in response.parts:
    if fn := part.function_call:
        args = ", ".join(f"{key}={repr(val)}" for key, val in fn.args.items())
        func = f"{fn.name}({args})"
        #print(func)
        rs = eval(func)
        #loop = asyncio.get_event_loop()
        #loop.create_task(ctx.send(f"-#running {fn.name}"))
        fc_rs[fn.name] = rs
  if len(fc_rs) > 0:
    response_parts = [
        genai.protos.Part(function_response=genai.protos.FunctionResponse(name=fn, response={"result": val}))
        for fn, val in fc_rs.items()
    ]
    response = chat.send_message(response_parts)
  #log(prompt,response.text) -> 有一點小問題，建議別用 by Koala
  print(f"{prompt}\nBot:{response.text}")
  return response.text

def calling_gemini_api(data):
    url = f'https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={gemini_api_key}'
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
      print(response.json())
      return response.json()
    else:
      return "Error"

def clear_chat(id):
  try:
    chat_history.pop(str(id))
    return True
  except Exception as e:
    return False
