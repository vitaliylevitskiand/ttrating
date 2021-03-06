import flask_bcrypt as bcrypt
import datetime
import json

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

db = SQLAlchemy()


class Category:
    MEN = 'MEN'
    WOMEN = 'WOMEN'

    VALUES = [MEN, WOMEN]


class NameReprMixin:
    def __str__(self):
        return self.name


class TimeStampMixin:
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now,
                          onupdate=func.now)


class WorldPlayer(NameReprMixin, TimeStampMixin, db.Model):
    column_searchable_list = ('id', 'name')
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    rating = db.Column(db.Integer)
    country_code = db.Column(db.String, ForeignKey("country.code"))
    country = relationship("Country")
    category = db.Column(db.String)
    position = db.Column(db.Integer)


class WorldRating(TimeStampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    player_id = db.Column(db.Integer, ForeignKey('world_player.id'))
    player = relationship("WorldPlayer")
    position = db.Column(db.Integer)
    rating = db.Column(db.Integer)
    year = db.Column(db.Integer)
    month = db.Column(db.Integer)

    def __str__(self):
        return f'{self.player.name} {self.year}.{self.month}'


class WorldRatingList(TimeStampMixin, db.Model):
    id = db.Column(db.String, primary_key=True)
    year = db.Column(db.Integer)
    month = db.Column(db.Integer)
    def __str__(self):
        return f'World Rating {self.category} {self.year}.{self.month}'


class Country(NameReprMixin, db.Model):
    code = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)
    code_2 = db.Column(db.String)
    weight = db.Column(db.Integer)


