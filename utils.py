import pymongo
import os
import re
import datetime
from pandas import read_excel

def connect_to_mongo(uri='mongodb://127.0.0.1:27017/', db_name='IP-Monitoring', collection_name='datas'):
    """
    Connects to MongoDB and returns the collection object.
    """
    client = pymongo.MongoClient(uri)
    db = client[db_name]
    return db[collection_name]

def read_ips_from_excel(file_path, sheet_name):
    """
    Reads IP addresses from the given Excel file.

    Parameters:
    - file_path: Path to the Excel file containing IP addresses.
    - sheet_name: Name of the sheet within the Excel file.
    """
    df = read_excel(file_path, sheet_name=sheet_name)
    return df['ip'].values.tolist()

def ping_ip(ip):
    """
    Pings an IP address and returns the status and default gateway.
    """
    os.system(f"copy /y NUL file3.txt & ping {ip} > file3.txt")
    os.system(f"copy /y NUL file4.txt & tracert -h 15 {ip} > file4.txt")

    with open("file3.txt", 'r') as ping_file:
        ping_output = ping_file.readlines()

    with open("file4.txt", 'r') as trace_file:
        trace_output = trace_file.readlines()

    status = "Working"
    default_gateway = None
    route = []

    for line in ping_output:
        if re.search("Destination Host Unreachable|Request timed out", line):
            status = "Not Working"

    for line in trace_output:
        if re.search("^  1", line):
            default_gateway = ",".join(set(re.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", line)))
            break
        if re.search("Request timed out", line):
            route.append("Unreachable")
            break
        route.append(",".join(set(re.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", line))))

    return status, default_gateway, route

def process_ips(ips, mongo_collection):
    """
    Processes a list of IPs and stores their details in MongoDB.

    Parameters:
    - ips: List of IP addresses to process.
    - mongo_collection: MongoDB collection object to store IP details.
    """
    results = []
    for index, ip in enumerate(ips):
        status, gateway, route = ping_ip(ip)
        timestamp = datetime.datetime.now().strftime("%c")
        data = [index + 1, ip, status, gateway, route, timestamp]

        # Store in MongoDB
        document = {str(index + 1): data}
        mongo_collection.insert_one(document)
        
        results.append(data)
    return results
