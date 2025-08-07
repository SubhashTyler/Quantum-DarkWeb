import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import numpy as np
from math import pi

st.set_page_config(page_title="Quantum-Safe Cryptography Dashboard", layout="wide")
st.title("🔐 Quantum-Safe Cryptography Benchmark Dashboard")

st.markdown("""
This dashboard compares Classical, Post-Quantum (PQC), and Quantum Key Distribution (QKD) cryptographic protocols.
Upload a custom benchmark file or use the default simulated benchmark dataset.
""")

uploaded_file = st.file_uploader("📤 Upload your benchmark CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
else:
    protocols = [
        # Classical
        "RSA 2048", "RSA 4096", "ECC", "AES-256",

        # Post-Quantum Cryptography
        "ML-KEM (Kyber)", "ML-DSA (Dilithium)", "SLH-DSA (SPHINCS+)",
        "NTRU", "McEliece", "Rainbow", "Falcon",

        # Quantum Key Distribution
        "QKD - BB84", "QKD - E91", "QKD - B92", "QKD - SARG04", "QKD - COW", "QKD - Decoy State"
    ]
    #
    data = {
        "Protocol": protocols,
        "Key Exchange Time (ms)": [120, 230, 85, 30, 20, 25, 45, 33, 50, 35, 12, 14, 15, 18, 22, 20],
        "Encryption Time (ms)": [95, 185, 70, 12, 18, 22, 38, 20, 55, 25, 11, 13, 13, 15, 16, 15],
        "Decryption Time (ms)": [90, 180, 68, 10, 15, 21, 40, 19, 52, 27, 10, 12, 11, 13, 14, 13],
        "Key Size (Bytes)": [256, 512, 128, 32, 800, 1600, 4100, 1087, 1357824, 1280, 0, 0, 0, 0, 0, 0],
        "Anonymity Level": ["Medium"] * 4 + ["High"] * 7 + ["Very High"] * 5,
        "Quantum Resistance": ["Low"] * 4 + ["High", "High", "Very High", "High", "Very High", "Medium", "High"] + ["Ultimate"] * 5,
        "Resource Usage (MB)": [15, 30, 12, 10, 40, 60, 120, 38, 200, 50, 25, 26, 27, 30, 28, 29],
        "Security Score (/10)": [5, 6, 6, 7, 9.2, 9.5, 9.3, 8.8, 9.7, 8.5, 10, 10, 10, 10, 10, 10]
    }
    #
    df = pd.DataFrame(data)

# Show raw data
st.subheader("🔍 Raw Benchmark Data")
st.dataframe(df, use_container_width=True)

# Feature 1: Metric Comparison
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
fig_heat, ax = plt.subplots(figsize=(12, 7))
sns.heatmap(df[perf_cols].set_index(df['Protocol']), annot=True, cmap="YlGnBu", fmt=".1f")
st.pyplot(fig_heat)

# Feature 4: Radar Chart
st.subheader("📡 Radar Chart: Protocol Performance Overview")

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

radar_metrics = ["Key Exchange Time (ms)", "Encryption Time (ms)", "Decryption Time (ms)", "Security Score (/10)"]
radar_fig = radar_chart(df, radar_metrics)
st.pyplot(radar_fig)

# Feature 5: Advanced Filtering
st.subheader("🧮 Advanced Filtering")
col1, col2 = st.columns(2)

with col1:
    min_score = st.slider("Minimum Security Score", 0.0, 10.0, 7.0, 0.1)
with col2:
    max_resource = st.slider("Maximum Resource Usage (MB)", 5, 250, 100)

filtered_df = df[(df["Security Score (/10)"] >= min_score) & (df["Resource Usage (MB)"] <= max_resource)]
st.markdown(f"Showing {len(filtered_df)} protocol(s) matching criteria.")
st.dataframe(filtered_df, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("Created for: *Next-Generation Quantum-Safe Cryptography for the Dark Web*")
