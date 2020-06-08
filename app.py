from flask import Flask, request, jsonify
import result
from models.schema.user import UserSchema

app = Flask(__name__)
user_schema = UserSchema()

@app.errorhandler(404)
def method_404(e):
    return result.result(404, "requested URL was not found on the server")


@app.errorhandler(405)
def method_405(e):
    return result.result(405, "http method is not allowed for the requested URL")

# --------------------------------------------------------------------------------------


@app.route('/', methods=["GET"])
def hello_world():
    return 'Restful api server v1.0.1'


@app.route('/rest/ping', methods=["GET"])
def ping():
    return result.result(200, "ping successful", "Welcome to restful api server.")

# --------------------------------------------------------------------------------------

@app.route('/rest/post', methods=["POST"])
def post():
    json_data = request.get_json()
    data = [
        {
            'name': 123
        }
    ]
    
    try:
        json_check = user_schema.load(json_data)
    except:
        return result.result(400, "please check your parameters")
    data.append(json_check)
    return jsonify(data)

if __name__ == '__main__':
    from common.ma import ma
    ma.init_app(app)
    app.run(debug=True)