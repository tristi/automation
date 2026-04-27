import time
import requests
import pandas as pd

INPUT_FILE = "serial_numbers.xlsx"
OUTPUT_FILE = "hasil_check_serial.xlsx"

SERIAL_COLUMN = "serial_number"
BRAND_COLUMN = "brand"  # isi: HP atau Lenovo

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json, text/plain, */*",
}


def check_hp(serial):
    url = "https://support.hp.com/wcc-services/searchresult/id-en"

    params = {
        "q": serial,
        "context": "pdp",
        "navigation": "false",
        "authState": "anonymous",
        "template": "WarrantyLanding",
    }

    try:
        r = requests.get(url, params=params, headers=HEADERS, timeout=30)

        if r.status_code != 200:
            return {
                "status": "ERROR",
                "product_name": "",
                "product_number": "",
                "message": f"HTTP {r.status_code}",
            }

        data = r.json()

        verify = data.get("data", {}).get("verifyResponse", {})
        code = verify.get("code")
        message = verify.get("message", "")
        product = verify.get("data", {})

        if code == 200 and product.get("serialNumber"):
            return {
                "status": "VALID",
                "product_name": product.get("productName", ""),
                "product_number": product.get("productNumber", ""),
                "message": message,
            }

        if code == 204:
            return {
                "status": "NOT FOUND",
                "product_name": "",
                "product_number": "",
                "message": message,
            }

        return {
            "status": "UNKNOWN",
            "product_name": "",
            "product_number": "",
            "message": message or str(verify),
        }

    except Exception as e:
        return {
            "status": "ERROR",
            "product_name": "",
            "product_number": "",
            "message": str(e),
        }


def check_lenovo(serial):
    url = "https://pcsupport.lenovo.com/id/en/api/v4/mse/getproducts"

    params = {
        "productId": serial
    }

    try:
        r = requests.get(url, params=params, headers=HEADERS, timeout=30)

        if r.status_code != 200:
            return {
                "status": "ERROR",
                "product_name": "",
                "product_number": "",
                "message": f"HTTP {r.status_code}",
            }

        data = r.json()

        if isinstance(data, list) and len(data) > 0:
            product = data[0]

            return {
                "status": "VALID",
                "product_name": product.get("Name", ""),
                "product_number": product.get("Id", ""),
                "message": "Product Found",
            }

        return {
            "status": "NOT FOUND",
            "product_name": "",
            "product_number": "",
            "message": "Device Not Found",
        }

    except Exception as e:
        return {
            "status": "ERROR",
            "product_name": "",
            "product_number": "",
            "message": str(e),
        }


def check_serial(brand, serial):
    brand = str(brand).strip().lower()

    if brand == "hp":
        return check_hp(serial)

    if brand == "lenovo":
        return check_lenovo(serial)

    return {
        "status": "UNKNOWN BRAND",
        "product_name": "",
        "product_number": "",
        "message": f"Brand tidak dikenali: {brand}",
    }


def main():
    df = pd.read_excel(INPUT_FILE)

    if SERIAL_COLUMN not in df.columns:
        print(f"Kolom '{SERIAL_COLUMN}' tidak ditemukan.")
        return

    if BRAND_COLUMN not in df.columns:
        print(f"Kolom '{BRAND_COLUMN}' tidak ditemukan.")
        return

    statuses = []
    product_names = []
    product_numbers = []
    messages = []

    for index, row in df.iterrows():
        serial = str(row[SERIAL_COLUMN]).strip()
        brand = str(row[BRAND_COLUMN]).strip()

        print(f"Checking {brand} - {serial}")

        result = check_serial(brand, serial)

        statuses.append(result["status"])
        product_names.append(result["product_name"])
        product_numbers.append(result["product_number"])
        messages.append(result["message"])

        time.sleep(1)

    df["status"] = statuses
    df["product_name"] = product_names
    df["product_number_or_id"] = product_numbers
    df["message"] = messages

    df.to_excel(OUTPUT_FILE, index=False)

    print(f"Selesai. Hasil disimpan ke {OUTPUT_FILE}")


if __name__ == "__main__":
    main()