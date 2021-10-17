from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from rolwithfriends.assets.forms import CreateWeaponForm, CreateClothesForm, CreateObjectForm
from rolwithfriends import mongo
from bson.objectid import ObjectId

assets = Blueprint('assets', __name__)


@assets.route('/create/assets',methods=['GET', 'POST'])
@login_required
def createAssets():
    createWForm  = CreateWeaponForm()
    createCForm = CreateClothesForm()
    createOForm = CreateObjectForm()
    if createWForm.submitWeapon.data and createWForm.is_submitted():

        existAlready = mongo.db.Weapons.find_one({"weaponName": createWForm.weaponName.data})
        if existAlready:
            flash(f'This weapon already exists!', 'warning')
        else:
            newWeapon = mongo.db.Weapons.insert_one({"weaponName": createWForm.weaponName.data,
                                        "weaponDescription": createWForm.weaponDescription.data,
                                        "weaponRarity": createWForm.weaponRarity.data,
                                        "weaponType": createWForm.weaponTypes.data,
                                        "weaponRange": createWForm.weaponRange.data,
                                        "weaponDamage": int(createWForm.weaponDamage.data),
                                        "weaponMultipliers": [float(x) for x in createWForm.weaponMultipliers.data],
                                        "weaponLimiters": [float(x) for x in createWForm.weaponLimiters.data],
                                        "weaponWeight": int(createWForm.weaponWeight.data),
                                        "weaponCost": int(createWForm.weaponCost.data)})
            if newWeapon:
                flash(f'Weapon created! It was added to the database!', 'success')
                newWp = mongo.db.Weapons.find_one({"weaponName": createWForm.weaponName.data})
                return redirect(url_for('assets.asset', asset_type = "Weapon", asset_id = newWp['_id']))
            else:
                flash(f'There was a problem creating the weapon, please try again later', 'warning')
    if createCForm.submitClothing.data and createCForm.is_submitted():
        existAlready = mongo.db.Clothes.find_one({"clothingName": createCForm.clothingName.data})
        if existAlready:
            flash(f'This clothin already exists!', 'warning')
        else:
            newClothing = mongo.db.Clothes.insert_one({
                "clothingName": createCForm.clothingName.data,
                "clothingDescription": createCForm.clothingDescription.data,
                "clothingRarity": createCForm.clothingRarity.data,
                "clothingPart": createCForm.clothingPart.data,
                "clothingSetName": createCForm.clothingSetName.data,
                "clothingWeight": createCForm.clothingWeight.data,
                "clothingCost": createCForm.clothingCost.data,
                "clothingMaterial": createCForm.clothingMaterial.data
            })
            if newClothing:
                flash(f'Clothing created! It was added to the database!', 'success')
                newCl = mongo.db.Clothes.find_one({"clothingName": createCForm.clothingName.data})
                return redirect(url_for('assets.asset', asset_type = "Clothing", asset_id = newCl['_id']))
    if createOForm.submitObject.data and createOForm.is_submitted():
        objectExists = mongo.db.Objects.find_one({"objectName": createOForm.objectName.data})
        if objectExists:
            flash(f'This object already exists!', 'warning')
        else:
            newObject = mongo.db.Objects.insert_one({
                "objectName": createOForm.objectName.data,
                "objectType": createOForm.objectType.data,
                "objectRarity": createOForm.objectRarity.data,
                "objectDescription": createOForm.objectDescription.data,
                "objectValue": int(createOForm.objectValue.data),
                "objectWeight": int(createOForm.objectWeight.data),
                "objectDurability": int(createOForm.objectDurability.data),
                "objectEffect": createOForm.objectEffect.data
            })
            if newObject:
                newObj = mongo.db.Objects.find_one({"objectName": createOForm.objectName.data})
                return redirect(url_for('assets.asset', asset_type = "Object", asset_id = newObj['_id']))
    elif request.method == 'GET':
        createOForm.objectEffect.data = "None"
    return render_template('assets/createasset.html', title="Create assets", 
                            createWForm = createWForm, createCForm = createCForm, createOForm = createOForm)


@assets.route("/asset/<string:asset_type>/<string:asset_id>")
def asset(asset_type, asset_id):
    if asset_type == "Object":
        asset = mongo.db.Objects.find_one({"_id": ObjectId(asset_id)})
        return render_template("assets/asset.html", title="Asset info", asset= asset)
    elif asset_type == "Weapon":
        asset = mongo.db.Weapons.find_one({"_id": ObjectId(asset_id)})
        return render_template("assets/weapon.html", title="Weapon info", asset = asset)
    elif asset_type == "Clothing":
        asset = mongo.db.Clothes.find_one({"_id": ObjectId(asset_id)})
        return render_template("assets/clothing.html", title="Clothing info", asset = asset)