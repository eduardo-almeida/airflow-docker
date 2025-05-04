from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import requests
import pandas as pd
import os

def fetch_and_save_countries():
    url = "https://restcountries.com/v3.1/all"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    # Extrair dados úteis
    countries = []
    for country in data:
        countries.append({
            'name': country.get('name', {}).get('common', ''),
            'official_name': country.get('name', {}).get('official', ''),
            'region': country.get('region', ''),
            'subregion': country.get('subregion', ''),
            'population': country.get('population', 0),
            'area': country.get('area', 0),
        })

    df = pd.DataFrame(countries)

    os.makedirs('/opt/airflow/data', exist_ok=True)
    df.to_csv('/opt/airflow/data/paises.csv', index=False)
    print("CSV salvo com sucesso!")

# DAG
with DAG(
    dag_id='Trabalho',
    start_date=datetime(2023, 1, 1),
    schedule_interval=None,  # ou algo como '@daily'
    catchup=False,
    tags=['api', 'csv', 'countries'],
) as dag:

    fetch_task = PythonOperator(
        task_id='fetch_and_save',
        python_callable=fetch_and_save_countries
    )
