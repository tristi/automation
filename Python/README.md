# Laptop Serial Number Validation Automation

## Overview

Automation untuk validasi serial number laptop **HP** dan **Lenovo** menggunakan Python.

Project ini membantu proses monitoring asset IT multi cabang, terutama saat Head IT Regional menerima laporan serial number dari cabang dan perlu melakukan validasi massal ke website resmi vendor.

---

## Version

| Version | Output | Status |
|---|---|---|
| V1 | Export hasil validasi ke Excel | Ready |
| V2 | Insert hasil validasi ke Database | On Progress |

---

## Supported Brand

| Brand | Validation Source |
|---|---|
| HP | HP Support Warranty API |
| Lenovo | Lenovo Support API |

---

## Input File

File input menggunakan format Excel:

`serial_numbers.xlsx`

### Required Columns

| Column | Description |
|---|---|
| brand | Brand laptop (HP / Lenovo) |
| serial_number | Serial number perangkat |

### Example

| cabang | brand | serial_number | qty | status_asset |
|---|---|---|---|---|
| Surabaya | HP | 5CD6064W7F | 1 | New Unit |
| Jakarta | Lenovo | PF55N907 | 1 | Existing |

---

## Output File (Version 1)

File hasil validasi:

`hasil_check_serial.xlsx`

### Example Output

| cabang | brand | serial_number | status | product_name | message |
|---|---|---|---|---|---|
| Surabaya | HP | 5CD6064W7F | VALID | HP ProBook 4 G1i | Success |
| Jakarta | Lenovo | PF55N907 | VALID | E14 Gen 6 ThinkPad | Product Found |
| Bandung | HP | 5CD7788ABC | NOT FOUND | - | Device Not Found |

---

## Validation Status

| Status | Description |
|---|---|
| VALID | Serial number ditemukan |
| NOT FOUND | Serial number tidak ditemukan |
| ERROR | Request gagal |
| UNKNOWN | Response tidak sesuai |
| UNKNOWN BRAND | Brand tidak didukung |

---

## Installation

```bash
pip install pandas openpyxl requests
```

---

## Run Script

```bash
python check_serial.py
```

---

## Version 2 Roadmap

| Feature | Status |
|---|---|
| Insert ke Database | On Progress |
| Support MySQL / PostgreSQL | Planned |
| Validation Timestamp | Planned |
| Raw API Response Storage | Planned |
| Dashboard Monitoring | Planned |

---

## Benefits

| Benefit |
|---|
| Mempercepat validasi serial number |
| Mengurangi human error |
| Mempermudah warranty tracking |
| Mendukung audit asset |
| Meningkatkan akurasi asset register |

---

## Notes

Gunakan delay request untuk menghindari rate limit:

```python
time.sleep(1)
```

