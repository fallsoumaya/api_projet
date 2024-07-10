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

