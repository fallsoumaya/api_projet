import marshmallow as ma

# Regroupement de l'ensemble des fichiers classes.py en un pour "une optimisation" et éviter trop de lignes d'importations qu'on pourrait regrouper en une seule igne


class UserSchema(ma.Schema):
    id = ma.fields.Integer(dump_only=True)
    username = ma.fields.String(required=True, error_messages={"required": {"message": "Username required", "code": 400}})
    email = ma.fields.Email(required=True, error_messages={"required": {"message": "Email required", "code": 400}})
    password = ma.fields.String(required=True, load_only=True)
    confirm_password = ma.fields.String(required=True, load_only=True)
    role = ma.fields.String(dump_only=True)


class LoginShema(ma.Schema):
    email = ma.fields.Email(required=True, error_messages={"required": {"message": "Email required", "code": 400}})
    password = ma.fields.String(required=True, error_messages={"required": {"message": "Password required", "code": 400}})


class UserCrendentialsSchema(ma.Schema): # Informations d’identification utilisateur
    email = ma.fields.Str()
    username = ma.fields.Str()


class GroupeSchema(ma.Schema):
    id = ma.fields.Int(dump_only=True)
    name = ma.fields.Str(required=True)
    description = ma.fields.Str()
    created_by = ma.fields.Int(dump_only=True)
    created_at = ma.fields.DateTime(dump_only=True)
    updated_at = ma.fields.DateTime(dump_only=True)


class PromptSchema(ma.Schema):
    id = ma.fields.Int(dump_only=True)
    prompt = ma.fields.Str(required=True)
    user_id = ma.fields.Int(required=True, dump_only=True)
    statut_id = ma.fields.Int(required=True)
    created_at = ma.fields.DateTime(dump_only=True)
    updated_at = ma.fields.DateTime(dump_only=True)


class VotesSchema(ma.Schema):
    id = ma.fields.Int(dump_only=True)
    prompt_id = ma.fields.Int(required=True)
    user_id = ma.fields.Int(required=True, dump_only=True)
    groupe_id = ma.fields.Int(required=True)
    points=ma.fields.Int(required=True) # 1 ou 2 point(s) à prendre en compte
    created_at = ma.fields.DateTime(dump_only=True)


class NotesSchema(ma.Schema):
    id = ma.fields.Int(dump_only=True)
    prompt_id = ma.fields.Int(required=True)
    user_id = ma.fields.Int(required=True, dump_only=True)
    note=ma.fields.Int(required=True) # between -10 et 10 !
    created_at = ma.fields.DateTime(dump_only=True)
    updated_at = ma.fields.DateTime(dump_only=True)