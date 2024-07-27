from flask import Blueprint
 
bp=Blueprint('vote', __name__,url_prefix='/vote',description='OPération sur la gestion des votes')

import app.votes.views