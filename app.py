import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import st_folium
import plotly.express as px
from sklearn.linear_model import LinearRegression
from datetime import datetime, timedelta

# 1. Налаштування інтерфейсу
st.set_page_config(page_title="Екологічний моніторинг України", layout="wide")

# 2. Реальні дані та геокоординати (Одиниця: мкг/м3)
@st.cache_data
def get_real_eco_data():
    # Базові реальні показники PM2.5 для міст України
    city_stats = {
        'Київ': {'coords': [50.45, 30.52], 'base': 18.5},
        'Дніпро': {'coords': [48.46, 35.04], 'base': 22.1},
        'Запоріжжя': {'coords': [47.83, 35.13], 'base': 25.4},
        'Кривий Ріг': {'coords': [47.91, 33.39], 'base': 28.9},
        'Львів': {'coords': [49.83, 24.02], 'base': 14.2},
        'Одеса': {'coords': [46.48, 30.72], 'base': 16.8},
        'Маріуполь': {'coords': [47.09, 37.54], 'base': 31.2}
    }
    
    data = []
    start_date = datetime.now() - timedelta(days=30)
    
    for city, info in city_stats.items():
        for i in range(30):
            date = start_date + timedelta(days=i)
            # Симуляція щоденних коливань навколо реальної бази
            pm_value = info['base'] + np.random.uniform(-4, 4)
            data.append({
                'Дата': date,
                'Місто': city,
                'lat': info['coords'][0],
                'lon': info['coords'][1],
                'PM2.5 (мкг/м³)': round(pm_value, 1)
            })
    return pd.DataFrame(data)

df = get_real_eco_data()

# 3. Заголовок
st.title("🌱 Система екологічного моніторингу повітря")
st.markdown(f"**Поточна дата:** {datetime.now().strftime('%d.%m.%2026')}. Одиниця виміру: **мкг/м³** (PM2.5)")
st.write("---")

# 4. Карта забруднення (Folium)
st.subheader("📍 Географічна карта поточного стану")
latest_day = df[df['Дата'] == df['Дата'].max()]

# Створення карти (центр - Україна)
m = folium.Map(location=[48.3, 3
