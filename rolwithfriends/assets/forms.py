from flask_wtf import FlaskForm
from rolwithfriends import mongo
from wtforms import StringField, SubmitField, SelectField, IntegerField, SelectMultipleField, BooleanField
from wtforms.validators import DataRequired, ValidationError

class CreateWeaponForm(FlaskForm):
    weaponName = StringField('Weapon name', validators=[DataRequired()])
    weaponDescription = StringField('Weapon description', validators=[DataRequired()])
    weaponTypes = SelectField('Weapon type', validators=[DataRequired()],choices=[('axe', 'Axe'), ('greatsword', 'Greatsword'), ('sword', 'Sword'), 
                                                    ('bow', 'Bow'), ('dagger', 'Dagger'), ('crossbow', 'Crossbow'), ('knuckles','Brass knuckles')])
    weaponRange = SelectField('Weapon type', validators=[DataRequired()],choices=[('melee', 'Melee'), ('range', 'Range')])
    weaponDamage = IntegerField('Damage', validators=[DataRequired()])
    weaponMultipliers = SelectMultipleField('Weapon multipliers', validators=[DataRequired()],choices=[(1.5, 'x 1.5'), (2, 'x 2'), (3, 'x 3'), (4, 'x 4'),
                                                                           (5, 'x 5'), (6, 'x 6'), (7, 'x 7'), (8, 'x 8'), (9, 'x 9'), (10, 'x 10')])
    weaponLimiters = SelectMultipleField('Weapon limiters', validators=[DataRequired()],choices=[(1, 'x 1'), (0.9, 'x 0.9'), (0.8, 'x 0.8'), (0.7, 'x 0.7'), (0.6, 'x 0.6'),
                                                                     (0.5, 'x 0.5'), (0.4, 'x 0.4'), (0.3, 'x 0.3'), (0.2, 'x 0.2'), (0.1, 'x 0.1'), (0, 'x 0')])
    weaponWeight = IntegerField('Weight', validators=[DataRequired()])
    weaponCost = IntegerField('Cost', validators=[DataRequired()])
    weaponRarity = SelectField('Weapon rarity', validators=[DataRequired()],choices=[('common', 'Common'), ('rare', 'Rare'),('epic','Epic'), ('legendary','Legendary')])
    submitWeapon = SubmitField('Add weapon')

    def validate_weapon_name(self, weaponName):
        existAlready = mongo.db.Weapons.find_one({"weaponName": weaponName.data})

        if existAlready:
            raise ValidationError('That username is already taken, please choose a different one')

class CreateClothesForm(FlaskForm):
    clothingName = StringField('Clothing name', validators=[DataRequired()])
    clothingDescription = StringField('Clothes description', validators=[DataRequired()])
    clothingPart = SelectField('Part of the body', validators=[DataRequired()],choices=[('head', 'Head'), ('chest', 'Chest'), ('pants', 'Pants'), 
                                                                                        ('Shoes', 'shoes')])
    clothingRarity = SelectField('Clothing rarity', validators=[DataRequired()],choices=[('common', 'Common'), ('rare', 'Rare'),('epic','Epic'), ('legendary','Legendary')])
    clothingSetName = StringField('Clothing set name', validators=[DataRequired()])
    clothingWeight = IntegerField('Weight', validators=[DataRequired()])
    clothingCost = IntegerField('Clothing cost', validators=[DataRequired()])
    clothingMaterial = StringField('Clothing material', validators=[DataRequired()])
    submitClothing = SubmitField('Add clothing')


class CreateObjectForm(FlaskForm):
    objectName = StringField('Object name', validators=[DataRequired()])
    objectType = SelectField('Object type', validators=[DataRequired()], choices=[('consumable', 'Consumable'), ('usable', 'Usable'), ('mount', 'Mount')])
    objectDescription = StringField('Object description', validators=[DataRequired()])
    objectValue = IntegerField('Object value', validators=[DataRequired()])
    objectWeight = IntegerField('Object weight', validators=[DataRequired()])
    objectDurability = IntegerField('Object durability', validators=[DataRequired()])
    objectEffect = StringField('Object effect', validators=[DataRequired()])
    objectRarity = SelectField('Object rarity', validators=[DataRequired()],choices=[('common', 'Common'), ('rare', 'Rare'),('epic','Epic'), ('legendary','Legendary')])
    submitObject = SubmitField('Add object')
