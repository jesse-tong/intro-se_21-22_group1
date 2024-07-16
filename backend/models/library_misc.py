from global_vars.database_init import db
from flask_login import UserMixin
from sqlalchemy import CheckConstraint
from dataclasses import dataclass
from datetime import datetime
from sqlalchemy.dialects.mysql import NVARCHAR

@dataclass
class Article(db.Model):
    __tablename__ = 'article'
    id:int = db.Column(db.Integer, primary_key=True)
    title:str = db.Column(db.String(500).with_variant(NVARCHAR(500), "mysql", "mariadb"))
    content:str = db.Column(db.String(15000).with_variant(NVARCHAR(15000), "mysql", "mariadb"))
    date:datetime = db.Column(db.DateTime, default=datetime.now)

@dataclass
class ArticleImage(db.Model):
    __tablename__ = 'user_image'
    id:int = db.Column(db.Integer, primary_key=True)
    userId:int = db.Column(db.Integer, db.ForeignKey('user.id'))
    imagePath:str = db.Column(db.String(500))