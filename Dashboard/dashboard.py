import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Konfigurasi halaman
st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")

st.title("🚲 Bike Sharing Dashboard")
st.markdown("Analisis tren peminjaman sepeda berdasarkan data harian dari layanan bike sharing.")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("day.csv")
    df["dteday"] = pd.to_datetime(df["dteday"])
    df["season"] = df["season"].map({1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"})
    df["weathersit"] = df["weathersit"].map({
        1: "Cerah/Berawan ringan",
        2: "Kabut + Awan",
        3: "Hujan ringan + Salju ringan",
        4: "Hujan deras + Badai"
    })
    return df

df = load_data()

# Sidebar filter
st.sidebar.header("🔍 Filter Data")
selected_season = st.sidebar.multiselect("Pilih Musim:", df["season"].unique(), default=df["season"].unique())
selected_weather = st.sidebar.multiselect("Pilih Cuaca:", df["weathersit"].unique(), default=df["weathersit"].unique())

filtered_df = df[(df["season"].isin(selected_season)) & (df["weathersit"].isin(selected_weather))]

# Statistik ringkasan
st.subheader("📊 Statistik Ringkasan")
col1, col2, col3 = st.columns(3)
col1.metric("Total Peminjaman", f"{filtered_df['cnt'].sum():,}")
col2.metric("Rata-rata Harian", f"{filtered_df['cnt'].mean():.0f}")
col3.metric("Hari Terbanyak", filtered_df.loc[filtered_df['cnt'].idxmax(), 'dteday'].strftime('%Y-%m-%d'))

# Visualisasi tren harian
st.subheader("📈 Tren Peminjaman Harian")
fig1, ax1 = plt.subplots(figsize=(12, 4))
sns.lineplot(data=filtered_df, x="dteday", y="cnt", color="blue")
plt.title("Jumlah Peminjaman Sepeda per Hari")
plt.xlabel("Tanggal")
plt.ylabel("Jumlah Peminjaman")
st.pyplot(fig1)

# Visualisasi berdasarkan musim
st.subheader("🌤️ Distribusi Peminjaman Berdasarkan Musim")
fig2, ax2 = plt.subplots()
sns.boxplot(data=filtered_df, x="season", y="cnt", palette="Set3")
plt.title("Distribusi Jumlah Peminjaman per Musim")
plt.xlabel("Musim")
plt.ylabel("Jumlah Peminjaman")
st.pyplot(fig2)

# Visualisasi berdasarkan cuaca
st.subheader("☁️ Distribusi Peminjaman Berdasarkan Cuaca")
fig3, ax3 = plt.subplots()
sns.boxplot(data=filtered_df, x="weathersit", y="cnt", palette="Set2")
plt.title("Distribusi Jumlah Peminjaman per Kondisi Cuaca")
plt.xlabel("Kondisi Cuaca")
plt.ylabel("Jumlah Peminjaman")
plt.xticks(rotation=15)
st.pyplot(fig3)