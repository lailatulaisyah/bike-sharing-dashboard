import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Konfigurasi halaman
st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")
st.title("🚲 Bike Sharing Dashboard")


# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("day.csv")
    df["dteday"] = pd.to_datetime(df["dteday"])
    df["season"] = df["season"].map({1: "🌸 Spring", 2: "☀️ Summer", 3: "🍂 Fall", 4: "❄️ Winter"})
    df["weathersit"] = df["weathersit"].map({ 1: "☀️ Sunny", 2: "☁️ Cloudy", 3: "🌧️ Rainy", 4: "⛈️ Heavy rain - Stormy"})
    return df

df = load_data()

# Sidebar filter
st.sidebar.header(" ▼ Filter Data")
selected_season = st.sidebar.multiselect("🌞 Select season:", df["season"].unique(), default=df["season"].unique())
selected_weather = st.sidebar.multiselect("🌤️ Select weather:", df["weathersit"].unique(), default=df["weathersit"].unique())

filtered_df = df[(df["season"].isin(selected_season)) & (df["weathersit"].isin(selected_weather))]
# Setelah filtered_df dibuat
if filtered_df.empty:
    st.warning("Please select season and weather on the data filter!")
else:

# Statistik ringkasan
    col1, col2, col3 = st.columns(3)
    col1.metric("**Total Peminjaman**", f"{filtered_df['cnt'].sum():,}")
    col2.metric("**Rata-rata Harian**", f"{filtered_df['cnt'].mean():.0f}")
    col3.metric("**Hari Terbanyak**", filtered_df.loc[filtered_df['cnt'].idxmax(), 'dteday'].strftime('%Y-%m-%d'))

# Load data
day_df = pd.read_csv("day.csv")
hour_df = pd.read_csv('hour.csv')

# Mapping label musim dan cuaca
season_map = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
weather_map = {1: "Sunny", 2: "Cloudy", 3: "Rainy"}

hour_df['season'] = hour_df['season'].map(season_map)
day_df['season'] = day_df['season'].map(season_map)
day_df['weathersit'] = day_df['weathersit'].map(weather_map)
hour_df['weathersit'] = hour_df['weathersit'].map(weather_map)

# Rata-rata peminjaman per jam per musim
avg_hourly = hour_df.groupby(['hr', 'season'])['cnt'].mean().reset_index()

# Plot 1: Lineplot jam vs musim
st.subheader("Rata-rata Peminjaman Sepeda per Jam Berdasarkan Musim")
fig1, ax1 = plt.subplots(figsize=(12, 6))
sns.lineplot(data=avg_hourly, x='hr', y='cnt', hue='season', palette='tab10', ax=ax1)
ax1.set_xlabel('Jam (0–23)')
ax1.set_ylabel('Jumlah Peminjaman')
ax1.grid(True)
st.pyplot(fig1)

# Pastikan dteday bertipe datetime
day_df['dteday'] = pd.to_datetime(day_df['dteday'])

# Filter 1 tahun terakhir
max_date = day_df['dteday'].max()
start_date = max_date - pd.Timedelta(days=365)
last_year = day_df.loc[day_df['dteday'].between(start_date, max_date)].copy()

# Agregasi bulanan per kondisi cuaca
last_year['month'] = last_year['dteday'].dt.to_period('M').dt.to_timestamp()
monthly = last_year.groupby(['month', 'weathersit'])['cnt'].mean().reset_index()

# Plot 2: Lineplot bulanan per kondisi cuaca
st.subheader("Rata-rata Peminjaman Bulanan Berdasarkan Kondisi Cuaca (1 Tahun Terakhir)")
fig2, ax2 = plt.subplots(figsize=(12, 5))
sns.lineplot(data=monthly, x='month', y='cnt', hue='weathersit', marker='o', ax=ax2)
ax2.set_xlabel('Bulan')
ax2.set_ylabel('Rata‑rata Jumlah Peminjaman')
plt.xticks(rotation=45)
st.pyplot(fig2)

# Insight tambahan
st.markdown("""
### Insight 
- Penggunaan sepeda paling tinggi terjadi pada jam 07:00 – 08:00 dan 17:00 - 19:00, terutama pada hari kerja.
- Musim gugur (fall) dan panas (summer) menunjukkan volume peminjaman tertinggi, kemungkinan karena cuaca yang mendukung dan aktivitas luar ruangan yang meningkat.
- Polanya konsisten, bentuk kurva di semua musim sama (dua puncak di pagi dan sore)
- Cuaca cerah (sunny) menunjukkan tingkat peminjaman tertinggi sepanjang tahun.
- Cuaca mendung/berawan (cloudy) menempati posisi menengah.
- Cuaca hujan (rainy) menunjukkan peminjaman terendah sepanjang tahun.
            
**Cuaca adalah faktor dominan: hari cerah mendorong penggunaan sepeda, sedangkan hujan menurunkan penggunaan sepeda**

## Saran/rekomendasi 
- Tingkatkan pasokan sepeda dengan permintaan puncak untuk mengurangi out‑of‑stock saat cuaca cerah meningkat.
- Adakan promosi atau diskon pada cuaca berawan dan hujan untuk mendorong penggunaan sepeda.
- Sediakan jas hujan saat musim hujan
""")