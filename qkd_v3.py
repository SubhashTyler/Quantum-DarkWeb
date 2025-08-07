import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set Streamlit page config
st.set_page_config(page_title="Quantum-Safe Cryptography Dashboard", layout="wide")
st.title("🔐 Quantum-Safe Cryptography Benchmark Dashboard")
st.markdown("""
This dashboard visualizes benchmark results comparing classical, post-quantum, and quantum key distribution (QKD) cryptographic protocols.
""")

# Simulated Benchmark Data
data = {
    "Protocol": [
        # Classical
        "RSA 2048", "RSA 4096", "ECC", "AES-256",

        # Post-Quantum Cryptography
        "ML-KEM (Kyber)", "ML-DSA (Dilithium)", "SLH-DSA (SPHINCS+)",
        "NTRU", "McEliece", "Rainbow", "Falcon",

        # Quantum Key Distribution
        "QKD - BB84", "QKD - E91", "QKD - B92", "QKD - SARG04", "QKD - COW", "QKD - Decoy State"
    ],
    "Key Exchange Time (ms)": [120, 230, 85, 30, 20, 25, 45, 33, 50, 35, 12, 14, 15, 18, 22, 20],
    "Encryption Time (ms)": [95, 185, 70, 12, 18, 22, 38, 20, 55, 25, 11, 13, 13, 15, 16, 15],
    "Decryption Time (ms)": [90, 180, 68, 10, 15, 21, 40, 19, 52, 27, 10, 12, 11, 13, 14, 13],
    "Key Size (Bytes)": [256, 512, 128, 32, 800, 1600, 4100, 1087, 1357824, 1280, 1056, 1100, 1000, 1024, 1088, 1072],
    "Anonymity Level": [
        "Medium", "Medium", "Medium", "Medium",
        "High", "High", "High", "High", "High", "High", "High",
        "Very High", "Very High", "Very High", "Very High", "Very High"
    ],
    "Quantum Resistance": [
        "Low", "Low", "Low", "Low",
        "High", "High", "Very High", "High", "Very High", "High", "Ultra High",
        "Ultimate", "Ultimate", "Ultimate", "Ultimate", "Ultimate"
    ],
    "Resource Usage (MB)": [15, 30, 12, 10, 40, 60, 120, 38, 200, 50, 33, 35, 36, 38, 37, 39],
    "Security Score (/10)": [5, 6, 6, 7, 9.2, 9.5, 9.3, 8.8, 9.7, 8.5, 9.0, 9.2, 9.1, 9.3, 9.4, 9.5]
}

# Create DataFrame
df = pd.DataFrame(data)

# Sidebar filters
st.sidebar.header("Filter Protocols")
selected_protocols = st.sidebar.multiselect(
    "Select cryptographic protocols to compare:",
    options=df["Protocol"].unique(),
    default=df["Protocol"].unique()
)

filtered_df = df[df["Protocol"].isin(selected_protocols)]

# Display data table
st.subheader("📊 Protocol Benchmark Table")
st.dataframe(filtered_df, use_container_width=True)

# Visualizations
st.subheader("📈 Benchmark Comparisons")

metric = st.selectbox("Select metric to visualize:", [
    "Key Exchange Time (ms)",
    "Encryption Time (ms)",
    "Decryption Time (ms)",
    "Key Size (Bytes)",
    "Resource Usage (MB)",
    "Security Score (/10)"
])

fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(data=filtered_df, x="Protocol", y=metric, palette="viridis", ax=ax)
plt.xticks(rotation=45, ha='right')
plt.ylabel(metric)
plt.title(f"Comparison of {metric}")
st.pyplot(fig)

# Legend for qualitative metrics
st.subheader("🔎 Anonymity & Quantum Resistance")
st.markdown("""
- **Anonymity Levels:** Medium < High < Very High
- **Quantum Resistance:** Low < High < Very High < Ultra High < Ultimate
""")

# Footer
st.markdown("""
---
Developed for: *Next-Generation Quantum-Safe Cryptography for the Dark Web*
""")
