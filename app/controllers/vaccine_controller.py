from http import HTTPStatus
from flask import request, current_app, jsonify
from app.excepts.error_handlers import DifferentThanElevenCharError, WrongTypeError
from app.models.vaccination_model import VaccinationModel
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import NotNullViolation, UniqueViolation

def get_vaccination_data():
    vaccination_data = (
        VaccinationModel.query.all()
    )

    return jsonify(vaccination_data), HTTPStatus.OK

def create_vaccination_data():
    try:        
        data = request.get_json()

        VaccinationModel.check_if_str(data)
        data = VaccinationModel.normalize(data)
        new_vaccine_data = VaccinationModel(**data)
        new_vaccine_data.cpf = VaccinationModel.validate_cpf(new_vaccine_data.cpf)
        

        current_app.db.session.add(new_vaccine_data)
        current_app.db.session.commit()

        return jsonify(new_vaccine_data), HTTPStatus.CREATED
    except IntegrityError as e:
        if isinstance(e.orig, UniqueViolation):

            return {'error': 'CPF já está cadastrado'}, HTTPStatus.CONFLICT

        if isinstance(e.orig, NotNullViolation): 
            return {'error': 'Preencha todos campos'}, HTTPStatus.BAD_REQUEST
    except DifferentThanElevenCharError as e:
        return {"error": f"CPF com {'mais' if e.args[0] > 11 else 'menos'} que 11 números."}, HTTPStatus.BAD_REQUEST

    except WrongTypeError:
        return {"error": "Todos campos devem ser strings"}, HTTPStatus.BAD_REQUEST