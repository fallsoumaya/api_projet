from extensions import api, jwt
from config import Config
from flask import Flask, jsonify,request


def create_app():

    #Creating the Flask App: 

    app=Flask(__name__)
    app.config.from_object(Config)
    
    #Initializing Extensions:
    api.init_app(app)
    jwt.init_app(app)

    #Database Initialization

    from . import connexion
    connexion.init_app(app)
    

    """

    #Blueprint Registration: 

    #JWT Error Handlers

    """
    return app