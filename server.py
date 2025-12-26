from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
import webbrowser
from threading import Timer

app = Flask(__name__)
CORS(app)

API_MAP = {
    "1772007": "77.70.74.151:49655:e5L5WC:7777",
    "CTT1kQFAcep7psPnl3DBjzUd8AMKIWEX": "36.50.54.151:49643:TN4UTA:Jhza1ZF0",
    "suIqN6ncMv4HuUVmEB16284S7RP6sPxQ": "36.50.54.151:49636:xzsa111:xzsa111",
    "Nlk7RjcifmhqRFRtcsDD7a2DaxBuvm5f": "36.50.54.151:49636:xzsa111:xzsa111",
    "Gmu9FitvE7wvYFCx6KiC49SitMG5EGNb": "36.50.54.151:49223:xzsa111:xzsa111",
    "LGS3o0oxmmRpLPnDP4fdGiMASgAASjGz": "36.50.54.151:49019:xzsa111:xzsa111",
    "ZhpYGs7sj8i83isTrI05LV3pU0bBKhsg": "36.50.54.151:49454:xzsa111:xzsa111",
    "ZOvT3th4cd2ugm3n3QqdAZC8EPcqbA24": "36.50.54.151:49052:xzsa111:xzsa111",
    "DvEi5DXmaks6FERAaI7nywGUAGuS92mB": "36.50.54.151:49797:testeagle:testeagle"
}

ROTATE_API = "https://proxyandanh.com/api/v1/proxy/change-ip?apiKey="

@app.route("/check_proxy_ip")
def check_proxy_ip():
    api_key = request.args.get("apiKey")
    if api_key not in API_MAP:
        return jsonify({"success": False, "message": "API key không hợp lệ"}), 400

    proxy_str = API_MAP[api_key]
    parts = proxy_str.split(":")
    ip, port = parts[0], parts[1]
    if len(parts) >= 4:
        user, passwd = parts[2], parts[3]
        proxy_url = f"socks5://{user}:{passwd}@{ip}:{port}"
    else:
        proxy_url = f"socks5://{ip}:{port}"

    try:
        # Lấy IP gốc
        res = requests.get(
            "http://api.ipify.org?format=json",
            proxies={"http": proxy_url, "https": proxy_url},
            timeout=15
        )
        ip_goc = res.json().get("ip")

        # Gọi API check KM
        try:
            api_res = requests.get(f"https://bet.smsbet.top/add_ip.php?ip={ip_goc}", timeout=10)
            if api_res.status_code == 200 and 'success' in api_res.text:
                status_km = {"status":"success","message":"Tỉ lệ lên KM CAO"}
            else:
                status_km = {"status":"fail","message":"IP khó lên KM - vui lòng xoay IP"}
        except:
            status_km = {"status":"fail","message":"IP khó lên KM - vui lòng xoay IP"}

        return jsonify({"success": True, "proxy": proxy_str, "ip": ip_goc, "km_status": status_km})

    except requests.exceptions.RequestException as e:
        return jsonify({"success": False, "message": str(e)})

@app.route("/")
def index():
    return send_from_directory('.', 'index.html')

if __name__ == "__main__":
    Timer(1, lambda: webbrowser.open("http://127.0.0.1:5000/")).start()
    app.run(host="0.0.0.0", port=5000)
