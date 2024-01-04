# serveur intellicarnet

## guide d'installation (développement)

- Cloner ce dépôt:
    ```
    git clone https://github.com/intellicarnet/serveur
    cd serveur/
    ```

- Créer un environnement virtuel:
    ```
    python3 -m venv venv; source venv/bin/activate; pip3 install -r requirements.txt
    ```

- Activer le serveur:
    ```
    FLASK_APP=server.py python3 server.py
    ```
