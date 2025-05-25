import streamlit as st
st.set_page_config(layout="wide")  # Cambiar de wide a centered
# Usar CSS para ajustar el alto de la pantalla
st.markdown("""
    <style>
        .main {
            height: 100vh;
            display: flex;
            flex-direction: column;

        }
            
        .block-container {
            flex: 1;
            overflow-y: auto;
            padding: 1rem;
        }
            
        .st-emotion-cache-t1wise {
            padding-left: 5%;
            padding-right: 5%;
        }
            
        img {
            max-height: 50vh;
            object-fit: cover;
        } 
    
        .st-emotion-cache-ocsh0s {
            background-color: #1f77b4;
            color: whitesmoke;
        }
            
        .st-emotion-cache-ocsh0s:hover {
            background-color: whitesmoke ;
            border-color: #1f77b4;
            color: #1f77b4;
        }
        
        .st-emotion-cache-rjm97v{
            background-color: #1f77b4;
            color: whitesmoke;
        }
        
        .st-emotion-cache-rjm97v:hover{
            background-color: whitesmoke ;
            border-color: #1f77b4;
            color: #1f77b4;
        }
        
        .st-emotion-cache-ocsh0s:focus:not(:active) {
            background-color: #1f77b4;
            border-color: whitesmoke;
            color: whitesmoke;
        }
        
    </style>
""", unsafe_allow_html=True)

import torch
import torch.nn as nn
import torchvision.transforms as transforms
import timm
import torch.nn.functional as F
from PIL import Image
import os
import pandas as pd
import matplotlib.pyplot as plt
import joblib


# Título
st.title("🔍 Predicción de Accidentes por Región, Clima y Año")

# Cargar modelo y columnas
@st.cache_resource
def load_model():
    modelo = joblib.load('modelo_accidentes_por_region.pkl')
    columnas = joblib.load('columnas_modelo.pkl')
    return modelo, columnas

modelo, columnas_modelo = load_model()

# Listas de opciones (ajusta según tus datos reales)
regiones = ['Auckland', 'Wellington', 'Canterbury', 'Otago']  # Actualiza con tus regiones
climas = ['Fine', 'Rain', 'Snow', 'Fog', 'Wind']              # Actualiza con tus climas
años = list(range(2024, 2031))                                # Puedes ajustar los años

# Formulario de entrada
with st.form("form_prediccion"):
    col1, col2 = st.columns(2)
    with col1:
        region = st.selectbox("📍 Región", regiones)
    with col2:
        weather = st.selectbox("🌦️ Clima", climas)

    año = st.selectbox("📅 Año", años)

    submitted = st.form_submit_button("Predecir Accidentes")

# Si se envió el formulario
if submitted:
    # Crear DataFrame con la entrada
    df_input = pd.DataFrame([{
        'region': region,
        'weatherA': weather,
        'crashYear': año
    }])

    # Codificar las variables igual que en entrenamiento
    X_input = pd.get_dummies(df_input)
    X_input = X_input.reindex(columns=columnas_modelo, fill_value=0)

    # Hacer la predicción
    prediccion = modelo.predict(X_input)[0]

    # Mostrar el resultado
    st.markdown(f"""
        <div style='background-color:#1f77b4; padding:20px; border-radius:5px; margin-top:20px;'>
            <h3 style='color:white; text-align:center;'>🚗 Predicción de Accidentes</h3>
            <h1 style='color:white; text-align:center;'>{prediccion:.2f} accidentes estimados</h1>
            <p style='color:white; text-align:center;'>en <b>{region}</b> con clima <b>{weather}</b> en el año <b>{año}</b>.</p>
        </div>
    """, unsafe_allow_html=True)