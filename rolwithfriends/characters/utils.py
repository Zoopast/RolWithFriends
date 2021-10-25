from PIL import Image
import cloudinary
import cloudinary.uploader
import cloudinary.api
from io import BytesIO

def save_charPictures(c_picture, typeOfPicture):
    buf = BytesIO()

    if typeOfPicture == "portrait":
        i = Image.open(c_picture)
        
        i.save(buf, 'png')
        buf.seek(0)

        image_bytes = buf.read()
        picture_uploaded = cloudinary.uploader.upload(image_bytes, eager=[
            {"width": 300, "height": 600, "crop": "pad"}], 
            folder = "RolWithFriends/characters/portraits/")
    elif typeOfPicture == "avatar":
        i = Image.open(c_picture)
        i.save(buf, 'png')
        buf.seek(0)

        image_bytes = buf.read()
        picture_uploaded = cloudinary.uploader.upload(image_bytes, eager=[
            {"width": 400, "height": 400, "crop": "pad"}], 
            folder = "RolWithFriends/characters/avatars/")
    
    buf.close()

    return picture_uploaded['eager'][0]['secure_url']

def getRaceAttributes(cRace):
    if cRace == "human":
        return {"hp": 100, "bAttack": 10, 
                "attacksPTurn": 1, "bInventory": 10,
                "bMaxWeight": 20}
    elif cRace == "dwarf":
        return {"hp": 80, "bAttack": 15, 
                "attacksPTurn": 1, "bInventory": 10,
                "bMaxWeight": 12}
    elif cRace == "warewolf":
        return {"hp": 110, "bAttack": 25, 
                "attacksPTurn": 1, "bInventory": 10,
                "bMaxWeight": 30}
    elif cRace == "dragonborn":
        return {"hp": 130, "bAttack": 20, 
                "attacksPTurn": 1, "bInventory": 10,
                "bMaxWeight": 25}
    elif cRace == "undead":
        return {"hp": 200, "bAttack": 17, 
                "attacksPTurn": 1, "bInventory": 7,
                "bMaxWeight": 15}
    elif cRace == "orc":
        return {"hp": 150, "bAttack": 30, 
                "attacksPTurn": 1, "bInventory": 12,
                "bMaxWeight": 23}
    elif cRace == "orc":
        return {"hp": 150, "bAttack": 30, 
                "attacksPTurn": 1, "bInventory": 12,
                "bMaxWeight": 23}
    elif cRace == "fairy":
        return {"hp": 70, "bAttack": 17, 
                "attacksPTurn": 2, "bInventory": 4,
                "bMaxWeight": 10}
    elif cRace == "naga":
        return {"hp": 100, "bAttack": 15, 
                "attacksPTurn": 1, "bInventory": 8,
                "bMaxWeight": 17}

def GetSkillPoints():
    return {"Strength": 5, "Stamina": 5, "Dexterity":5, 
            "Intelligence": 5, 
            "Wisdom": 5, 
            "Charisma": 5, "Luck": 5}
def getClassProsAndCons(cClass):
    if cClass == "fighter":
        return {"pro": "Light weight weapons doubles de damage",
            "con": "You cannot use ranged weapons"}
    elif cClass == "dark wizard":
        return {"pro": "If you get a 6 in damage multiplier you get 50 extra points in damage",
            "con": "The prices of any merchant is doubled"}
    elif cClass == "warrior":
        return {"pro": "Using a heavy weapon adds 30 to your total damage",
            "con": "You lose 10 damage for each missing piece of armor"}
    elif cClass == "monk":
        return {"pro": "Spending a turn meditating recovers 20 health",
            "con": "Heavy weapons take 100 damage from you"}