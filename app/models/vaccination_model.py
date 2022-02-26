from importlib.metadata import requires
from os import stat
from app.configs.database import db

from sqlalchemy import DateTime, String, Column
from dataclasses import dataclass
from datetime import datetime, timedelta

from app.excepts.error_handlers import DifferentThanElevenCharError, WrongTypeError

@dataclass
class VaccinationModel(db.Model):
    __tablename__ = "vaccine_cards"
    cpf: str
    name: str
    first_shot_date: str
    second_shot_date: str
    vaccine_name: str
    health_unit_name: str

    cpf = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    first_shot_date = Column(DateTime, default=datetime.now())
    second_shot_date = Column(DateTime, default=(datetime.now() + timedelta(days=90)))
    vaccine_name = Column(String, nullable=False)
    health_unit_name = Column(String, nullable=False)

    @staticmethod
    def validate_cpf(cpf):
        if cpf.isnumeric() and len(cpf) == 11:
            return cpf
        
        only_numbers = filter(str.isdigit, cpf)
        only_numbers = ''.join(only_numbers)

        if len(only_numbers) != 11:
            raise DifferentThanElevenCharError(len(only_numbers))

        return only_numbers

    @staticmethod
    def check_if_str(data):
        for value in list(data.values()):
            if type(value) != str:
                raise WrongTypeError
        return

    @staticmethod
    def normalize(data):
        normalized_data = {
            "cpf": data["cpf"],
            "name": data["name"].title(),
            "vaccine_name": data["vaccine_name"].title(),
            "health_unit_name": data["health_unit_name"].title()
        }

        return normalized_data