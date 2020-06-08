from flask import jsonify

# http code status
status = {
    200: 'OK',
    400: 'Bad Request',
    404: 'Not Found',
    405: 'Method Not Allowed',
    500: 'Internal Server Error'
}

# http code description (default)
default_description = {
    200: 'Successful response',
    400: 'Please check paras or query valid.',
    404: 'Please read the document to check API.',
    405: 'Please read the document to check API.',
    500: 'Please contact api server manager.'
}


def result(code, msg, description=""):

    description = default_description.get(code) if description == "" else description
    response = jsonify({
        "code": code,
        "status": status.get(code),
        "message": msg, 
        "description": description
    })

    return response, code, {'Content-Type':'application/json'}