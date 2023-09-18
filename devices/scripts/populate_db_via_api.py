import httpx
import csv
import argparse

parser = argparse.ArgumentParser(description="Populate database via API")
parser.add_argument("--api-url", type=str, help="API base URL", required=True)
parser.add_argument("--api-token", type=str, help="API token", required=True)
parser.add_argument("--csv-file", type=str, help="Data file", required=True)
args = parser.parse_args()

headers = {
    "Authorization": f"Token {args.api_token}",
    "User-Agent": "iot-device-upload/0.0.1",
}


def get_device_type():
    """Check if one device type exists, if not create it and return URL."""
    url = "{}/device-types/".format(args.api_url.rstrip("/"))
    r = httpx.get(url, headers=headers)
    if r.status_code != 200:
        print("Failed to get device types")
        print(r.status_code)
        print(r.text)
        exit(1)
    r_data = r.json()
    if r_data["count"] > 0:
        return r_data["results"][0]["url"]
    else:
        device_type_data = {
            "name": "Placeholder",
            "description": "Placeholder device type",
        }
        r = httpx.post(url, headers=headers, json=device_type_data)
        r_data = r.json()
        return r_data["url"]


def post_device_data(data: dict):
    url = "{}/devices/".format(args.api_url.rstrip("/"))
    device_data = {
        "device_id": data["device_id"],
        "name": data["name"],
        "owner": "http://127.0.0.1:8000/api/v1/users/1/",
        "type": device_type,
        "parser_module": data["parser_module"],
        "maintenance_log_set": [],
        "installation_image_set": [],
    }
    # Check first if device exists
    device_url = f"{url}{data['device_id']}/"
    r = httpx.get(device_url, headers=headers)
    if r.status_code == 200:
        print("Device exists, updating...")
        r = httpx.put(device_url, headers=headers, json=device_data)
    else:  # POST new device
        print("Device does not exist, creating...")
        r = httpx.post(url, headers=headers, json=device_data)

    print(r.status_code, r.text)


# Get placeholder device type URL
device_type = get_device_type()

# Parse CSV file using csv.DictReader
with open(args.csv_file, newline="") as csvfile:
    lines = csv.DictReader(csvfile)
    for line in lines:
        print(line)
        post_device_data(line)
