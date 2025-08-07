import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import numpy as np
from math import pi

# Dashboard Title
st.set_page_config(page_title="Quantum-Safe Cryptography for the Dark Web", layout="wide")
st.title("🕸️ Next-Generation Quantum-Safe Cryptography for the Dark Web")

st.markdown("""
This interactive dashboard evaluates and compares advanced cryptographic protocols including Post-Quantum Cryptography (PQC), Quantum Key Distribution (QKD), and Quantum Randomness.
Use it to assess their suitability for secure and anonymous Dark Web communication.
""")

# Data Upload Option
uploaded_file = st.file_uploader("📤 Upload your cryptographic benchmark CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
else:
    # Simulated Dataset
    protocols = [
        "RSA 2048", "RSA 4096", "ECC", "AES-256",
        "Kyber", "Dilithium", "SPHINCS+", "NTRU", "McEliece", "Rainbow", "Falcon",
        "BB84", "E91", "B92", "SARG04", "COW", "Decoy State",
        "QRNG - Entropy", "QRNG - Vacuum Noise"
    ]

    key_exchange = [120, 230, 85, 30, 20, 25, 45, 33, 50, 35, 40, 12, 14, 15, 18, 22, 20, 10, 11]
    encryption =   [95, 185, 70, 12, 18, 22, 38, 20, 55, 25, 35, 11, 13, 13, 15, 16, 15, 8, 9]
    decryption =   [90, 180, 68, 10, 15, 21, 40, 19, 52, 27, 30, 10, 12, 11, 13, 14, 13, 7, 9]
    key_size =     [256, 512, 128, 32, 800, 1600, 4100, 1087, 1357824, 1280, 1240, 0, 0, 0, 0, 0, 0, 0, 0]
    anonymity =    ["Medium"]*4 + ["High"]*7 + ["Very High"]*6 + ["Very High"]*2
    resistance =   ["Low"]*4 + ["High", "High", "Very High", "High", "Very High", "High", "Ultra High"] + ["Ultimate"]*6 + ["Ultimate"]*2
    usage =        [15, 30, 12, 10, 40, 60, 120, 38, 200, 50, 45, 25, 26, 27, 30, 28, 29, 14, 15]
    score =        [5, 6, 6, 7, 9.2, 9.5, 9.3, 8.8, 9.7, 8.5, 9.0, 10, 10, 10, 10, 10, 10, 10, 10]

    if all(len(lst) == len(protocols) for lst in [key_exchange, encryption, decryption, key_size, anonymity, resistance, usage, score]):
        df = pd.DataFrame({
            "Protocol": protocols,
            "Key Exchange Time (ms)": key_exchange,
            "Encryption Time (ms)": encryption,
            "Decryption Time (ms)": decryption,
            "Key Size (Bytes)": key_size,
            "Anonymity Level": anonymity,
            "Quantum Resistance": resistance,
            "Resource Usage (MB)": usage,
            "Security Score (/10)": score
        })
    else:
        st.error("Simulated data arrays are not of equal length. Please check data consistency.")

if 'df' in locals():
    # Show Raw Data
    st.subheader("📄 Raw Benchmark Data")
    st.dataframe(df, use_container_width=True)

    # Metric Comparison
    st.subheader("📊 Protocol Metric Comparison")
    metric = st.selectbox("Select a performance metric:", df.columns[1:-2])
    fig_bar = px.bar(df, x="Protocol", y=metric, color="Quantum Resistance", text=metric)
    fig_bar.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_bar, use_container_width=True)

    # Distribution Charts
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🔒 Anonymity Level Distribution")
        fig_anon = px.pie(df, names="Anonymity Level", title="Anonymity Levels")
        st.plotly_chart(fig_anon)

    with col2:
        st.subheader("🧬 Quantum Resistance Levels")
        fig_qres = px.pie(df, names="Quantum Resistance", title="Quantum Resistance")
        st.plotly_chart(fig_qres)

    # Heatmap
    st.subheader("🌡️ Heatmap: Protocol Performance")
    perf_cols = ["Key Exchange Time (ms)", "Encryption Time (ms)", "Decryption Time (ms)", "Resource Usage (MB)", "Security Score (/10)"]
    fig_heat, ax = plt.subplots(figsize=(12, 7))
    sns.heatmap(df[perf_cols].set_index(df['Protocol']), annot=True, cmap="YlGnBu", fmt=".1f")
    st.pyplot(fig_heat)

    # Radar Chart
    st.subheader("📡 Radar Chart: Comparative Protocol Profile")
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
        ax.set_title("Protocol Radar View")
        plt.legend(loc='upper right', bbox_to_anchor=(1.4, 1))
        return fig

    radar_metrics = ["Key Exchange Time (ms)", "Encryption Time (ms)", "Decryption Time (ms)", "Security Score (/10)"]
    st.pyplot(radar_chart(df, radar_metrics))

    # Filtering
    st.subheader("🧮 Advanced Filtering Options")
    col1, col2 = st.columns(2)
    with col1:
        min_score = st.slider("Minimum Security Score", 0.0, 10.0, 7.0, 0.1)
    with col2:
        max_resource = st.slider("Maximum Resource Usage (MB)", 5, 250, 100)

    filtered_df = df[(df["Security Score (/10)"] >= min_score) & (df["Resource Usage (MB)"] <= max_resource)]
    st.markdown(f"Protocols matching filter: **{len(filtered_df)}**")
    st.dataframe(filtered_df, use_container_width=True)

    # Footer
    st.markdown("---")
    st.markdown("**Research Project**: *Next-Generation Quantum-Safe Cryptography for the Dark Web: Leveraging PQC, QKD, and Quantum Randomness*  ")
    st.markdown("Developed by: Research Team | Secure Cryptographic Systems | 2025")
else:
    st.warning("Dataset could not be loaded. Please verify the benchmark data.")