class Player(TimeStampMixin, NameReprMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    external_id = db.Column(db.Integer, unique=True)
    position = db.Column(db.Integer)
    year = db.Column(db.Integer)
    rating = db.Column(db.Float)
    fine_rating = db.Column(db.Float)
    prev_rating = db.Column(db.Float)
    weight = db.Column(db.Float)
    max = db.Column(db.Float)
    city = db.Column(db.String, nullable=False)
    city2 = db.Column(db.String)
    category = db.Column(db.String)
    tournaments = relationship('PlayerTournament',
                               order_by="desc(PlayerTournament.index)")

    tournaments_total = db.Column(db.Integer, default=0, nullable=False)
    game_total = db.Column(db.Integer, default=0, nullable=False)
    game_won = db.Column(db.Integer, default=0, nullable=False)
    stability = db.Column(db.Integer)
    about = db.Column(db.Integer)
    photo_url = db.Column(db.String)


class RatingList(TimeStampMixin, db.Model):
    id = db.Column(db.String, primary_key=True)
    year = db.Column(db.Integer, nullable=False)
    month = db.Column(db.Integer, nullable=False)
    tournaments = db.relationship('Tournament')

    def __str__(self):
        return f'UA Rating {self.year}.{self.month:0>2}'


class Rating(TimeStampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, ForeignKey('player.id'))
    player = relationship("Player")
    position = db.Column(db.Integer)
    rating = db.Column(db.Float)
    rating_fine = db.Column(db.Float)
    weight = db.Column(db.Integer)
    max = db.Column(db.Float)
    year = db.Column(db.Integer)
    month = db.Column(db.Integer)

    def __str__(self):
        return f'{self.player.name} {self.year}.{self.month}'


class Tournament(TimeStampMixin, NameReprMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    external_id = db.Column(db.Integer, unique=True)
    rating_list_id = db.Column(db.Integer, ForeignKey('rating_list.id'))
    rating_list = relationship('RatingList')
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    judge = db.Column(db.String)
    city = db.Column(db.String)
    group = db.Column(db.String)
    description = db.Column(db.Text)
    player_total = db.Column(db.Integer)
    players_info = relationship("PlayerTournament")


class PlayerTournament(db.Model):
    player_id = db.Column(db.Integer, ForeignKey('player.id'),
                          ForeignKey('game.player_id'),
                          primary_key=True)
    tournament_id = db.Column(db.Integer, ForeignKey('tournament.id'),
                              ForeignKey('game.tournament_id'),
                              primary_key=True)
    player = relationship("Player")
    game_total = db.Column(db.Integer)

    @property
    def games(self):
        return Game.query.filter_by(player_id=self.player_id,
                                    tournament_id=self.tournament_id).all()

    index = db.Column(db.Integer)
    tournament = relationship("Tournament")
    start_rating = db.Column(db.Float)
    final_rating = db.Column(db.Float)
    start_weight = db.Column(db.Integer)
    final_weight = db.Column(db.Integer)
    delta_rating = db.Column(db.Float)
    delta_weight = db.Column(db.Integer)


class City(NameReprMixin, db.Model):
    name = db.Column(db.String, primary_key=True)
    external_id = db.Column(db.String, nullable=True)  # external name actually
    weight = db.Column(db.Integer)


class Game(TimeStampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    result = db.Column(db.Boolean)
    player_id = db.Column(db.Integer, ForeignKey('player.id'))
    player_name = db.Column(db.String)
    opponent_id = db.Column(db.Integer, ForeignKey('player.id'))
    opponent_name = db.Column(db.String)
    opponent_rating = db.Column(db.Float)
    player_rating = db.Column(db.Float)
    contribution = db.Column(db.Integer)
    tournament_id = db.Column(db.Integer, ForeignKey('tournament.id'))
    tournament = relationship('Tournament')
    date = db.Column(db.Date)

    def __str__(self):
        return f'{self.player_name} vs {self.opponent_name}'


class Topic(TimeStampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    active = db.Column(db.Boolean, default=True)
    type = db.Column(db.Integer)
    period = db.Column(db.Integer)
    name = db.Column(db.String, nullable=False)
    display_name = db.Column(db.String, default=lambda context: context.
                             get_current_parameters()['name'])
    group = db.Column(db.String)
    index = db.Column(db.Integer)
    processor = db.Column(db.String)
    _properties = db.Column(db.String, name='properties')

    def get_properties(self):
        return json.loads(self._properties)

    def set_properties(self, val):
        self._properties = json.dumps(val)

    properties = property(get_properties, set_properties)

    def __str__(self):
        return f'{self.name}'


class TopicIssue(TimeStampMixin, db.Model):
    def __init__(self, topic_id, data):
        self._data = json.dumps(data)
        self.topic_id = topic_id
        self.new = True

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.Date)
    period_date = db.Column(db.Date)
    _data = db.Column(db.Text, name='data')
    topic_id = db.Column(db.Integer, ForeignKey('topic.id'))
    topic = relationship('Topic')
    new = db.Column(db.Boolean)

    @property
    def data(self):
        return json.loads(self._data)

    def __str__(self):
        return f'{self.topic.name} {self.date}'


class LiveTournament(TimeStampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    key = db.Column(db.String)
    name = db.Column(db.String)
    is_rating = db.Column(db.Boolean)
    coefficient = db.Column(db.Float)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    judge = db.Column(db.String)
    city = db.Column(db.String)
    group = db.Column(db.String)
    description = db.Column(db.Text)
    player_total = db.Column(db.Integer)
    is_started = db.Column(db.Boolean)
    status = db.Column(db.String)
    _players = db.Column(db.String, name='players')
    _games = db.Column(db.String, name='games')

    # games : [{'player_1_number', 'player_2_number', 'result', 'score'}]
    # players {'number'{'number', 'name', 'city', 'rating', 'weight',
    # 'player_id'}

    @property
    def players(self):
        return json.loads(self._players)

    @property
    def games(self):
        return json.loads(self._games)

    def get_player(self, number):
        for p in self.players:
            if p['number'] == number:
                return p
        return None


class Sparring(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    player_id = db.Column(db.Integer, ForeignKey('player.id'))
    player = relationship('Player')
    description = db.Column(db.Text)
    price = db.Column(db.Integer)
    city = db.Column(db.String, ForeignKey('city.name'))
    location = db.Column(db.String)
    datetime = db.Column(db.DateTime)
    email = db.Column(db.String)


class Translation(db.Model):
    def __init__(self, origin, locale):
        self.id = origin + "_" + locale
        self.locale = locale

    id = db.Column(db.String, primary_key=True)
    origin = db.Column(db.String)
    locale = db.Column(db.String)
    translated = db.Column(db.String)
    model = db.Column(db.String)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    confirmed_on = db.Column(db.DateTime, nullable=True)
    player_id = db.Column(db.Integer, ForeignKey('player.id'))
    player = relationship('Player')
    language = db.Column(db.String)

    def __init__(self, email, password, confirmed, confirmed_on=None,
                 player_id=None, language=None):
        self.email = email
        self.password = bcrypt.generate_password_hash(password)
        self.registered_on = datetime.datetime.now()
        self.confirmed = confirmed
        self.confirmed_on = confirmed_on
        self.player_id = player_id
        self.language = language
