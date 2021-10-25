from bson.objectid import ObjectId
from flask import Blueprint, url_for, redirect, flash, render_template
from rolwithfriends import mongo
from rolwithfriends.characters.forms import CreateCharacterForm
from flask_login import current_user, login_required
from rolwithfriends.characters.utils import save_charPictures, getRaceAttributes, GetSkillPoints, getClassProsAndCons
characters = Blueprint('characters', __name__)



@characters.route("/create/character/<int:roomId>", methods=["GET", "POST"])
@login_required
def create_character(roomId):
    newCharacterForm = CreateCharacterForm()
    if newCharacterForm.is_submitted():

        charPortrait = save_charPictures(newCharacterForm.cImage.data, "portrait")
        charAvatar = save_charPictures(newCharacterForm.cAvatar.data, "avatar")

        mongo.db.Characters.insert_one({"cName": newCharacterForm.cName.data, 
                                                       "bgStory": newCharacterForm.bgStory.data,
                                                       "race": newCharacterForm.cRace.data,
                                                       "status": "normal",
                                                       "gold": 0,
                                                       "cClass": newCharacterForm.cClass.data,
                                                       "cClassProsAndCons": getClassProsAndCons(newCharacterForm.cClass.data),
                                                       "cHeight": newCharacterForm.cHeight.data,
                                                       "cWeight": newCharacterForm.cWeight.data,
                                                       "inventory": [],
                                                       "level": 1,
                                                       "cPortrait": charPortrait,
                                                       "cAvatar": charAvatar,
                                                       "cAttributes": GetSkillPoints(),
                                                       "clothes": [],
                                                       "cAbilities": [],
                                                       "raceAttributes": getRaceAttributes(newCharacterForm.cRace.data),
                                                       "weapon": {"wName": "None", "wAbility": "None"},
                                                       "gift": {"gName": "None", "gAbility": "None"},
                                                       "language": newCharacterForm.cLanguage.data,
                                                       "roomId": roomId,
                                                       "owner": current_user.id,
                                                       "skillPointsLeft": 0})
        newCharacter = mongo.db.Characters.find_one({"cName": newCharacterForm.cName.data, "roomId": roomId})
        if newCharacter:
            print(newCharacter["_id"])
            mongo.db.Rooms.update_one({"roomId": roomId}, {"$push":{"characters": {"character": newCharacter['_id'], "owner": current_user.id}}})
            if newCharacter:
                flash('Character created!', 'success')
                return redirect(url_for('rooms.room', roomId = roomId))
    return render_template('/characters/createcharacter.html', form = newCharacterForm)

@characters.route("/room/<int:roomId>/character/<string:charId>")
def profile(roomId, charId):
   
   charInfo = mongo.db.Characters.find_one({"_id": ObjectId(charId)})

   if charInfo: 
    return render_template("/characters/profile.html", characterInfo = charInfo)
   else:
       flash("There was a problem loading the character info", "warning")
       return redirect(url_for("rooms.room", roomId = roomId)) 
