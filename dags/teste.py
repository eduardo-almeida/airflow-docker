import requests
import pandas as pd
import pytz
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime,timedelta

local = pytz.timezone('America/Sao_Paulo')
ontem = datetime.now(local) - timedelta(days=1)

dados = []
counter = 0

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': ontem,
    'catchup': False,
}

def chamada_api():
    
    for pagina in range (1, 10):

        print(f'processando página {pagina} de 10...')    

        # link API 
        url = f'https://api-dados-abertos.cearatransparente.ce.gov.br/transparencia/servidores/salarios?year=2024&month=11&page={pagina}'

        # fazendo a requisição
        response = requests.get(url, headers= {'accept': 'application/json'})

        # Guardando na lista vazia "dados" toda vez que a reguisição der certo
        if response == 200:
            data = response.json()
            dados.extend(data['data'])

        else:
            print(f'Erro na requisição:' + str(response.status_code))

    df = pd.DataFrame(dados)

    df.to_csv('servidores.csv', index=False)


with DAG(
    'chamada_api',
    description='DAG para chamada de API',
    default_args=default_args,
    schedule_interval='20 11 * * *', # Todo dia 11:15
) as dag:
    executa_api = PythonOperator(
        task_id='executa_api',
        python_callable=chamada_api,
    )

    executa_api