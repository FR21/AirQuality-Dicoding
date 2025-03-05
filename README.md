# Data Analysis Project

## Setup Environment - Anaconda
```sh
conda create --name main-ds python=3.12
conda activate main-ds
pip install -r requirements.txt
```

## Setup Environment - Shell/Terminal
```sh
mkdir proyek_analisis_data
cd proyek_analisis_data
pipenv install
pipenv shell
pip install -r requirements.txt
```

## Run Streamlit App
```sh
streamlit run dashboard/dashboard.py
