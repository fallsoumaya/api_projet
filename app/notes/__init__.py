from flask import Blueprint
 
bp=Blueprint('note', __name__,url_prefix='/note',description='Opération sur la gestion des notes')

import app.notes.views