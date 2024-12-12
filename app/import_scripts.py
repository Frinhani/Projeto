import requests
import pandas as pd
import zipfile
import os
import sqlite3

# Configuração do banco de dados
DB_MAIN = "database.db"  # Banco principal gerenciado pelo SQLAlchemy
DB_SECONDARY = "dados_cvm.sqlite"  # Banco secundário para backup
EXTRACTION_PATH = "extracted_files"  # Diretório de extração de arquivos ZIP
df = {}  # Dicionário para armazenar DataFrames temporariamente

# Função genérica para salvar dados no banco usando pandas
def salvar_no_banco(dataframe, table_name, db_path):
    """
    Salva o DataFrame em uma tabela do banco SQLite.

    Args:
        dataframe (pd.DataFrame): O DataFrame a ser salvo.
        table_name (str): O nome da tabela.
        db_path (str): Caminho do banco de dados SQLite.
    """
    try:
        with sqlite3.connect(db_path) as conn:
            dataframe.to_sql(table_name, conn, if_exists="replace", index=False)
            print(f"Tabela '{table_name}' salva com sucesso em {db_path}!")
    except Exception as e:
        print(f"Erro ao salvar a tabela '{table_name}' em {db_path}: {e}")

# Função para baixar um arquivo
def baixar_arquivo(url, destino):
    """
    Baixa um arquivo de uma URL e salva no caminho especificado.

    Args:
        url (str): URL do arquivo a ser baixado.
        destino (str): Caminho local onde o arquivo será salvo.
    """
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(destino, 'wb') as f:
                f.write(response.content)
            print(f"Arquivo {destino} baixado com sucesso!")
        else:
            print(f"Erro ao baixar o arquivo {url}: {response.status_code}")
    except Exception as e:
        print(f"Erro durante o download do arquivo {url}: {e}")

# Função para importar dados de companhias abertas
def import_companhias_abertas():
    """
    Importa dados de companhias abertas do site da CVM.
    """
    url = "https://dados.cvm.gov.br/dados/CIA_ABERTA/CAD/DADOS/cad_cia_aberta.csv"
    file_name = "cad_cia_aberta.csv"

    # Baixar o arquivo
    baixar_arquivo(url, file_name)

    # Carregar dados no pandas
    table_name = "companhias_abertas"
    try:
        df[table_name] = pd.read_csv(file_name, sep=";", encoding="latin1")
        print(f"Dados da tabela '{table_name}' carregados com sucesso!")
    except Exception as e:
        print(f"Erro ao carregar os dados do arquivo {file_name}: {e}")
        return

    # Salvar no banco principal e secundário
    salvar_no_banco(df[table_name], table_name, DB_SECONDARY)
    salvar_no_banco(df[table_name], table_name, DB_MAIN)

# Função para importar dados do formulário de referência
def import_formulario_referencia():
    """
    Importa dados do formulário de referência da CVM.
    """
    url = "https://dados.cvm.gov.br/dados/CIA_ABERTA/DOC/FRE/DADOS/fre_cia_aberta_2024.zip"
    zip_file_name = "fre_cia_aberta_2024.zip"
    target_files = [
        "fre_cia_aberta_empregado_local_faixa_etaria_2024.csv",
        "fre_cia_aberta_empregado_local_declaracao_raca_2024.csv",
        "fre_cia_aberta_empregado_local_declaracao_genero_2024.csv",
    ]

    # Baixar o arquivo ZIP
    baixar_arquivo(url, zip_file_name)

    # Extrair os arquivos do ZIP
    try:
        with zipfile.ZipFile(zip_file_name, 'r') as zip_ref:
            for file in target_files:
                if file in zip_ref.namelist():
                    zip_ref.extract(file, EXTRACTION_PATH)
                    print(f"Arquivo {file} extraído para {EXTRACTION_PATH}!")
                else:
                    print(f"Arquivo {file} não encontrado no ZIP!")
    except Exception as e:
        print(f"Erro ao extrair arquivos do ZIP {zip_file_name}: {e}")
        return

    # Processar arquivos extraídos
    for file in target_files:
        file_path = os.path.join(EXTRACTION_PATH, file)
        if os.path.exists(file_path):
            table_name = file.replace(".csv", "")
            try:
                df[table_name] = pd.read_csv(file_path, sep=";", encoding="latin1")
                print(f"Dados do arquivo '{file}' carregados com sucesso!")
                # Salvar no banco principal e secundário
                salvar_no_banco(df[table_name], table_name, DB_SECONDARY)
                salvar_no_banco(df[table_name], table_name, DB_MAIN)
            except Exception as e:
                print(f"Erro ao processar o arquivo {file}: {e}")
        else:
            print(f"Arquivo {file_path} não encontrado!")
    print("Importação do formulário de referência concluída!")
