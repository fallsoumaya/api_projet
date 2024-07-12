"""
import postgresql

# Les informations de connexion
user = 'soumaya'
password = 'root'
host = 'localhost'  
port = 5432  
database = 'prompts'

# Ouvrir la connexion à la base de données
db = postgresql.open(f'pq://{user}:{password}@{host}:{port}/{database}')


# Liste des noms de tables
tables = ["groupes","groupes_users","prompts", "roles", "statuts","tokens_block_list","users"]
#...
for table in tables:
    cur = conn.cursor()
    cur.execute("SELECT * FROM {}".format(table))
    rows = cur.fetchall()
    for row in rows:
        print(row)
        print("")
#cur.close()
#conn.close()
"""


"""
import psycopg

try:
    conn = psycopg.connect(
        user="soumaya",
        password="root",
        host="localhost",
        port="5432",
        dbname="prompts"
    )

    # Liste des noms de tables
    tables = ["groupes","groupes_users","prompts", "roles", "statuts","tokens_block_list","users"]
    #...
    for table in tables:
        cur = conn.cursor()
        cur.execute("SELECT * FROM {}".format(table))
        rows = cur.fetchall()
        for row in rows:
            print(row)
            print("")
    cur.close()
    conn.close()

except (Exception, psycopg.Error) as error:
    print("Erreur lors de la connexion à PostgreSQL :", error)

# Ajout des données de l'application dans la base de données avec des requêtes sql
"""



import os
import dotenv
from getpass import getpass
import psycopg
from psycopg.rows import dict_row
from werkzeug.security import generate_password_hash
import click
from flask import current_app, g
from .send_email import send_activation_email

# Charge les variables d'environnement depuis le fichier .env
dotenv.load_dotenv()

def get_db():
    """
    Obtient une connexion à la base de données.
    
    La connexion est stockée dans l'objet 'g' pour être réutilisée
    au lieu de créer une nouvelle connexion à chaque fois.
    """
    if 'db' not in g:
        g.db = psycopg.connect(
            user="soumaya",
            password="root",
            host="localhost",
            port="5432",
            dbname="prompts")
    return g.db

def close_db(e=None):
    """
    Ferme la connexion à la base de données.
    
    Cette fonction est appelée à la fin de chaque requête.
    """
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    """
    Initialise la base de données en exécutant les commandes SQL
    dans le fichier 'schema.sql'.
    """
    conn = get_db()
    with current_app.open_resource('schema.sql') as f:
        with conn.cursor() as cur:
            cur.execute(f.read().decode('utf8'))
            conn.commit()

@click.command('init-db')
def init_db_command():
    """
    Efface les données existantes et crée de nouvelles tables.
    
    Cette commande peut être exécutée dans le terminal par l'utilisateur.
    """
    init_db()
    click.echo('La base de données a été initialisée.')

import re

def is_valid_email(email):
    """
    Vérifie si une adresse email est valide.
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email)

def validate_password(password):
    """
    Vérifie si un mot de passe respecte les règles de complexité suivantes :
    - Au moins 12 caractères
    - Au moins une majuscule
    - Au moins une minuscule
    - Au moins un chiffre
    - Au moins un caractère spécial
    """
    pattern = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@#$%^&*])[A-Za-z\d@#$%^&*]{12,}$"
    return bool(re.match(pattern, password))

def user_input(field: str, password: bool = False) -> str:
    """
    Demande une entrée à l'utilisateur et la valide.
    
    Args:
        field (str): Le nom du champ (par exemple, 'username' ou 'email').
        password (bool): Si True, masque l'entrée de l'utilisateur.
    
    Returns:
        str: L'entrée de l'utilisateur validée.
    """
    while True:
        if password:
            result = getpass(prompt=f'{field}: ')
            if not result:
                print(f'{field} ne peut pas être vide. Veuillez réessayer.')
            else:
                return result
        else:
            result = input(f'{field}: ').strip()
            if not result:
                print(f'{field} ne peut pas être vide. Veuillez réessayer.')
            else:
                db = get_db()
                if field == 'username':
                    exist = db.execute("SELECT username FROM users WHERE username = %s;", (result,)).fetchone()
                    if exist:
                        print(f'Attention : {result} est déjà utilisé. Veuillez choisir un autre nom d\'utilisateur.')
                    else:
                        return result
                elif field == 'email':
                    if is_valid_email(result):
                        exist = db.execute("SELECT email FROM users WHERE email = %s;", (result,)).fetchone()
                        if exist:
                            print(f'Attention : {result} est déjà utilisé. Veuillez choisir une autre adresse email.')
                        else:
                            return result
                    else:
                        print('Format d\'email invalide. Veuillez réessayer.')

@click.command('create-admin')
def create_admin_user():
    """
    Crée un utilisateur administrateur.
    
    Cette commande peut être exécutée dans le terminal par l'utilisateur.
    """
    username = user_input('Nom d\'utilisateur')
    email = user_input('Email')
    password = user_input('Mot de passe', True)
    
    if validate_password(password):
        hashed_password = generate_password_hash(password)
        db = get_db()
        db.execute("INSERT INTO users (username, email, password, role) VALUES (%s, %s, %s, %s)", (username, email, hashed_password, 'admin'))
        send_activation_email(email)
        click.echo('Utilisateur administrateur créé avec succès.')
    else:
        click.echo('Le mot de passe ne respecte pas les règles de complexité. Veuillez réessayer.')




def init_app(app):
    """
    Initialise l'application Flask.
    
    Enregistre les fonctions close_db() et les commandes init-db et create-admin.
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(create_admin_user)
