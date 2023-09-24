from flask import Blueprint

api = Blueprint('api', __name__)

@api.route('/login', methods=['POST'])
def api_login():
    return '',200
