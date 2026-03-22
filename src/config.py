import configparser

def setNewConfig(firstName, lastName, emailValue, synchroKeyEmail, objectMail, textMail, frequency):
    config = configparser.ConfigParser()
    config.read('config.ini')

    if "GENERAL" not in config:
        config["GENERAL"] = {}

    config["GENERAL"]["firstName"] = firstName
    config["GENERAL"]["lastName"] = lastName
    config["SETUP"]["objectMail"] = objectMail
    config["SETUP"]["textMail"] = textMail
    config["SETUP"]["frequency"] = frequency
    config["EMAIL"]["email_address"] = emailValue
    config["EMAIL"]["email_password"] = synchroKeyEmail
    

    with open("config.ini", "w", encoding="utf-8") as configfile:
        config.write(configfile)

def loadCurrentConfig():
    config_parser = configparser.ConfigParser()
    config_parser.read("config.ini", encoding="utf-8")

    return {
        "firstName": config_parser.get("GENERAL", "firstName", fallback=""),
        "lastName": config_parser.get("GENERAL", "lastName", fallback=""),
        "email": config_parser.get("EMAIL", "email_address", fallback=""),
        "synchroKeyEmail": config_parser.get("EMAIL", "email_password", fallback=""),
        "frequency": config_parser.get("SETUP", "frequency", fallback=""),
        "objectMail": config_parser.get("SETUP", "objectMail", fallback=""),
        "textMail": config_parser.get("SETUP", "textMail", fallback=""),
    }