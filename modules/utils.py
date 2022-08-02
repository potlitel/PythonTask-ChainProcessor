from os.path import exists as file_exists
from configparser import ConfigParser

#Get the configparser object
config_object = ConfigParser()
initValues = ""
#def getInitValues():
if file_exists("config.ini"):
   #Read config.ini file
   config_object.read("config.ini")
   #Get the password
   initValues = config_object["AppConfig"]
   print("File name es {}".format(initValues["fileName"]))
else:
    config_object["AppConfig"] = {
    "fileName": "chains.txt",
    "numberOfChains": "500",
    }
    #Write the above sections to config.ini file
    with open('config.ini', 'w') as conf:
        config_object.write(conf)