from flask import Flask, request, jsonify
import result
from models.schema.user import UserSchema
import json
from load_model import get_model_structure, get_test_model
from image_recognition import find_image
import wget
import os

app = Flask(__name__)
user_schema = UserSchema()
app.config["JSON_AS_ASCII"] = False

model_structure = get_model_structure()
test_model = get_test_model(model_structure)

@app.before_request
def before_request():
    result.write_log('info', "User requests info, path: {0}, method: {1}, ip: {2}, agent: {3}"
                     .format(str(request.path), str(request.method), str(request.remote_addr), str(request.user_agent)))

@app.after_request
def after_request(response):
    resp = response.get_json()

    if resp is not None:
        code, status, description = resp["code"], resp["status"], resp["description"]
        response_info = "Server response info, code: {0}, status: {1}, description: {2}"

        if code == 500:
            result.write_log('warning', response_info.format(code, status, description))
        else:
            result.write_log('info', response_info.format(code, status, description))

    return response

# --------------------------------------------------------------------------------------

@app.errorhandler(404)
def method_404(e):
    return result.result(404, "requested URL was not found on the server")


@app.errorhandler(405)
def method_405(e):
    return result.result(405, "http method is not allowed for the requested URL")

# --------------------------------------------------------------------------------------

@app.route('/', methods=["GET"])
def hello_world():
    test = result.result(200, "ping successful", "Welcome to restful api server.")
    return str(test[1])


@app.route('/rest/ping', methods=["GET"])
def ping():
    return result.result(200, "ping successful", "Welcome to restful api server.")

# --------------------------------------------------------------------------------------

@app.route('/rest/post', methods=["POST"])
def post():
    # get post data
    json_data = request.get_json()

    try:
        # input check by ma.Schema
        json_check = user_schema.load(json_data)
        # get json of server response
        result_json = result.result(200, "ping successful")[0].get_json()
        # logging post data
        result.write_log('info', "data: {}".format(json_data))
    except:
        return result.result(400, "please check your parameters")

    result_json['data'] = json_check

    return jsonify(result_json)

@app.route('/rest/image', methods=["POST"])
def image():
    json_data = request.get_json()
    
    try:
        image_url = json_data['image']
        local_image_filename = wget.download(image_url)

        find_image_dict = find_image(test_model, local_image_filename)
        # get json of server response
        result_json = result.result(200, "ping successful")[0].get_json()
        # logging post data
        result.write_log('info', "data: {}".format(find_image_dict))

        if os.path.exists(local_image_filename):
            os.remove(local_image_filename)
    except:
        return result.result(400, "please check your parameters")

    result_json['data'] = find_image_dict
    return jsonify(result_json)
# --------------------------------------------------------------------------------------

if __name__ == '__main__':
    from common.ma import ma
    ma.init_app(app)
    app.run(debug=True)