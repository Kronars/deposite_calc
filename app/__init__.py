import json

from flask import Flask
from flask import request, Response
from flask import jsonify

from app.validation import validate_deposite
from app.calculation import deposite_calc, increase_days


def create_app():
    app = Flask(__name__)

    @app.route('/deposite/', methods=['POST'])
    def deposite():
        req_json = request.get_json()

        validation_verdict = validate_deposite(req_json)

        if validation_verdict != True:
            err_resp = jsonify(error=validation_verdict)
            err_resp.status_code = 400
            return err_resp

        deposite_increase = deposite_calc(req_json)
        deposite_days = increase_days(req_json)
        json_resp = dict(zip(deposite_days, deposite_increase))

        response = Response(json.dumps(json_resp), status=200)  # при использовании jsonify или flask.json нарушается порядок элементов
        response.headers['Content-Type'] = "application/json; charset=UTF-8"

        return response

    return app
