from sqlalchemy import Column, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
import random
import string
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer,
                          BadSignature,
                          SignatureExpired)

Base = declarative_base()

secret_key = ''.join(random.choice(string.ascii_uppercase +
                                   string.digits) for x in range(32))


class User(Base):
    __tablename__ = 'user'
    id = Column(String, primary_key=True)
    email = Column(String(64), unique=True, nullable=False)
    picture = Column(String)

    def generate_auth_token(self, expiration=600):
        s = Serializer(secret_key, expires_in=expiration)
        return s.dumps({'id': self.id})

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
                'picture': self.picture,
                'email': self.email,
                'name': self.name
                }

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(secret_key)
        try:
            data = s.loads(token)
        except SignatureExpired:
            # Valid Token, but expired
            return None
        except BadSignature:
            # Invalid Token
            return None
        user_id = data['id']
        return user_id


class Category(Base):
    __tablename__ = 'category'
    name = Column(String(24), primary_key=True)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
                'name': self.name
                }


class Item(Base):
    __tablename__ = 'item'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    picture = Column(String)
    description = Column(String)
    price = Column(String)
    category_id = Column(String, ForeignKey('category.name'))
    owner = Column(String, ForeignKey('user.id'))
    category = relationship(Category)
    user = relationship(User)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
                'id': self.id,
                'name': self.name,
                'picture': self.picture,
                'price': self.price,
                'description': self.description
                }


engine = create_engine('sqlite:///catalog.db')
Base.metadata.create_all(engine)
