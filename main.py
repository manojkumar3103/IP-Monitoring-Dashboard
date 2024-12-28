import os
import re
import datetime
from flask import Flask, render_template
from pandas import read_excel
import pymongo

# MongoDB setup
MONGO_URI = 'mongodb://127.0.0.1:27017/'
DB_NAME = 'IP-Monitoring'
COLLECTION_NAME = 'datas'

def connect_to_mongo():
    """Connects to MongoDB and returns the collection."""
    client = pymongo.MongoClient(MONGO_URI)
    return client[DB_NAME][COLLECTION_NAME]

def process_ip(ip):
    """Ping and traceroute for the given IP, returning status and route."""
    os.system(f"copy /y NUL file3.txt & ping {ip} > file3.txt")
    os.system(f"copy /y NUL file4.txt & tracert -h 15 {ip} > file4.txt")

    # Read ping output
    with open("file3.txt", 'r') as file:
        ping_output = file.readlines()

    # Determine status
    status = "Working"
    for line in ping_output:
        if "Destination Host Unreachable" in line or "Request timed out" in line:
            status = "Not Working"
            break

    # Read traceroute output
    with open("file4.txt", 'r') as file:
        tracert_output = file.readlines()

    route = []
    for line in tracert_output:
        if re.search("^  [1-9]", line):
            ip_match = re.findall(r"[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+", line)
            if ip_match:
                route.append(ip_match[0])
        elif "Request timed out" in line:
            route.append("Unreachable")
            break

    return status, route

def process_ips(ips):
    """Process a list of IPs and return results."""
    results = []
    for idx, ip in enumerate(ips):
        status, route = process_ip(ip)
        timestamp = datetime.datetime.now().strftime("%c")
        results.append([idx + 1, ip, status, route, timestamp])
    return results

def save_to_mongo(collection, data):
    """Save the data to MongoDB collection."""
    for idx, entry in enumerate(data, start=1):
        collection.insert_one({str(idx): entry})

# Flask app setup
app = Flask(__name__)

@app.route("/")
def dashboard():
    """Render the dashboard with data."""
    collection = connect_to_mongo()
    data = list(collection.find({}, {"_id": 0}))
    return render_template("dashboard.html", data=data)

if __name__ == '__main__':
    # Load IPs from Excel
    FILENAME = 'data/ip6.xlsx'
    SHEET_NAME = 'Sheet1'
    df = read_excel(FILENAME, sheet_name=SHEET_NAME)
    ips = df['ip'].tolist()

    # Process IPs and save results to MongoDB
    collection = connect_to_mongo()
    results = process_ips(ips)
    save_to_mongo(collection, results)

    # Run the Flask app
    app.run(debug=True)
