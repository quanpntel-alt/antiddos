from flask import Flask, render_template
import sqlite3

app = Flask(__name__)
DB_PATH = "../ddos.db"

@app.route("/")
def dashboard():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT cluster_id, ip, packet_count, byte_total, ttl_avg, timestamp
    FROM blocked_clusters
    ORDER BY timestamp DESC
    """)
    rows = cursor.fetchall()
    conn.close()

    # Gom theo cụm
    clusters = {}
    for row in rows:
        cluster_id, ip, pkt, size, ttl, ts = row
        if cluster_id not in clusters:
            clusters[cluster_id] = {
                "ips": [], "pkt_total": 0, "size_total": 0, "ttl_total": 0, "ts": ts
            }
        clusters[cluster_id]["ips"].append(ip)
        clusters[cluster_id]["pkt_total"] += pkt
        clusters[cluster_id]["size_total"] += size
        clusters[cluster_id]["ttl_total"] += ttl

    # Chuẩn bị dữ liệu cho template
    cluster_display = []
    ttl_labels, ttl_values, size_values = [], [], []

    for cluster_id, info in clusters.items():
        ip_list = info["ips"]
        avg_ttl = round(info["ttl_total"] / len(ip_list), 2)
        cluster_display.append({
            "id": cluster_id,
            "count": len(ip_list),
            "avg_ttl": avg_ttl,
            "total_pkt": info["pkt_total"],
            "total_size": info["size_total"],
            "timestamp": info["ts"],
            "ips": ip_list
        })
        ttl_labels.append(f"Cluster {cluster_id}")
        ttl_values.append(avg_ttl)
        size_values.append(info["pkt_total"])

    return render_template("dashboard.html",
                           clusters=cluster_display,
                           ttl_labels=ttl_labels,
                           ttl_values=ttl_values,
                           size_values=size_values)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
