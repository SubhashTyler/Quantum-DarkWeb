import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import numpy as np

# Load benchmark data (can be replaced with uploaded CSV)
st.title("🔐 Quantum-Safe Cryptography Benchmark Dashboard")

st.markdown("""
This dashboard compares classical and quantum-safe cryptographic protocols used in Dark Web communication.
You can upload your benchmark CSV file or explore using the extended simulated dataset.
""")

uploaded_file = st.file_uploader("📤 Upload your benchmark CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
else:
    # Extended and more realistic simulated benchmark data
    data = {
        "Protocol": [
            "RSA 2048", "RSA 4096", "ECC", "AES-256", "Kyber-512", "Kyber-1024",
            "Dilithium-2", "Dilithium-5", "Falcon-512", "SPHINCS+", "QKD (Sim)"
        ],
        "Key Exchange Time (ms)": [120, 230, 85, 30, 20, 28, 25, 33, 22, 45, 10],
        "Encryption Time (ms)": [95, 185, 70, 12, 18, 24, 22, 30, 19, 38, 12],
        "Decryption Time (ms)": [90, 180, 68, 10, 15, 22, 21, 29, 17, 40, 11],
        "Key Size (Bytes)": [256, 512, 128, 32, 800, 1500, 1600, 2800, 1300, 4100, 0],
        "Anonymity Level": ["Medium"]*4 + ["High"]*7,
        "Quantum Resistance": ["Low", "Low", "Low", "Low", "High", "Very High", "High", "Very High", "High", "Very High", "Ultra High"],
        "Resource Usage (MB)": [15, 30, 12, 10, 40, 55, 60, 85, 50, 120, 25],
        "Security Score (/10)": [5, 6, 6, 7, 9, 9.5, 9, 9.5, 8.8, 9.3, 10]
    }
    df = pd.DataFrame(data)

st.subheader("🔍 Raw Benchmark Data")
st.dataframe(df, use_container_width=True)

# Feature 1: Metric Comparison with Plotly
metric = st.selectbox("📈 Select Metric to Compare", df.columns[1:-2])
st.subheader(f"📊 {metric} Comparison")
fig_bar = px.bar(df, x="Protocol", y=metric, color="Quantum Resistance", text=metric)
fig_bar.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig_bar, use_container_width=True)

# Feature 2: Pie Charts
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
perf_cols = [
    "Key Exchange Time (ms)", "Encryption Time (ms)", "Decryption Time (ms)",
    "Resource Usage (MB)", "Security Score (/10)"
]
fig_heat, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(df[perf_cols].set_index(df['Protocol']), annot=True, cmap="YlGnBu", fmt=".1f")
st.pyplot(fig_heat)

# Feature 4: Radar Chart
from math import pi

def radar_chart(df, metrics):
    categories = metrics
    N = len(categories)
    fig, ax = plt.subplots(figsize=(7, 7), subplot_kw=dict(polar=True))
    for i, row in df.iterrows():
        values = [row[m] for m in categories]
        values += values[:1]
        angles = [n / float(N) * 2 * pi for n in range(N)]
        angles += angles[:1]
        ax.plot(angles, values, label=row['Protocol'])
        ax.fill(angles, values, alpha=0.1)
    ax.set_xticks([n / float(N) * 2 * pi for n in range(N)])
    ax.set_xticklabels(categories)
    ax.set_title("Radar View of Protocol Performance")
    plt.legend(loc='upper right', bbox_to_anchor=(1.4, 1))
    return fig

st.subheader("📡 Radar Chart: Protocol Performance Overview")
radar_metrics = ["Key Exchange Time (ms)", "Encryption Time (ms)", "Decryption Time (ms)", "Security Score (/10)"]
radar_fig = radar_chart(df, radar_metrics)
st.pyplot(radar_fig)

# Feature 5: Advanced Filtering & Sorting
st.subheader("🧮 Advanced Filtering")
col1, col2 = st.columns(2)

with col1:
    min_score = st.slider("Minimum Security Score", 0.0, 10.0, 7.0, 0.1)
    max_resource = st.slider("Maximum Resource Usage (MB)", 5, 150, 60)

filtered_df = df[(df["Security Score (/10)"] >= min_score) & (df["Resource Usage (MB)"] <= max_resource)]

st.markdown(f"Showing {len(filtered_df)} protocol(s) matching criteria.")
st.dataframe(filtered_df, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("Created for: *Next-Generation Quantum-Safe Cryptography for the Dark Web*")
