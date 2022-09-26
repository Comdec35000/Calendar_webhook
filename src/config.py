from distutils.command.config import config
import json


def get_config():
    with open('config.json') as raw:
        config = json.load(raw)
        if(validate_config(config)):
            config["url_old"] = config["url"]
            save_config(config)
            return config
        else:
            return create_config(config)
        

def validate_config(config):
    try:
        if config["webhook"] == "": return False
        if config["url"] == "" or not str(config["url"]).startswith("https://") : return False

        print("\nSuccessfully validated the configuration !")
        return True
    except :
        return False

def create_config(old_cfg: dict):
    print("\n\nSome config data is missing ! Let's supplement it !\n")
    webhook = input("Please enter here your webhook's link ! \n > ")
    url = input("Please paste here the direct link to your .ics file !\n > ")

    config = {
        "webhook": webhook,
        "url": url,
        "url_old": old_cfg.get("url") if old_cfg.get("url") != None else ""
    }

    if not validate_config(config): return create_config(old_cfg)

    save_config(config)
    return config

def save_config(config): 
    with open('config.json', 'w') as file:
        json.dump(config, file, indent=2)