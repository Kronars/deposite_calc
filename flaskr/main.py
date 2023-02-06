import json

from flask import request, Response

from flaskr import create_app
from validation import deposite_valid
from calculation import deposite_calc, increase_days


app = create_app()


@app.route('/deposite/', methods=['POST'])
def deposite():

    req_json = request.get_json()

    validation_verdict = deposite_valid(req_json)

    if validation_verdict != True: 
        return json.dumps({
            'error': validation_verdict
        })

    deposite_increase = deposite_calc(req_json)
    deposite_days = increase_days(req_json)
    json_resp = dict(zip(deposite_days, deposite_increase))

    full_resp = Response(json.dumps(json_resp), status=200)
    full_resp.headers['Content-Type'] = "application/json; charset=UTF-8".encode('utf-8')

    return full_resp
