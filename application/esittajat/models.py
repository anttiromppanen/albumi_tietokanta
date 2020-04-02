from application import db
from application.models import Base

class Esittaja(Base):
    
   __tablename__ = "esittaja"

   nimi = db.Column(db.String(144), nullable=False)

   def __init__(self, nimi):
       self.nimi = nimi
