# serveur intellicarnet

## guide d'installation (développement)

- Cloner ce dépôt:
    ```
    git clone https://github.com/.../serv
    cd serv/
    ```

- Créer un environnement virtuel:
    ```
    python3 -m venv venv; source venv/bin/activate; pip3 install -r requirements.txt
    ```

- Activer le serveur:
    ```
    flask --app incarnet.server run
    ```
