import requests
import time

url = "http://127.0.0.1:5000/controller"

data = {
    "moveleft": 0,
    "moveright": 0,
}

while True:
    try:
        resp = requests.post(url, json=data)
        if resp.ok == False:
            break
    except:        
        time.sleep(0.1)
        continue

    time.sleep(0.1)

    gui_data = resp.json()
    collide_level = gui_data["collide_level"]
    carpos = gui_data["carpos"]

    data = {
            "moveleft": 0,
            "moveright": 0,
        }

    collide_level["top"] = 100 if collide_level["top"] == 0 else collide_level["top"]
    collide_level["left"] = 100 if collide_level["left"] == 0 else collide_level["left"]
    collide_level["right"] = 100 if collide_level["right"] == 0 else collide_level["right"]

    if collide_level["top"] >= collide_level["left"] and collide_level["top"] >= collide_level["right"]:
            data = {
            "moveleft": 0,
            "moveright": 0,
        }
    elif collide_level["left"] >= collide_level["top"] and collide_level["left"] >= collide_level["right"]:
        data = {
            "moveleft": 1,
            "moveright": 0,
        }
    elif collide_level["right"] >= collide_level["top"] and collide_level["right"] >= collide_level["left"]:
        data = {
            "moveleft": 0,
            "moveright": 1,
        }
