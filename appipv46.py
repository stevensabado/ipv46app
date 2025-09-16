from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Your existing API functions adapted for Flask app:

def get_public_ip():
    try:
        response = requests.get("https://api.ipify.org?format=json")
        response.raise_for_status()
        return response.json().get("ip")
    except requests.RequestException:
        return None

def get_isp_info(ip):
    url = "https://seo-api2.p.rapidapi.com/isp-checker"
    headers = {
        "x-rapidapi-key": "dc109e3e7fmsh0833d65ca28256dp152bbejsna0d2643850b4",
        "x-rapidapi-host": "seo-api2.p.rapidapi.com"
    }
    params = {"ip": ip}
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        return None

def get_geo_info(ip):
    url = "https://seo-api2.p.rapidapi.com/ip-geolocation-checker"
    headers = {
        "x-rapidapi-key": "dc109e3e7fmsh0833d65ca28256dp152bbejsna0d2643850b4",
        "x-rapidapi-host": "seo-api2.p.rapidapi.com"
    }
    params = {"ip": ip}
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    ip = None
    isp_data = None
    geo_data = None
    error = None

    if request.method == 'POST':
        ip = request.form.get('ip')
        if not ip:
            ip = get_public_ip()
        if not ip:
            error = "Unable to determine IP address."
        else:
            isp_data = get_isp_info(ip)
            geo_data = get_geo_info(ip)
            if not isp_data or not geo_data:
                error = "Error fetching data from API."

    return render_template('index.html', ip=ip, isp=isp_data, geo=geo_data, error=error)

if __name__ == "__main__":
    app.run(debug=True)
