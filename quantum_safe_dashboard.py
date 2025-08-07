import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Load benchmark data (can be replaced with uploaded CSV)
st.title("🔐 Quantum-Safe Cryptography Benchmark Dashboard")

st.markdown("""
This dashboard compares classical and quantum-safe cryptographic protocols used in the Dark Web communication ecosystem.
Upload your benchmark CSV file below or use the sample dataset.
""")

uploaded_file = st.file_uploader("📤 Upload your benchmark CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
else:
    # Sample benchmark data
    data = {
        "Protocol": ["RSA 2048", "ECC", "Kyber-512", "Dilithium-2", "QKD (Sim)"],
        "Key Exchange Time (ms)": [120, 85, 20, 25, 10],
        "Encryption Time (ms)": [95, 70, 18, 22, 12],
        "Decryption Time (ms)": [90, 68, 15, 21, 11],
        "Key Size (Bytes)": [256, 128, 800, 1600, 0],
        "Anonymity Level": ["Medium", "Medium", "High", "High", "High"],
        "Quantum Resistance": ["Low", "Low", "High", "High", "Very High"],
        "Resource Usage (MB)": [15, 12, 40, 60, 25],
        "Security Score (/10)": [5, 6, 9, 9, 10]
    }
    df = pd.DataFrame(data)

st.subheader("🔍 Raw Benchmark Data")
st.dataframe(df)

# Feature 1: Metric Comparison with Plotly
metric = st.selectbox("📈 Select Metric to Compare", df.columns[1:-2])
st.subheader(f"📊 {metric} Comparison")
fig_bar = px.bar(df, x="Protocol", y=metric, color="Protocol", text=metric)
st.plotly_chart(fig_bar)

# Feature 2: Anonymity Level & Quantum Resistance Pie Charts
col1, col2 = st.columns(2)

with col1:
    st.subheader("🕵️ Anonymity Level Distribution")
    anon_counts = df["Anonymity Level"].value_counts()
    fig_anon = px.pie(names=anon_counts.index, values=anon_counts.values, title="Anonymity Level")
    st.plotly_chart(fig_anon)

with col2:
    st.subheader("🧪 Quantum Resistance Distribution")
    qres_counts = df["Quantum Resistance"].value_counts()
    fig_qres = px.pie(names=qres_counts.index, values=qres_counts.values, title="Quantum Resistance")
    st.plotly_chart(fig_qres)

# Feature 3: Heatmap of Performance Metrics
st.subheader("📊 Heatmap of Performance Metrics")
perf_cols = ["Key Exchange Time (ms)", "Encryption Time (ms)", "Decryption Time (ms)", "Resource Usage (MB)", "Security Score (/10)"]
fig_heat, ax = plt.subplots()
sns.heatmap(df[perf_cols].set_index(df['Protocol']), annot=True, cmap="YlGnBu")
st.pyplot(fig_heat)

# Feature 4: Radar Chart (if enough numeric metrics)
from math import pi
import matplotlib.pyplot as plt

def radar_chart(df, metrics):
    categories = metrics
    N = len(categories)
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    for i, row in df.iterrows():
        values = [row[m] for m in categories]
        values += values[:1]
        angles = [n / float(N) * 2 * pi for n in range(N)]
        angles += angles[:1]
        ax.plot(angles, values, label=row['Protocol'])
        ax.fill(angles, values, alpha=0.1)
    ax.set_xticks([n / float(N) * 2 * pi for n in range(N)])
    ax.set_xticklabels(categories)
    plt.legend(loc='upper right', bbox_to_anchor=(1.3, 1))
    return fig

st.subheader("📡 Radar Chart: Protocol Performance Overview")
radar_metrics = ["Key Exchange Time (ms)", "Encryption Time (ms)", "Decryption Time (ms)", "Security Score (/10)"]
radar_fig = radar_chart(df, radar_metrics)
st.pyplot(radar_fig)

# Footer
st.markdown("---")
st.markdown("Created for: *Next-Generation Quantum-Safe Cryptography for the Dark Web*")
