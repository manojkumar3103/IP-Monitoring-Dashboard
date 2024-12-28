# Live Dashboard for IP Monitoring Using Python and Flask

## Overview
This project provides a dynamic live dashboard for monitoring the status of IP addresses. It allows users to:
- Check the working status of multiple IPs.
- View traceroute details.
- Store historical data in MongoDB for analysis.

The dashboard is built using Python, Flask, and MongoDB. It uses Jinja2 templates for rendering data dynamically in the browser.

## Features
- **IP Status Check:** Automatically checks if an IP is reachable using `ping`.
- **Traceroute Analysis:** Provides detailed routing information for each IP.
- **Data Storage:** Stores results in a MongoDB collection.
- **Web Interface:** Displays results in a user-friendly dashboard.

## Prerequisites
- Python 3.7+
- MongoDB installed and running on `localhost:27017`
- Required Python packages (specified in `requirements.txt`)

## Installation

1. Clone the repository:
   ```bash
   git clone manojkumar3103/IP-Monitoring-Dashboard
   cd IP-Monitoring-Dashboard
   ```

2. Set up a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Place your input file `ip6.xlsx` in the `data/` folder.

5. Start MongoDB:
   ```bash
   mongod
   ```

## Running the Application

1. Start the Flask server:
   ```bash
   python app/main.py
   ```

2. Access the dashboard in your browser at:
   ```
   http://127.0.0.1:5000/
   ```

## File Structure
```
.
├── app/
│   ├── templates/
│   │   └── dashboard.html    # HTML template for rendering the dashboard
│   ├── static/               # (Optional) For CSS/JS files
│   ├── main.py               # Main application logic
│   ├── utils.py              # Utility functions (e.g., file handling, database interaction)
├── README.md
├── requirements.txt          # Python dependencies
```

## Example Input
**ip6.xlsx:**
| ip            |
|---------------|
| 192.168.1.1   |
| 8.8.8.8       |
| 172.16.0.1    |

## Example Output
**Dashboard Columns:**
- **Index**
- **IP Address**
- **Status** (Working/Not Working)
- **Route** (Traceroute hops or Unreachable)
- **Timestamp** (Last updated)

## Contributing
Contributions are welcome! Please fork the repository and create a pull request for any improvements.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

## Acknowledgments
Special thanks to Bannari Amman Institute of Technology for supporting this project.
