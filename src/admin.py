import os
from flask_admin import Admin
from models import db, User, Character, Planet, FavoriteCharacter, FavoritePlanet
from flask_admin.contrib.sqla import ModelView
from wtforms.fields import SelectField



def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3')

    with app.app_context():

        class CharacterAdmin(ModelView):
            form_columns = ['name', 'genre', 'race', 'skin_color', 'hair_color', 'eye_color', 'planet_id']
            form_choices = {
                'planet_id': [(str(p.id), p.name) for p in Planet.query.all()]
            }

        class FavoriteCharacterAdmin(ModelView):
            form_columns = ['user_id', 'character_id']
            form_choices = {
                'user_id': [(str(u.id), u.name) for u in User.query.all()],
                'character_id': [(str(c.id), c.name) for c in Character.query.all()]
            }

        class FavoritePlanetAdmin(ModelView):
            form_columns = ['user_id', 'planet_id']
            form_choices = {
                'user_id': [(str(u.id), u.name) for u in User.query.all()],
                'planet_id': [(str(p.id), p.name) for p in Planet.query.all()]
            }


    # Add your models here, for example this is how we add a the User model to the admin
    admin.add_view(ModelView(User, db.session))
    admin.add_view(CharacterAdmin(Character, db.session))
    admin.add_view(ModelView(Planet, db.session))
    admin.add_view(FavoriteCharacterAdmin(FavoriteCharacter, db.session))
    admin.add_view(FavoritePlanetAdmin(FavoritePlanet, db.session))

    # You can duplicate that line to add mew models
    # admin.add_view(ModelView(YourModelName, db.session))