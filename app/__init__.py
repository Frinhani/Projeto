from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Instância do SQLAlchemy
db = SQLAlchemy()

def create_app():
    """
    Cria e configura a aplicação Flask.

    Retorna:
        app (Flask): Instância da aplicação Flask configurada.
    """
    # Inicializa o app Flask
    app = Flask(__name__)

    # Configurações do banco de dados
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializar o banco de dados
    db.init_app(app)

    # Registrar rotas
    from app.routes import init_routes  # Importação dinâmica para evitar dependências circulares
    init_routes(app)

    return app
