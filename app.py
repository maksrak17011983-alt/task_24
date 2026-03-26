import streamlit as st
import requests
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="GitHub Monitor", layout="wide")

# 1. ОТРИМАННЯ ДАНИХ (GitHub API)
@st.cache_data
def get_github_data(user):
    # Запит до API для отримання репозиторіїв
    url = f"https://api.github.com/users/{user}/repos?per_page=100"
    response = requests.get(url)
    return response.json() if response.status_code == 200 else None

st.title("🐙 Моніторинг проєктів у GitHub")

# Поле введення як на скріншоті
username = st.text_input("Введіть нікнейм користувача GitHub:", value="streamlit")

if username:
    data = get_github_data(username)
    
    if data:
        # Формуємо таблицю
        df = pd.DataFrame(data)[['name', 'stargazers_count', 'forks_count', 'open_issues_count']]
        df.columns = ['Проєкт', 'Зірки ⭐', 'Форки 🍴', 'Issues 🛠']

        # 2. ГРАФ АКТИВНОСТІ
        st.subheader("📈 Граф активності (Issues vs Stars)")
        fig_activity = px.scatter(df, x='Зірки ⭐', y='Issues 🛠', size='Форки 🍴',
                                 hover_name='Проєкт', color='Issues 🛠',
                                 title="Аналіз завантаженості проєктів")
        st.plotly_chart(fig_activity, use_container_width=True)

        # 3. РЕЙТИНГ ЗА ЗІРКАМИ
        st.subheader("🏆 Рейтинг за популярністю")
        top_10 = df.sort_values('Зірки ⭐', ascending=False).head(10)
        fig_stars = px.bar(top_10, x='Зірки ⭐', y='Проєкт', orientation='h', 
                           color='Зірки ⭐', text='Зірки ⭐')
        fig_stars.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_stars, use_container_width=True)

        # 4. АНАЛІЗ ДИНАМІКИ РОЗРОБКИ
        st.subheader("🔍 Показники динаміки")
        c1, c2 = st.columns(2)
        with c1:
            # Аналіз активності через середню кількість відкритих задач
            avg_issues = round(df['Issues 🛠'].mean(), 1)
            st.metric("Середня активність (Issues)", avg_issues)
        with c2:
            # Аналіз залученості через форки
            st.metric("Всього репозиторіїв", len(df))

        st.dataframe(df.sort_values('Зірки ⭐', ascending=False), use_container_width=True)
    else:
        st.error("Користувача не знайдено")
