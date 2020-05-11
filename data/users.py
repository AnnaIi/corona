import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from utills import CreateCoordinate


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    email = sqlalchemy.Column(sqlalchemy.String,
                              index=True, unique=True, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)
    address = sqlalchemy.Column(sqlalchemy.String, )
    chatname = sqlalchemy.Column(sqlalchemy.String, )
    lat = sqlalchemy.Column(sqlalchemy.Float)
    lon = sqlalchemy.Column(sqlalchemy.Float)
    is_ill = sqlalchemy.Column(sqlalchemy.Boolean, default=False)

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    def create_address(self, address):
        try:
            coordinates = CreateCoordinate.get_coordinate(address)
            self.lat = coordinates[0]
            self.lon = coordinates[1]
        except Exception as e:
            return False
        return True
