import requests
import urllib.parse
from datetime import datetime
import asyncio
import httpx

#How many times to retry requests?
retries = 8

async def gen_text(prompt, system_prompt, json):
    delay = 3
    for i in range(retries):
        try:
            if json:
                result = await _generate_text_json(prompt, system_prompt)
            else:
                result = await _generate_text(prompt, system_prompt)
            return result
        except (httpx.RequestError, httpx.HTTPStatusError):
            print(f"Request failed (attempt {i+1})")
            if i < retries-1:
                print(f"Retrying in {delay} seconds")
                await asyncio.sleep(delay) #delay repeated 
                if delay < 12:
                    delay *=2
            else:
                raise

async def gen_image(prompt, download, **kwargs):
    seed = "random"
    model = "flux"
    width = 480
    height = 480
    enhance = True
    safe = True
    debug = False
    for key, value in kwargs.items():
        if key == "seed":
            seed = value
        if key == "model":
            model = value
        if key == "width":
            width = value
        if key == "height":
            height = value
        if key == "enhance":
            enhance = value
        if key == "safe":
            safe = value
        if key == "debug":
            debug = value
    delay = 1
    for i in range(retries):
        try:
            if debug:
                print(f"Requesting image (attempt {i + 1})")
            if download:
                result = await _generate_image_download(prompt, seed=seed, model=model, width=width, height=height, enhance=enhance, safe=safe)
            else:
                result = await _generate_image_url(prompt, seed=seed, model=model, width=width, height=height, enhance=enhance, safe=safe)
            return result
        except (httpx.RequestError, httpx.HTTPStatusError):
            print(f"Request failed (attempt {i+1})")
            if i < retries-1:
                print(f"Retrying in {delay} seconds")
                await asyncio.sleep(delay) #delay repeated requests
                delay *=2
            else:
                raise



async def _generate_text(prompt, system_prompt):
    payload = {
    "messages": [
        {"role": "system", "content": f"{system_prompt}"},
        {"role": "user", "content": f"{prompt}"}
    ],
    "model": "openai-large",
    "seed": 42,
    "jsonMode": False,
    "private": True
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(url="http://text.pollinations.ai", json=payload)
    response.raise_for_status()
    data = response.content.decode("utf-8")
    return data

async def _generate_text_json(prompt, system_prompt):
    payload = {
    "messages": [
        {"role": "system", "content": f"{system_prompt}"},
        {"role": "user", "content": f"{prompt}"}
    ],
    "model": "openai",
    "seed": 42,
    "jsonMode": True,
    "private": True
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(url="https://text.pollinations.ai", json=payload)
    response.raise_for_status()
    return response.json()

async def _generate_image_url(prompt, **kwargs):
    seed = "random"
    model = "flux"
    width = 480
    height = 480
    enhance = True
    safe = True
    for key, value in kwargs.items():
        if key == "seed":
            seed = value
        if key == "model":
            model = value
        if key == "width":
            width = value
        if key == "height":
            height = value
        if key == "enhance":
            enhance = value
        if key == "safe":
            safe = value
    payload = urllib.parse.urlencode({
        "seed": seed,
        "enhance": enhance,
        "model": model,
        "width": width,
        "height": height,
        "nologo": True,
        "private": True,
        "safe": safe
    })
    url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(prompt)}?{payload}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url=url)
    response.raise_for_status()
    return url

async def _generate_image_download(prompt, **kwargs):
    seed = "random"
    model = "flux"
    width = 480
    height = 480
    enhance = True
    safe = True
    for key, value in kwargs.items():
        if key == "seed":
            seed = value
        if key == "model":
            model = value
        if key == "width":
            width = value
        if key == "height":
            height = value
        if key == "enhance":
            enhance = value
        if key == "safe":
            safe = value
    payload = urllib.parse.urlencode({
        "seed": seed,
        "enhance": enhance,
        "model": model,
        "width": width,
        "height": height,
        "nologo": True,
        "private": True,
        "safe": safe
    })
    url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(prompt)}?{payload}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url=url)
    response.raise_for_status()
    filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_image.jpg"
    with open(filename, "wb") as file:
        file.write(response.content)
    return filename


#This is a way to test these functions as a command line tool
#text generation:  gt--user prompt--system prompt
#json generation:  gtj--user prompt--system prompt
#image URL gen:    gi--image prompt
#image download:   gid--image prompt
    
running = True

# while running:
#     command = input("Enter command: ")
#     split_c = command.split("--")
#     if split_c[0] == "gi":
#         if len(split_c) < 2:
#             print("gi requires a param")
#         url = asyncio.run(gen_image(split_c[1], False))
#         print(url)
#     if split_c[0] == "gid":
#         asyncio.run(gen_image(split_c[1], True))
#         if len(split_c) < 2:
#             print("gid requires a param")
#     if split_c[0] == "gt":
#         if len(split_c) < 3:
#             print("gt requires two params")
#         else:
#             text = asyncio.run(gen_text(split_c[2], split_c[1], False))
#             print(text)
#     if split_c[0] == "gtj":
#         if len(split_c) < 3:
#             print("gtj requires two params")
#         else:
#             text= asyncio.run(gen_text(split_c[2], split_c[1], True))
#             print(text)