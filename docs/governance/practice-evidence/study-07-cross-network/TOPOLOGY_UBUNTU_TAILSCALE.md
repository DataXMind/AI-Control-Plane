# Study 07 — Topology: Ubuntu workstation + Windows laptop (mạng ngoài)

**Document ID:** ACP-GOV-PRACTICE-STUDY-07-TOPO-UBUNTU-TS  
**Operator topology (planned)**

| Vai trò | Thiết bị | Mạng vật lý | Tailscale (tailnet) |
|---------|----------|-------------|---------------------|
| **Máy A — API** | Ubuntu workstation (hoặc `ubuntu-vps`) | LAN nhà / datacenter | `100.94.21.33` (ví dụ) |
| **Máy B — Client** | Laptop Windows (WSL) | **Hotspot / Wi-Fi ngoài** — không `192.168.1.x` | `100.102.105.47` (msi) |
| Witness (optional) | Mac Mini M2 | LAN nhà `192.168.1.99` | `100.72.15.27` |

```text
     [ Internet / 4G hotspot ]
              │
    ┌─────────┴─────────┐
    │  LAPTOP (ngoài)   │──── Tailscale 100.102.x.x ────┐
    │  WSL client only  │                                  │
    └───────────────────┘                                  ▼
                                              ┌──────────────────────┐
     [ LAN nhà 192.168.1.0/24 ]              │  Tailscale tailnet    │
              │                                │  (encrypted overlay)  │
    ┌─────────┴─────────┐                      └──────────┬───────────┘
    │ Ubuntu API :8000  │◄─────────────────────────────────┘
    │ LAN + TS IP       │
    └─────────┬─────────┘
              │
    ┌─────────┴─────────┐
    │ Mac (witness)     │  LAN → Ubuntu OK; so sánh với Laptop ngoài
    └───────────────────┘
```

---

## Vì sao cần Study 07 sau Study 06?

| Study | Đường mạng | Chứng minh |
|-------|------------|------------|
| **06** | Cùng LAN `192.168.1.x` (+ portproxy WSL) | 2 host cùng subnet; bidirectional |
| **07** | **Khác** LAN; chỉ `100.x` Tailscale | Operator remote / staging thật |

Study 06 **không** chứng minh laptop ở quán cafe vẫn gọi được API tại nhà. Study 07 bổ sung đúng kịch bản đó.

---

## Thiết lập từng bước

### Bước 1 — Ubuntu (máy cố định)

1. Cài Tailscale, join cùng tailnet với `msi` và `dataxminds-mac-mini`.
2. Clone repo, `pip install -e ".[dev]"`.
3. `uvicorn --host 0.0.0.0 --port 8000` + fixture config.
4. Mở firewall port 8000 (ưu tiên interface `tailscale0`).
5. Ghi `UBUNTU_TS_IP` và `UBUNTU_LAN_IP`.

### Bước 2 — Chuẩn bị Laptop “mạng ngoài”

1. Hoàn tất Study 06 trên LAN (đã PASS).
2. Khi chạy Study 07: **tắt Wi-Fi nhà**, bật hotspot.
3. `tailscale status` — phải thấy Ubuntu **online**.
4. Chạy negative test: `ping UBUNTU_LAN_IP` → fail.

### Bước 3 — Client drills qua Tailscale

```bash
export ACP_API_URL=http://<UBUNTU_TS_IP>:8000
# full suite: health, gov status, policy, assign
```

### Bước 4 — Optional PB-9 soak

```bash
bash scripts/soak_staging.sh --log /tmp/acp-soak-remote.log
```

---

## Lựa chọn Ubuntu host

| Host | Ưu | Nhược |
|------|-----|-------|
| **Workstation Ubuntu tại nhà** | Giống staging on-prem; latency thấp trong LAN | Cần máy luôn bật |
| **`ubuntu-vps` cloud** | Luôn online; không phụ thuộc điện nhà | Thêm hardening SSH/firewall |

Cả hai đều hợp lệ miễn Tailscale IP ổn định trong tailnet.

---

## Không dùng / tránh

- **Không** dùng LAN IP trên Laptop ngoài — sẽ fail by design.
- **Không** copy `.venv` qua Tailscale — mỗi máy `pip install` riêng.
- **Không** bắt buộc portproxy WSL trên Study 07 (Laptop = client).
- **Không** nhầm Study 07 với đóng PB-9 — soak calendar 14 ngày vẫn riêng.

---

## Liên hệ Study 06 follow-ups

| Follow-up 06 | Study 07 |
|--------------|----------|
| Drill Tailscale `100.x` | **Core** của Study 07 |
| Remote `soak_staging.sh` (6-5) | Drill **7-5** |
| Round B full policy + assign | Có thể lặp trên Ubuntu↔Laptop TS nếu muốn đủ 2 chiều |

---

## Evidence (sau khi chạy)

Điền [`RESULTS.md`](RESULTS.md) với:

- Screenshot/log negative LAN test
- `ACP_API_URL` dùng Tailscale IP
- Ubuntu access log với IP `100.x` client
- (Optional) soak log excerpt
