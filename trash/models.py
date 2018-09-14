from flask_sqlalchemy import SQLAlchemy
import datetime

db  =  SQLAlchemy()
class BASEMODEL (db.Model):
    #Base data model for all projects
    __abstract__ = True
    def __init__(self,*args):
        super().__init__(*args)
    def __repr__(self):
        #define a base way to print model
        return '%s%s' % (self.__class__.__name__,{
            column:  value
            for column,value in self._to_dict().items()
        })
    def json(self):
        """
                Define a base way to jsonify models, dealing with datetime objects
        """
        return {
            column: value if not isinstance(value, datetime.date) else value.strftime('%Y-%m-%d')
            for column, value in self._to_dict().items()
        }
class Station(BASEMODEL,db.Model):
    """Model for the stations table"""
    __tablename__ = 'stations'

    id = db.Column(db.Integer, primary_key = True)
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)
