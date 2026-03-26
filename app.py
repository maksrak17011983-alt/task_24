import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# Налаштування сторінки
st.set_page_config(page_title="GitHub Аналітика", layout="wide")

# Функція завантаження даних (Кешування для швидкості)
@st.cache_data(ttl=3600)
def get_github_data(user):
    url = f"https://api.github.com/users/{user}/repos?per_page=100"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

st.title("🐙 GitHub Project Monitoring Dashboard")
st.markdown("---")

# Поле введення користувача
username = st.text_input("Введіть нікнейм користувача GitHub:", value="streamlit")

if username:
    with st.spinner('Завантаження даних...'):
        raw_data = get_github_data(username)
    
    if raw_data:
        # Створення таблиці даних
        df = pd.DataFrame(raw_data)
        # Вибираємо лише необхідні стовпці згідно з ТЗ
        df = df[['name', 'stargazers_count', 'forks_count', 'open_issues_count']]
        df.columns = ['Проєкт', 'Зірки ⭐', 'Форки 🍴', 'Issues 🛠']

        # --- КРОК 2: РЕЙТИНГ ЗА ЗІРКАМИ ---
        st.subheader("🏆 ТОП-10 проєктів за популярністю")
        top_10 = df.sort_values('Зірки ⭐', ascending=False).head(10)
        fig_stars = px.bar(top_10, x='Зірки ⭐', y='Проєкт', orientation='h', 
                           color='Зірки ⭐', color_continuous_scale='Viridis',
                           text='Зірки ⭐')
        fig_stars.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_stars, use_container_width=True)

        # --- КРОК 3: ГРАФ АКТИВНОСТІ ---
        st.subheader("📈 Граф активності: Популярність vs Задачі")
        fig_activity = px.scatter(df, x='Зірки ⭐', y='Issues 🛠', size='Форки 🍴',
                                 hover_name='Проєкт', color='Issues 🛠',
                                 title="Бульбашкова діаграма (Розмір = Форки)")
        st.plotly_chart(fig_activity, use_container_width=True)

        # --- КРОК 4: АНАЛІЗ ДИНАМІКИ ---
        st.subheader("🔍 Аналітика розробки")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Всього репозиторіїв", len(df))
        with c2:
            st.metric("Сумарно зірок", df['Зірки ⭐'].sum())
        with c3:
            avg_issues = round(df['Issues 🛠'].mean(), 1)
            st.metric("Сер. кількість Issues", avg_issues)

        st.write("---")
        st.dataframe(df.sort_values('Зірки ⭐', ascending=False), use_container_width=True)
    else:
        st.error("Користувача не знайдено або ліміт запитів API вичерпано.")

st.caption("Виконано згідно з вимогами Завдання №24")
