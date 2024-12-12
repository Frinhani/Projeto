from app import create_app, db
from app.import_scripts import import_companhias_abertas, import_formulario_referencia

# Criação da aplicação Flask
app = create_app()

def setup_database():
    """
    Função para garantir que as tabelas sejam criadas e os dados importados.
    """
    with app.app_context():
        # Criar as tabelas no banco de dados
        db.create_all()
        print("Tabelas criadas com sucesso no banco de dados!")

        # Importar os dados para o banco de dados
        print("Importando dados das companhias abertas...")
        import_companhias_abertas()
        print("Dados das companhias abertas importados com sucesso!")

        print("Importando dados do formulário de referência...")
        import_formulario_referencia()
        print("Dados do formulário de referência importados com sucesso!")

# Configuração para execução
if __name__ == "__main__":
    setup_database()  # Configurar o banco de dados e importar dados
    app.run(debug=True)
