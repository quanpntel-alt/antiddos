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

🚀 Khởi chạy
1. Chạy tool phân tích + chặn IP
bash
Sao chép
Chỉnh sửa
python cluster_engine.py
Tool sẽ:

Đọc TTL/size từ suricata_reader.py

Cluster IP theo hành vi

Lưu cụm bị chặn vào SQLite (ddos.db)

Chặn IP theo cụm

2. Khởi chạy giao diện dashboard Flask
bash
Sao chép
Chỉnh sửa
cd flask_web
python app.py
Truy cập tại: http://localhost:8080
Dashboard hiển thị: cụm DDoS, TTL trung bình, IP bị chặn, biểu đồ thống kê.

🧪 Mô phỏng DDoS để test
bash
Sao chép
Chỉnh sửa
cd test
sudo python spoof_udp_gen.py
Hoặc dùng hping3:

bash
Sao chép
Chỉnh sửa
sudo hping3 --flood --udp -a 1.2.3.4 -p ++ --rand-source 192.168.1.100
📁 Cấu trúc thư mục
bash
Sao chép
Chỉnh sửa
ddos_cluster_blocker/
├── cluster_engine.py           # Gom cụm + chặn IP
├── suricata_reader.py         # Đọc TTL/size từ eve.json
├── flask_web/
│   ├── app.py                 # Flask web
│   └── templates/dashboard.html
├── utils/ip_blocker.py        # iptables/ipset handler
├── test/spoof_udp_gen.py      # DDoS giả lập
├── ddos.db                    # SQLite lưu cụm
├── requirements.txt
└── README.md
⚠️ Lưu ý bảo mật
Nên dùng ipset thay vì iptables nếu số lượng IP bị chặn > 1000

TTL và size có thể bị ngẫu nhiên hoá – cân nhắc các đặc trưng khác như burst, inter-arrival time, flag

Nên kết hợp thêm phân tích entropy theo thời gian để phát hiện sớm
