# 🛡️ DDoS Cluster Blocker

Công cụ phát hiện và chặn các cụm IP có hành vi tấn công DDoS sử dụng Suricata + Machine Learning (DBSCAN).  
Tự động đọc log từ `eve.json`, gom nhóm IP theo hành vi (TTL, packet size, packet count), cảnh báo, chặn bằng iptables/ipset, và hiển thị dashboard Flask trực quan.

---

## 🔧 Tính năng chính

- 📥 Đọc log real-time từ `Suricata eve.json`
- 📊 Trích xuất đặc trưng TTL trung bình, kích thước gói, số packet per IP
- 🧠 Gom nhóm IP bằng thuật toán **DBSCAN** (không cần xác định số cụm)
- 🚫 Tự động chặn toàn bộ IP trong cụm tấn công bằng iptables
- 🗃️ Lưu log cụm bị chặn vào **SQLite**
- 🌐 Giao diện Flask: hiển thị cụm DDoS, IP bị chặn, thống kê TTL & packet size

---

## 🖥️ Yêu cầu

- Python 3.8+
- Suricata đã bật log `eve.json`
- Linux (vì sử dụng iptables)
- Quyền root nếu muốn chặn IP thật

---

## 📦 Cài đặt

```bash
git clone https://github.com/your-org/ddos_cluster_blocker.git
cd ddos_cluster_blocker
pip install -r requirements.txt
