from flask import Blueprint, url_for, redirect, flash, render_template
from rolwithfriends import mongo
from rolwithfriends.characters.forms import CreateCharacterForm
from flask_login import current_user, login_required
from rolwithfriends.characters.utils import save_charPictures, getRaceAttributes, GetSkillPoints
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
                                                       "cHeight": newCharacterForm.cHeight.data,
                                                       "inventory": [],
                                                       "cPortrait": charPortrait,
                                                       "cAvatar": charAvatar,
                                                       "cAttributes": GetSkillPoints(),
                                                       "clothes": [],
                                                       "raceAttributes": getRaceAttributes(newCharacterForm.cRace.data),
                                                       "weapon": {"wName": "", "wAbility": ""},
                                                       "gift": {"gName": "", "gAbility": ""},
                                                       "weight": newCharacterForm.cWeight.data,
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