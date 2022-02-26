from flask import Blueprint

from app.controllers.vaccine_controller import create_vaccination_data, get_vaccination_data

bp_vaccine = Blueprint('bp_vaccine', __name__, url_prefix='/vaccinations')

bp_vaccine.get('')(get_vaccination_data)
bp_vaccine.post('')(create_vaccination_data)