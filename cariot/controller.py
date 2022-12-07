import requests
import time


def extract(url, controller_data):
    try:
        resp = requests.post(url, json=controller_data)
        if resp.ok == False:
            return None
    except:
        return None

    return resp.json()


def transform(gui_data, controller_data):
    collide_level = gui_data["collide_level"]

    controller_data = {
            "moveleft": 0,
            "moveright": 0,
        }

    collide_level["top"] = 100 if collide_level["top"] == 0 else collide_level["top"]
    collide_level["left"] = 100 if collide_level["left"] == 0 else collide_level["left"]
    collide_level["right"] = 100 if collide_level["right"] == 0 else collide_level["right"]

    if collide_level["top"] >= collide_level["left"] and collide_level["top"] >= collide_level["right"]:
        controller_data = {
            "moveleft": 0,
            "moveright": 0,
        }
    elif collide_level["left"] >= collide_level["top"] and collide_level["left"] >= collide_level["right"]:
        controller_data = {
            "moveleft": 1,
            "moveright": 0,
        }
    elif collide_level["right"] >= collide_level["top"] and collide_level["right"] >= collide_level["left"]:
        controller_data = {
            "moveleft": 0,
            "moveright": 1,
        }

    print(gui_data)
    print(controller_data)
    return controller_data

if __name__ == "__main__":
    url = "http://127.0.0.1:5000/controller"

    controller_data = {
        "moveleft": 0,
        "moveright": 0,
    }

    while True:
        gui_data = extract(url, controller_data)
        if gui_data is not None:
            controller_data = transform(gui_data, controller_data)
            frecuencia = gui_data["frecuencia"]
            time.sleep(1/frecuencia)