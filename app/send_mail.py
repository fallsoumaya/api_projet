from flask import url_for, request
from flask_jwt_extended import create_access_token
from flask_mail import Message
import datetime
from extensions import mail

def generate_activation_link(user_id):
    token = create_access_token(identity=user_id, expires_delta=datetime.timedelta(hours=15))
    domain = f"{request.scheme}://{request.host}"
    return f"{domain}{url_for('auth.activate', token=token)}"

def send_activation_email(user_id, email):
    activation_link = generate_activation_link(user_id)
    msg = Message(subject="Activate Your Account", recipients=[email])
    msg.body = f'Please click the link to activate your account: {activation_link}'
    try:
        mail.send(msg)
        print(f"Activation link sent to {email}")
    except Exception as e:
        print(f"Error sending activation link to {email}: {str(e)}")
