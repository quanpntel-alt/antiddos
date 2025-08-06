import time
import pandas as pd
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
from suricata_reader import read_eve_snapshot
from utils.ip_blocker import create_ipset, block_ip
import sqlite3
from datetime import datetime

DB_PATH = "ddos.db"
CLUSTER_INTERVAL = 10  # Giây giữa mỗi lần quét mới

# 🗃️ Khởi tạo database nếu chưa có
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS blocked_clusters (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cluster_id INTEGER,
        ip TEXT,
        packet_count INTEGER,
        byte_total INTEGER,
        ttl_avg REAL,
        timestamp TEXT
    )
    """)
    conn.commit()
    conn.close()

# 💾 Lưu cụm IP bị chặn vào SQLite
def save_cluster_to_db(cluster_df):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    timestamp = datetime.utcnow().isoformat()

    for _, row in cluster_df.iterrows():
        cursor.execute("""
        INSERT INTO blocked_clusters (cluster_id, ip, packet_count, byte_total, ttl_avg, timestamp)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (
            row['cluster'], row['ip'], row['packet_count'],
            row['byte_total'], row['ttl_avg'], timestamp
        ))

    conn.commit()
    conn.close()

# 🧠 Gom cụm IP bằng DBSCAN
def cluster_ips(df):
    if df.empty:
        return pd.DataFrame()

    features = df[['packet_count', 'byte_total', 'ttl_avg']]
    scaled = StandardScaler().fit_transform(features)

    model = DBSCAN(eps=1.0, min_samples=3)
    df['cluster'] = model.fit_predict(scaled)
    return df

# 🚫 Chặn IP của từng cụm
def process_clusters(df):
    valid_clusters = df[df['cluster'] != -1]['cluster'].unique()

    for cluster_id in valid_clusters:
        group = df[df['cluster'] == cluster_id]
        if len(group) < 5:
            continue  # Bỏ qua cụm nhỏ

        print(f"\n[!!!] Cluster DDoS #{cluster_id}: {len(group)} IPs")

        for ip in group['ip']:
            block_ip(ip)

        save_cluster_to_db(group)

# 🔁 Vòng lặp chính
def main():
    print("[*] Starting DDoS Cluster Engine...")
    init_db()
    create_ipset()

    while True:
        snapshot = read_eve_snapshot()

        if not snapshot:
            time.sleep(CLUSTER_INTERVAL)
            continue

        # Chuyển snapshot thành DataFrame
        rows = []
        for ip, stats in snapshot.items():
            ttl_list = stats['ttl_list']
            ttl_avg = sum(ttl_list) / len(ttl_list) if ttl_list else 0

            rows.append({
                'ip': ip,
                'packet_count': stats['count'],
                'byte_total': stats['size'],
                'ttl_avg': ttl_avg
            })

        df = pd.DataFrame(rows)
        clustered = cluster_ips(df)
        process_clusters(clustered)

        time.sleep(CLUSTER_INTERVAL)

if __name__ == "__main__":
    main()
