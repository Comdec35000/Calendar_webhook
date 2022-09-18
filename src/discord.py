
def check_current():
    pass

def check_for_week():
    pass

def url(config): 
    return f"https://discord.com/api/webhooks/{config.get('id')}/{config.get('token')}"