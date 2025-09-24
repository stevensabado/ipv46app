from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Get the user's public IP
def get_public_ip():
    try:
        response = requests.get("https://api.ipify.org?format=json")
        response.raise_for_status()
        return response.json().get("ip")
    except requests.RequestException:
        return None

# Get ISP info from ip-api
def get_isp_info(ip):
    url = f"http://ip-api.com/json/{ip}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data.get("status") == "success":
            return {"isp": data.get("isp")}
        return None
    except requests.RequestException:
        return None

# Get geolocation info from ip-api
def get_geo_info(ip):
    url = f"http://ip-api.com/json/{ip}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data.get("status") == "success":
            return data
        return None
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

            # Debugging
            print("ISP Data Response:", isp_data)
            print("Geo Data Response:", geo_data)

            if not isp_data or not geo_data:
                error = "Could not retrieve full data. Please check the IP or try again later."
                isp_data = None
                geo_data = None

    return render_template('index.html', ip=ip, isp=isp_data, geo=geo_data, error=error)

if __name__ == "__main__":
    app.run(debug=True)
