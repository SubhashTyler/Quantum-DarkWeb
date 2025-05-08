import hashlib
import json
import time
import base64
import secrets
import pandas as pd
import numpy as np
from cryptography.fernet import Fernet
from sklearn.cluster import KMeans
from datetime import datetime
import random
import streamlit as st

# Simulated Dark Web Data

def generate_simulated_data(n_transactions=1000):
    countries = ['US', 'RU', 'CN', 'BR', 'IN', 'IR', 'DE', 'FR', 'UK', 'NG']
    data = {
        "transaction_id": [f"TX{i}" for i in range(n_transactions)],
        "wallet_address": [f"addr{i}" for i in range(n_transactions)],
        "amount": np.random.uniform(0.1, 10.0, n_transactions),
        "timestamp": [datetime.now().strftime("%Y-%m-%d %H:%M:%S") for _ in range(n_transactions)],
        "country": [random.choice(countries) for _ in range(n_transactions)]
    }
    return pd.DataFrame(data)

# QKD Key Simulation

def simulate_qkd_key():
    raw_key = secrets.token_bytes(32)
    return base64.urlsafe_b64encode(raw_key)

def encrypt_data(data, key):
    fernet = Fernet(key)
    return fernet.encrypt(json.dumps(data).encode())

def decrypt_data(encrypted_data, key):
    fernet = Fernet(key)
    return json.loads(fernet.decrypt(encrypted_data).decode())

# Blockchain Classes

class Block:
    def __init__(self, index, data, previous_hash, timestamp, role, user):
        self.index = index
        self.data = data
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.user = user
        self.role = role
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = f"{self.index}{self.data}{self.previous_hash}{self.timestamp}{self.user}{self.role}"
        return hashlib.sha256(block_string.encode()).hexdigest()

    def to_dict(self):
        return {
            "Index": self.index,
            "Timestamp": datetime.fromtimestamp(self.timestamp).strftime('%Y-%m-%d %H:%M:%S'),
            "Hash": self.hash,
            "Previous Hash": self.previous_hash,
            "User": self.user,
            "Role": self.role,
            "Data": self.data[:100] + b"...".decode() if isinstance(self.data, bytes) else str(self.data)[:100]
        }

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.access_logs = []

    def create_genesis_block(self):
        return Block(0, "Genesis Block", "0", time.time(), "system", "admin")

    def add_block(self, data, user="system", role="admin"):
        previous_block = self.chain[-1]
        new_block = Block(len(self.chain), data, previous_block.hash, time.time(), role, user)
        self.chain.append(new_block)
        self.log_access(user, role, "store_data")
        return new_block

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]
            if current.hash != current.calculate_hash() or current.previous_hash != previous.hash:
                return False
        return True

    def log_access(self, user, role, action):
        self.access_logs.append({
            "user": user,
            "role": role,
            "action": action,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

    def get_all_blocks(self):
        return [block.to_dict() for block in self.chain]

# Anonymization & Ethics

def anonymize_data(df):
    df['wallet_address'] = df['wallet_address'].apply(
        lambda x: hashlib.sha256(x.encode()).hexdigest()[:10]
    )
    return df

def check_ethical_compliance(df):
    if any(df['wallet_address'].str.contains('addr')):
        raise ValueError("Data not fully anonymized!")
    return True

def detect_anomalies(df):
    return df[df['amount'] > 9.5]

# Clustering & Analytics

def analyze_data(df):
    X = df[['amount']].values
    kmeans = KMeans(n_clusters=2, random_state=42)
    df['cluster'] = kmeans.fit_predict(X)
    insights = {
        "high_value_cluster": df[df['cluster'] == 1]['amount'].mean(),
        "low_value_cluster": df[df['cluster'] == 0]['amount'].mean(),
        "suspicious_transactions": len(df[df['amount'] > 5.0])
    }
    return insights, df

# Streamlit Dashboard

def run_dashboard(blockchain, df, insights, anomalies, decrypted_data):
    st.title("🔐 Quantum-Enhanced Blockchain Dashboard")

    st.sidebar.title("📋 Navigation")
    view = st.sidebar.radio("Select a view:", [
        "Blockchain Summary",
        "Show All Blocks",
        "Blockchain Size",
        "Show Anonymized Data",
        "Export Anonymized Data",
        "Suspicious Transactions",
        "Cluster Summaries",
        "Show Decrypted Data",
        "Access Log",
        "Is Blockchain Valid?",
        "Show Insights"
    ])

    if view == "Blockchain Summary":
        st.metric("Total Blocks", len(blockchain.chain))
        st.metric("Chain Valid", blockchain.is_chain_valid())

    elif view == "Show All Blocks":
        st.subheader("🧱 All Blockchain Blocks")
        st.dataframe(pd.DataFrame(blockchain.get_all_blocks()))

    elif view == "Blockchain Size":
        st.subheader("📦 Blockchain Size")
        st.write(f"Total number of blocks: {len(blockchain.chain)}")

    elif view == "Show Anonymized Data":
        st.subheader("🕵️ Anonymized Data Sample")
        st.dataframe(df.head(50))

    elif view == "Export Anonymized Data":
        st.subheader("📤 Export Anonymized Data")
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("Download CSV", csv, "anonymized_data.csv", "text/csv")

    elif view == "Suspicious Transactions":
        st.subheader("⚠️ Suspicious Transactions (Amount > 9.5)")
        st.dataframe(anomalies)

    elif view == "Cluster Summaries":
        st.subheader("🔍 Cluster Analysis")
        st.write(df.groupby('cluster')['amount'].describe())

    elif view == "Show Decrypted Data":
        st.subheader("🔓 Decrypted Data Sample")
        st.dataframe(decrypted_data.head(50))

    elif view == "Access Log":
        st.subheader("📝 Access Log")
        st.dataframe(pd.DataFrame(blockchain.access_logs))

    elif view == "Is Blockchain Valid?":
        st.subheader("✅ Blockchain Validation")
        st.write("Blockchain is valid." if blockchain.is_chain_valid() else "Blockchain is NOT valid!")

    elif view == "Show Insights":
        st.subheader("📈 Insights from Analysis")
        st.json(insights)

# Main Driver

def main():
    data = generate_simulated_data()
    anonymized_data = anonymize_data(data)
    check_ethical_compliance(anonymized_data)
    qkd_key = simulate_qkd_key()
    encrypted_data = encrypt_data(anonymized_data.to_dict(), qkd_key)

    blockchain = Blockchain()
    for i in range(50):
        blockchain.add_block(encrypted_data, user="node_operator", role="system")

    decrypted_data = pd.DataFrame(decrypt_data(encrypted_data, qkd_key))
    insights, analyzed_df = analyze_data(decrypted_data)
    anomalies = detect_anomalies(decrypted_data)

    blockchain.add_block(json.dumps(insights), user="law_enforcement", role="analyst")

    run_dashboard(blockchain, analyzed_df, insights, anomalies, decrypted_data)

if __name__ == "__main__":
    main()
