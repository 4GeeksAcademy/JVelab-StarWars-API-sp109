from typing import List
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    singup_date: Mapped[int] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    favorite_planet = relationship("FavoritePlanet", back_populates="user")
    favorite_character = relationship("FavoriteCharacter", back_populates="user")

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "singup date": self.singup_date,
            "name": self.name,
        }

    
class Planet(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    climate: Mapped[str] = mapped_column(nullable=False)
    terrain: Mapped[str] = mapped_column(nullable=False)
    population: Mapped[int] = mapped_column(nullable=False)
    mass: Mapped[int] = mapped_column(nullable=False)

    character = relationship("Character", back_populates="planet")
    favorite_planet = relationship("FavoritePlanet", back_populates="planet")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "clima": self.climate,
            "terrain": self.terrain,
            "population": self.population,
            "mass": self.mass,
        }
    
class Character(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    genre: Mapped[str] = mapped_column(nullable=False)
    race: Mapped[str] = mapped_column(nullable=False)
    skin_color: Mapped[str] = mapped_column(nullable=False)
    eye_color: Mapped[str] = mapped_column(nullable=False)
    hair_color: Mapped[str] = mapped_column(nullable=False)

    favorite_character = relationship("FavoriteCharacter", back_populates="character")
    planet_id = mapped_column(ForeignKey("planet.id"))
    planet = relationship("Planet", back_populates="character")


    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "genre": self.genre,
            "race": self.race,
            "skin color": self.skin_color,
            "eye color": self.eye_color,
        }
    
class FavoriteCharacter(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)

    user_id = mapped_column(ForeignKey("user.id"))
    user = relationship("User", back_populates="favorite_character")
    character_id = mapped_column(ForeignKey("character.id"))
    character = relationship("Character", back_populates="favorite_character")

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user_id,
            "character": self.character_id,
        }
    
class FavoritePlanet(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)

    user_id = mapped_column(ForeignKey("user.id"))
    user = relationship("User", back_populates="favorite_planet")
    planet_id = mapped_column(ForeignKey("planet.id"))
    planet = relationship("Planet", back_populates="favorite_planet")

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user_id,
            "planet": self.planet_id,
        }