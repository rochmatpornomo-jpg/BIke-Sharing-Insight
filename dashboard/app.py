
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="Bike Sharing Insights", page_icon="🚲", layout="wide")
st.title("🚲 Bike Sharing Insights")
st.caption("Dashboard eksplorasi permintaan penyewaan sepeda Capital Bikeshare, Washington D.C. | 2011–2012")

@st.cache_data
def load_data():
    folder = Path(__file__).parent
    daily = pd.read_csv(folder / "day.csv", parse_dates=["dteday"])
    hourly = pd.read_csv(folder / "hour.csv", parse_dates=["dteday"])
    daily["Tahun"] = daily["yr"].map({0: "2011", 1: "2012"})
    hourly["Tahun"] = hourly["yr"].map({0: "2011", 1: "2012"})
    season = {1:"Spring", 2:"Summer", 3:"Fall", 4:"Winter"}
    weather = {1:"Cerah / sedikit berawan", 2:"Berkabut / berawan",
               3:"Hujan ringan / salju ringan", 4:"Cuaca ekstrem"}
    for df in (daily, hourly):
        df["Musim"] = df["season"].map(season)
        df["Kondisi cuaca"] = df["weathersit"].map(weather)
    hourly["Tipe hari"] = hourly["workingday"].map({1:"Hari kerja", 0:"Akhir pekan/libur"})
    return daily, hourly

day, hour = load_data()
st.sidebar.header("Filter dashboard")
years = st.sidebar.multiselect("Tahun", ["2011", "2012"], default=["2011", "2012"])
seasons = ["Spring", "Summer", "Fall", "Winter"]
chosen_seasons = st.sidebar.multiselect("Musim", seasons, default=seasons)
filtered_day = day[day["Tahun"].isin(years) & day["Musim"].isin(chosen_seasons)]
filtered_hour = hour[hour["Tahun"].isin(years) & hour["Musim"].isin(chosen_seasons)]

if filtered_day.empty or filtered_hour.empty:
    st.warning("Tidak ada data untuk kombinasi filter tersebut. Silakan ubah filter.")
    st.stop()

total = int(filtered_day["cnt"].sum())
avg_day = filtered_day["cnt"].mean()
peak_hour = filtered_hour.groupby("hr")["cnt"].mean().idxmax()
peak_value = filtered_hour.groupby("hr")["cnt"].mean().max()
c1,c2,c3 = st.columns(3)
c1.metric("Total penyewaan (harian)", f"{total:,.0f}")
c2.metric("Rata-rata penyewaan per hari", f"{avg_day:,.0f}")
c3.metric("Jam dengan rata-rata tertinggi", f"{int(peak_hour):02d}:00", f"{peak_value:,.0f} sepeda/jam")

st.divider()
tab1, tab2, tab3 = st.tabs(["Tren & musim", "Pola per jam", "Cuaca"])
with tab1:
    left,right = st.columns(2)
    monthly = filtered_day.assign(Bulan=filtered_day["dteday"].dt.to_period("M").astype(str)).groupby("Bulan",as_index=False)["cnt"].mean()
    left.plotly_chart(px.line(monthly, x="Bulan", y="cnt", markers=True,
                      title="Rata-rata penyewaan harian per bulan",
                      labels={"cnt":"Rata-rata sepeda/hari"}), use_container_width=True)
    season_avg = filtered_day.groupby("Musim",as_index=False)["cnt"].mean()
    right.plotly_chart(px.bar(season_avg, x="Musim", y="cnt", color="Musim",
                      title="Rata-rata penyewaan menurut musim",
                      labels={"cnt":"Rata-rata sepeda/hari"}), use_container_width=True)
    year_avg = filtered_day.groupby("Tahun",as_index=False)["cnt"].mean()
    st.plotly_chart(px.bar(year_avg, x="Tahun", y="cnt", text_auto=".0f",
                   title="Perbandingan rata-rata penyewaan harian per tahun"), use_container_width=True)

with tab2:
    profile = filtered_hour.groupby(["hr","Tipe hari"],as_index=False)["cnt"].mean()
    st.plotly_chart(px.line(profile,x="hr",y="cnt",color="Tipe hari",markers=True,
                   title="Rata-rata penyewaan per jam: hari kerja vs akhir pekan/libur",
                   labels={"hr":"Jam","cnt":"Rata-rata sepeda/jam"}), use_container_width=True)
    top = filtered_hour.groupby("hr",as_index=False)["cnt"].mean().sort_values("cnt",ascending=False).head(5)
    st.subheader("Lima jam dengan rata-rata permintaan tertinggi")
    st.dataframe(top.rename(columns={"hr":"Jam","cnt":"Rata-rata penyewaan"}), use_container_width=True, hide_index=True)

with tab3:
    weather_avg = filtered_day.groupby("Kondisi cuaca",as_index=False)["cnt"].mean().sort_values("cnt",ascending=False)
    st.plotly_chart(px.bar(weather_avg,x="Kondisi cuaca",y="cnt",color="Kondisi cuaca",
                   title="Rata-rata penyewaan harian menurut kondisi cuaca",
                   labels={"cnt":"Rata-rata sepeda/hari"}), use_container_width=True)
    st.info("Kategori cuaca mengikuti Readme dataset. Hasil merupakan perbandingan deskriptif, bukan bukti hubungan sebab-akibat.")

st.divider()
st.subheader("Catatan interpretasi")
st.markdown("""
- Gunakan pola jam sibuk untuk membantu perencanaan redistribusi armada.
- Gunakan perbedaan musim dan cuaca sebagai masukan perencanaan kapasitas.
- Data berasal dari Washington D.C. pada 2011–2012, sehingga pola tidak otomatis mewakili kota atau periode lain.
""")
with st.expander("Tentang data"):
    st.write("Dataset Bike Sharing dari Capital Bikeshare. `day.csv` berisi agregasi harian dan `hour.csv` berisi agregasi per jam. Kolom `cnt` adalah total penyewaan, yaitu `casual + registered`.")
