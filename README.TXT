# Dashboard de Companhias Abertas

Este projeto consiste em uma aplicação web desenvolvida em Flask para exibir dashboards interativos com dados sobre companhias abertas, como distribuição por gênero, raça e faixa etária.

## Funcionalidades

- **Pesquisa e edição:** Busque e edite informações de companhias diretamente na aplicação.
- **Dashboards interativos:** Visualize dados percentuais por gênero, raça e faixa etária.
- **Filtros regionais:** Aplique filtros regionais para análises detalhadas.

---

## Passos para Rodar os Scripts de Importação

1. **Requisitos:** Certifique-se de ter o Python 3.11+ instalado em seu sistema.
2. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt

3. **Execute o script principal** (run.py):
   ```bash
    Copiar código: python run.py
    Os dados serão automaticamente baixados e carregados no banco de dados database.db.

4. **Passos para Executar a Aplicação Web**
    Certifique-se de ter executado os scripts de importação.
    Execute o servidor Flask:
    ```bash
        Copiar código: python run.py

    Acesse a aplicação no navegador no endereço:
    Copiar código
    http://127.0.0.1:5000/

    **Tecnologias Utilizadas**
        Linguagem: Python 3.11
        Framework Web: Flask
        Banco de Dados: SQLite
        Visualização: Plotly.js
        Outras bibliotecas:
        pandas
        requests
        zipfile
        Flask-SQLAlchemy