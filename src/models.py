from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()



class User(db.Model):
    __tablename__ = "user"
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True, nullable=False)
    fullname = db.Column(db.String(250), unique=False, nullable=False)
    lastname = db.Column(db.String(250), unique=False, nullable=False)
    password = db.Column(db.String(250), unique=False, nullable=False)
    characterfavorites = db.relationship('CharacterFavorite',backref='user', lazy=True)
    planetfavorites = db.relationship('PlanetFavorite', backref='user', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "fullname": self.fullname,
            "lastname": self.lastname,
            "characterfavorites": list(map(lambda x: x.serializebyUser(), self.characterfavorites)),
            "planetfavorites": list(map(lambda x: x.serializebyUser(), self.planetfavorites)),
            
        }

    def serializeFavorites(self):
        return {
            "id": self.id,
            "characterfavorites": list(map(lambda x: x.serializebyUser(), self.characterfavorites)),
            "planetfavorites": list(map(lambda x: x.serializebyUser(), self.planetfavorites)),
            
        }

class Character(db.Model):
    __tablename__ = "character"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    description = db.Column(db.String(500), unique=False, nullable=False)
    height = db.Column(db.Integer, unique=False, nullable=False)
    hair_color = db.Column(db.String(50), unique=False, nullable=False)
    skin_color = db.Column(db.String(50), unique=False, nullable=False)
    eye_color = db.Column(db.String(50), unique=False, nullable=False)
    birth_year = db.Column(db.String(50), unique=False, nullable=False)
    gender = db.Column(db.String(25), unique=False, nullable=False)
    favorites = db.relationship('CharacterFavorite', backref="character", lazy=True)

    def __repr__(self):
        return '<Character %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "height": self.height,
            "hair_color": self.hair_color,
            "skin_color": self.skin_color,
            "eye_color": self.eye_color,
            "birth_year": self.birth_year,
            "gender": self.gender,
            "favorites": list(map(lambda x: x.serializebyCharacter(), self.favorites))
            
        }

class Planet(db.Model):
    __tablename__ = "planet"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    description = db.Column(db.String(500), unique=False, nullable=False)
    diameter = db.Column(db.Integer, unique=False, nullable=False)
    rotation_period = db.Column(db.Integer, unique=False, nullable=False)
    orbital_period = db.Column(db.Integer, unique=False, nullable=False)
    gravity = db.Column(db.String(50), unique=False, nullable=False)
    population = db.Column(db.Integer, unique=False, nullable=False)
    climate = db.Column(db.String(25), unique=False, nullable=False)
    terrain = db.Column(db.String(25), unique=False, nullable=False)
    surface_water = db.Column(db.Integer, unique=False, nullable=False)
    favorites = db.relationship('PlanetFavorite', backref="Planet", lazy=True)
    def __repr__(self):
        return '<Planet %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "diameter": self.diameter,
            "rotation_period": self.rotation_period,
            "orbital_period": self.orbital_period,
            "gravity": self.gravity,
            "population": self.population,
            "climate": self.climate,
            "terrain": self.terrain,
            "surface_water": self.surface_water,
            "favorites": list(map(lambda x: x.serializebyPlanet(), self.favorites))
            
        }

class CharacterFavorite(db.Model):
    __tablename__ = 'characterfavorite'
    
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('user.id'))
    characterid = db.Column(db.Integer, db.ForeignKey('character.id'))

    def __repr__(self):
        return '<CharacterFavorite %r>' % self.userid

    def serializebyUser(self):
        return {
            "id": self.id,
            "characterid": self.characterid,            
            
        }

    def serializebyCharacter(self):
        return {
            "id": self.id,
            "userid": self.userid,            
            
        }

class PlanetFavorite(db.Model):
    __tablename__ = 'planetfavorite'
    
    id = db.Column(db.Integer, primary_key=True)
    planetid = db.Column(db.Integer, db.ForeignKey('planet.id'))
    userid = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def __repr__(self):
        return '<PlanetFavorite %r>' % self.userid

    def serializebyUser(self):
        return {
            "id": self.id,
            "planetid": self.planetid,            
            
        }

    def serializebyPlanet(self):
        return {
            "id": self.id,
            "userid": self.userid,            
           
        }