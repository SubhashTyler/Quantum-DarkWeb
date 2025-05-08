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

# Simulated Dark Web Data (Cryptocurrency Transactions)
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

# Simulate QKD Key

def simulate_qkd_key():
    raw_key = secrets.token_bytes(32)
    return base64.urlsafe_b64encode(raw_key)

def encrypt_data(data, key):
    fernet = Fernet(key)
    return fernet.encrypt(json.dumps(data).encode())

def decrypt_data(encrypted_data, key):
    fernet = Fernet(key)
    return json.loads(fernet.decrypt(encrypted_data).decode())

# Blockchain Structures
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
            previous = self.chain[i-1]
            if current.hash != current.calculate_hash():
                return False
            if current.previous_hash != previous.hash:
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

# Governance & Anonymization

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
    return df[df['amount'] > 9.5]  # Rule-based anomaly for simulation

# Data Analysis

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

# Streamlit Dashboard UI
def run_dashboard(blockchain, df, insights, anomalies):
    st.title("🔐 Quantum-Enhanced Blockchain Dashboard")

    st.subheader("Blockchain Status")
    st.metric("Total Blocks", len(blockchain.chain))
    st.metric("Chain Valid", blockchain.is_chain_valid())

    if st.checkbox("Show Blockchain Nodes"):
        st.write(pd.DataFrame(blockchain.get_all_blocks()))

    st.subheader("Access Logs")
    st.write(pd.DataFrame(blockchain.access_logs))

    st.subheader("Insights from Data Analysis")
    st.json(insights)

    st.subheader("Detected Anomalies")
    st.write(anomalies)

    st.subheader("Anonymized Transaction Data Sample")
    st.write(df.head(10))

# Main Execution
def main():
    data = generate_simulated_data()
    anonymized_data = anonymize_data(data)
    check_ethical_compliance(anonymized_data)
    qkd_key = simulate_qkd_key()
    encrypted_data = encrypt_data(anonymized_data.to_dict(), qkd_key)

    blockchain = Blockchain()
    for i in range(50):
        blockchain.add_block(encrypted_data, user="node_operator", role="system")

    decrypted_data = decrypt_data(encrypted_data, qkd_key)
    df = pd.DataFrame(decrypted_data)
    insights, analyzed_df = analyze_data(df)
    anomalies = detect_anomalies(df)

    blockchain.add_block(json.dumps(insights), user="law_enforcement", role="analyst")

    run_dashboard(blockchain, analyzed_df, insights, anomalies)

if __name__ == "__main__":
    main()
