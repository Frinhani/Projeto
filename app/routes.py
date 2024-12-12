from flask import render_template, request, redirect, url_for, jsonify
import sqlite3


# Função para inicializar as rotas
def init_routes(app):
    # Rota para a página inicial
    @app.route('/')
    def index():
        """
        Página inicial com lista de companhias e pesquisa por DENOM_SOCIAL.
        """
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        # Pesquisa por DENOM_SOCIAL
        DENOM_SOCIAL_pesquisa = request.args.get('DENOM_SOCIAL', '')
        query = """
            SELECT CNPJ_CIA, DENOM_SOCIAL, SIT 
            FROM companhias_abertas
        """
        if DENOM_SOCIAL_pesquisa:
            query += " WHERE DENOM_SOCIAL LIKE ? LIMIT 10"
            cursor.execute(query, ('%' + DENOM_SOCIAL_pesquisa + '%',))
        else:
            cursor.execute(query)

        rows = cursor.fetchall()
        conn.close()

        return render_template('index.html', companhias=rows, DENOM_SOCIAL_pesquisa=DENOM_SOCIAL_pesquisa)

    # Rota para editar companhias
    @app.route('/editar_companhia/<DENOM_SOCIAL>', methods=['GET', 'POST'])
    def editar_companhia(DENOM_SOCIAL):
        """
        Permite a edição do nome da companhia selecionada.
        """
        DENOM_SOCIAL_original = DENOM_SOCIAL.replace('-', ' ').replace('/', '-')

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM companhias_abertas WHERE DENOM_SOCIAL=?", (DENOM_SOCIAL_original,))
        companhia = cursor.fetchone()

        if request.method == 'POST':
            novo_nome = request.form['denom_social']
            cursor.execute("UPDATE companhias_abertas SET DENOM_SOCIAL=? WHERE DENOM_SOCIAL=?", 
                           (novo_nome, DENOM_SOCIAL_original))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

        conn.close()
        return render_template('editar_companhia.html', companhia=companhia)

    # Função genérica para construir dados de dashboards
    def construir_dados(query_base, filtros, parametros):
        """
        Constrói e executa a consulta para os dashboards.
        """
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        if filtros:
            query_base += " WHERE " + " AND ".join(filtros)
        cursor.execute(query_base, parametros)
        row = cursor.fetchone()
        conn.close()
        return row

    # Rota para o dashboard de raça
    @app.route('/dashboard_raca')
    def dashboard_raca():
        """
        Exibe o dashboard de raça para a companhia selecionada.
        """
        companhia = request.args.get('companhia', '')
        return render_template('dashboard_raca.html', companhia=companhia)

    @app.route('/dados_raca', methods=['GET'])
    def dados_raca():
        """
        Fornece os dados de raça para o dashboard.
        """
        regiao = request.args.get('regiao', '')
        companhia = request.args.get('companhia', '')
        query = """
            SELECT 
                SUM(Quantidade_Amarelo), 
                SUM(Quantidade_Branco), 
                SUM(Quantidade_Preto), 
                SUM(Quantidade_Pardo), 
                SUM(Quantidade_Indigena), 
                SUM(Quantidade_Outros), 
                SUM(Quantidade_Sem_Resposta)
            FROM fre_cia_aberta_empregado_local_declaracao_raca_2024
        """
        filtros, parametros = [], []
        if regiao:
            filtros.append("Local = ?")
            parametros.append(regiao)
        if companhia:
            filtros.append("Nome_Companhia = ?")
            parametros.append(companhia)

        row = construir_dados(query, filtros, parametros)
        if not row or all(value is None for value in row):
            return jsonify({"mensagem": "Nenhum dado encontrado para os filtros aplicados."})

        total = sum(row) if row else 0
        data = {key: value / total * 100 if total > 0 else 0 for key, value in zip(
            ["Amarelo", "Branco", "Preto", "Pardo", "Indígena", "Outros", "Sem Resposta"], row)}

        return jsonify({"dados": data})

    # Rota para o dashboard de gênero
    @app.route('/dashboard_genero')
    def dashboard_genero():
        """
        Exibe o dashboard de gênero para a companhia selecionada.
        """
        companhia = request.args.get('companhia', '')
        return render_template('dashboard_genero.html', companhia=companhia)

    @app.route('/dados_genero', methods=['GET'])
    def dados_genero():
        """
        Fornece os dados de gênero para o dashboard.
        """
        regiao = request.args.get('regiao', '')
        companhia = request.args.get('companhia', '')
        query = """
            SELECT 
                SUM(Quantidade_Feminino), 
                SUM(Quantidade_Masculino), 
                SUM(Quantidade_Nao_Binario), 
                SUM(Quantidade_Outros), 
                SUM(Quantidade_Sem_Resposta)
            FROM fre_cia_aberta_empregado_local_declaracao_genero_2024
        """
        filtros, parametros = [], []
        if regiao:
            filtros.append("Local = ?")
            parametros.append(regiao)
        if companhia:
            filtros.append("Nome_Companhia = ?")
            parametros.append(companhia)

        row = construir_dados(query, filtros, parametros)
        if not row or all(value is None for value in row):
            return jsonify({"mensagem": "Nenhum dado encontrado para os filtros aplicados."})

        total = sum(row) if row else 0
        data = {key: value / total * 100 if total > 0 else 0 for key, value in zip(
            ["Feminino", "Masculino", "Não Binário", "Outros", "Sem Resposta"], row)}

        return jsonify({"dados": data})

    # Rota para o dashboard de faixa etária
    @app.route('/dashboard_faixa_etaria')
    def dashboard_faixa_etaria():
        """
        Exibe o dashboard de faixa etária para a companhia selecionada.
        """
        companhia = request.args.get('companhia', '')
        return render_template('dashboard_faixa_etaria.html', companhia=companhia)

    @app.route('/dados_faixa_etaria', methods=['GET'])
    def dados_faixa_etaria():
        """
        Fornece os dados de faixa etária para o dashboard.
        """
        regiao = request.args.get('regiao', '')
        companhia = request.args.get('companhia', '')
        query = """
            SELECT 
                SUM(Quantidade_Ate30Anos), 
                SUM(Quantidade_30a50Anos), 
                SUM(Quantidade_Acima50Anos)
            FROM fre_cia_aberta_empregado_local_faixa_etaria_2024
        """
        filtros, parametros = [], []
        if regiao:
            filtros.append("Local = ?")
            parametros.append(regiao)
        if companhia:
            filtros.append("Nome_Companhia = ?")
            parametros.append(companhia)

        row = construir_dados(query, filtros, parametros)
        if not row or all(value is None for value in row):
            return jsonify({"mensagem": "Nenhum dado encontrado para os filtros aplicados."})

        total = sum(row) if row else 0
        data = {key: value / total * 100 if total > 0 else 0 for key, value in zip(
            ["Até 30 Anos", "30 a 50 Anos", "Acima de 50 Anos"], row)}

        return jsonify({"dados": data})
