from flask_jwt_extended import JWTManager
from flask_restful import Api
from flask_mail import Mail



jwt=JWTManager()

api=Api()

mail = Mail()