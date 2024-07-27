# Importation des modules et fonctions nécessaires
from app.authentification import bp
from flask import jsonify, request
from flask_smorest import abort # pour lever les erreurs http
from app.messages import Message
from app.connexion import get_db, validate_password
from app.classes import UserSchema, LoginShema # J'ai changé class en classes parce que class est un keyword 
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token, decode_token
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.send_email import send_activation_email

# Route d'enregistrement d'un nouvel utilisateur
@bp.route('/register', methods=['POST'])
@bp.arguments(UserSchema, location='json', description='Registring user.', as_kwargs=True)
@bp.response(status_code=201, schema=Message, description='sending message after a registring attemp')
def register(**kwargs):
    # Récupère les informations de l'utilisateur à partir de la requête
    username = kwargs.get("username").strip()
    email = kwargs.get("email").strip()
    password = kwargs.get("password").strip()
    confirm_password = kwargs.get("confirm_password").strip()

    # Vérifie si les mots de passe correspondent
    if password != confirm_password:
        abort(409, message='Les mots de passe ne correspondent pas')
    else:
        # Connecte-toi à la base de données
        db = get_db()

        # Vérifie si l'email ou le nom d'utilisateur existent déjà
        if db.execute("select *from users where email = %s;", (email,)).fetchone() is not None:
            abort(409, message='Cet email est déjà utilisé')
        elif db.execute("select *from users where username = %s;", (username,)).fetchone() is not None:
            abort(409, message="Ce nom d'utilisateur est déjà utilisé")
        else:
            # Vérifie si le mot de passe est valide
            if validate_password(password=password):
                # Hache le mot de passe
                hashed_password = generate_password_hash(password=password)

                # Crée un nouvel utilisateur dans la base de données
                user = db.execute("select create_get_user(%s, %s, %s, %s);", (username, email, hashed_password, 2)).fetchone()['create_get_user']
                user_id = int(user[0])

                # Envoie un email d'activation à l'utilisateur
                domain = request.url_root
                print(f'this is the domain: {domain}')
                send_activation_email(user_id=user_id, email=email)

                # Renvoie un message de succès
                return jsonify(message='Compte créé avec succès. Veuillez vérifier votre email pour activer votre compte.'), 201
            else:
                # Renvoie une erreur si le mot de passe n'est pas valide
                abort(400, message="Format de mot de passe invalide, longueur minimale, majuscule, minuscule, chiffre et caractère spécial.")

# Route de connexion d'un utilisateur
@bp.route('/login', methods=['POST'])
@bp.arguments(LoginShema, location='json', description='log an user.', as_kwargs=True)
@bp.response(status_code=201, schema=Message, description='sending message after a login attemp')
def login(**kwargs):
    # Récupère les informations de connexion à partir de la requête
    email = kwargs.get("email")
    password = kwargs.get("password")

    # Connecte-toi à la base de données et récupère les informations de l'utilisateur
    db = get_db()
    user = db.execute("select *from users where email = %s;", (email,)).fetchone()

    # Vérifie si l'utilisateur existe
    if user is None:
        abort(404, message="Cet utilisateur n'existe pas")
    else:
        # Vérifie si le mot de passe est correct
        hashed_password = user['password']
        check_password = check_password_hash(pwhash=hashed_password, password=password)
        if check_password:
            # Crée des jetons d'accès et de rafraîchissement
            access_token = create_access_token(identity=user['id'], fresh=True)
            refresh_token = create_refresh_token(identity=user['id'])
            context = {
                'tokens': {
                    'access': access_token,
                    'refresh': refresh_token
                }
            }
            # Renvoie les jetons dans la réponse
            return jsonify(message=context), 200
        else:
            # Renvoie une erreur si le mot de passe est incorrect
            abort(401, message='Mot de passe incorrect')
