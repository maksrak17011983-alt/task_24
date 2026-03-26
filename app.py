import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

# 1. Налаштування сторінки
st.set_page_config(page_title="Ризики підприємств", layout="wide")

# 2. Генерація CSV даних (Фінансові, податкові, публічні ознаки)
@st.cache_data
def load_company_data():
    data = {
        'Компанія': ['ТОВ "Вектор"', 'ПП "Оріон"', 'АТ "Старт"', 'ТОВ "Меркурій"', 'ПАТ "Зеніт"'],
        'Борг_млн': [0.5, 4.2, 1.1, 8.5, 0.2],         # Фінансова ознака
        'Податковий_борг': [0, 1, 0, 1, 0],            # Податкова ознака (0 - немає, 1 - є)
        'Судові_справи': [2, 15, 3, 22, 1],            # Публічна ознака
        'Стаж_років': [10, 2, 8, 1, 15]                # Додатковий фактор
    }
    return pd.DataFrame(data)

df = load_company_data()

# 3. Обчислення інтегрального індексу ризику (0-100)
def calculate_risk(row):
    # Логіка: великий борг + податковий борг + багато судів + малий стаж = високий ризик
    score = (row['Борг_млн'] * 5) + (row['Податковий_борг'] * 30) + (row['Судові_справи'] * 2) - (row['Стаж_років'] * 2)
    return min(max(score, 0), 100) # Обмежуємо від 0 до 100

df['Індекс_ризику'] = df.apply(calculate_risk, axis=1)

# 4. Інтерфейс
st.title("🛡️ Система оцінки ризику підприємств")
st.markdown("---")

# Вибір компанії для аналізу
company_name = st.selectbox("Оберіть компанію для перевірки:", df['Компанія'])
company_info = df[df['Компанія'] == company_name].iloc[0]
risk_val = company_info['Індекс_ризику']

# 5. Візуалізація у вигляді Gauge-chart
fig = go.Figure(go.Indicator(
    mode = "gauge+number",
    value = risk_val,
    title = {'text': f"Рівень ризику: {company_name}"},
    gauge = {
        'axis': {'range': [None, 100]},
        'bar': {'color': "black"},
        'steps': [
            {'range': [0, 40], 'color': "green"},   # Низький
            {'range': [40, 70], 'color': "yellow"}, # Середній
            {'range': [70, 100], 'color': "red"}    # Високий
        ],
        'threshold': {
            'line': {'color': "white", 'width': 4},
            'suffix': '!',
            'value': risk_val
        }
    }
))

st.plotly_chart(fig, use_container_width=True)

# 6. Підсвічування компаній з високим ризиком
st.subheader("📋 Загальний реєстр та критичні показники")

def highlight_high_risk(val):
    color = 'red' if val > 70 else 'white'
    return f'background-color: {color}'

# Виводимо таблицю з підсвічуванням
st.dataframe(df.style.applymap(highlight_high_risk, subset=['Індекс_ризику']))

if risk_val > 70:
    st.error(f"⚠️ УВАГА: Компанія {company_name} має КРИТИЧНИЙ рівень ризику!")
elif risk_val > 40:
    st.warning(f"🔔 Попередження: {company_name} потребує додаткової перевірки.")
else:
    st.success(f"✅ {company_name} надійна за всіма ознаками.")
