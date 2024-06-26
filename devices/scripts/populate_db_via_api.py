import argparse
import csv
import logging
from pprint import pprint, pformat

import httpx
import openpyxl

from django.utils.text import slugify


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Populate database via API")
    parser.add_argument("--api-url", type=str, help="API base URL", required=True)
    parser.add_argument("--api-token", type=str, help="API token", required=True)
    parser.add_argument("--django-user", type=str, help="Owner of devices", required=True)
    # Create mutually exclusive group for csv and excel files
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--csv-file", type=str, help="Data file")
    group.add_argument("--excel-file", type=str, help="Excel data file")
    group.add_argument("--uirasmeta", action="store_true", help="Use Uirasmeta data")
    # add argument to choose which sheets will be used
    parser.add_argument("--sheets", nargs="+", type=str, help="Sheets to use in Excel file")
    parser.add_argument("--log", choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], default="ERROR")
    args = parser.parse_args()
    logging.basicConfig(level=getattr(logging, args.log))
    args.api_url = args.api_url.rstrip("/")
    return args


args = parse_args()

headers = {
    "Authorization": f"Token {args.api_token}",
    "User-Agent": "iot-device-upload/0.0.1",
    "Accept": "application/json",
}


def get_device_type():
    """Check if one device type exists, if not create it and return URL."""
    url = "{}/device-types/".format(args.api_url)
    r = httpx.get(url, headers=headers)
    if r.status_code != 200:
        logging.critical(f"Failed to get device types from {url}: {r.status_code} {r.text}")
        exit(1)
    r_data = r.json()
    if r_data["count"] > 0:
        return r_data["results"][0]["url"]
    else:
        device_type_data = {
            "name": "Placeholder",
            "slug": "placeholder",
            "description": "Placeholder device type",
        }
        r = httpx.post(url, headers=headers, json=device_type_data)
        if r.status_code != 201:
            logging.critical(f"Failed to create device type: {r.status_code} {r.text}")
            exit(1)
        r_data = r.json()
        return r_data["url"]


def post_device_data(args: argparse.Namespace, device_type: str, data: dict):
    url = "{}/devices/".format(args.api_url)
    device_data = {
        "device_id": data["device_id"],
        "name": data["name"],
        "owner": f"{args.api_url}/users/{args.django_user}/",
        "type": device_type,
        "parser_module": data["parser_module"],
        "logs": [],
        "images": [],
    }
    logging.info(f"Posting device data to {url}: {device_data}")
    # Check first if device exists
    device_url = f"{url}{data['device_id']}/"
    r = httpx.get(device_url, headers=headers)
    if r.status_code == 200:
        logging.debug("Device exists, updating...")
        r = httpx.put(device_url, headers=headers, json=device_data)
    else:  # POST new device
        logging.debug("Device does not exist, creating...")
        r = httpx.post(url, headers=headers, json=device_data)
    logging.info(r.status_code, r.text)


def parse_csv(args: argparse.Namespace):
    # Get placeholder device type URL
    device_type = get_device_type()
    # Parse CSV file using csv.DictReader
    with open(args.csv_file, newline="") as csvfile:
        lines = csv.DictReader(csvfile)
        for line in lines:
            logging.debug(line)
            post_device_data(args, device_type, line)


def read_excel(filename: str):
    """Read Excel file and return it."""
    wb = openpyxl.load_workbook(filename)
    return wb


def read_excel_sheet(wb: openpyxl.Workbook, sheet_name: str) -> list:
    """Read Excel sheet and return it as a list of dicts."""
    sheet = wb[sheet_name]
    data_list = []

    for row in sheet.iter_rows(min_row=1, values_only=True):
        if any(value is not None for value in row):  # Skip empty rows
            data_list.append(row)

    column_names = data_list.pop(0)
    # create list of dicts
    data_list = [dict(zip(column_names, row)) for row in data_list]
    # remove items with None values
    data_list = [{k: v for k, v in d.items() if v is not None} for d in data_list]
    return data_list


def post_data(args: argparse.Namespace, endpoint: str, lookup_value: str, data: dict, patch: bool = False):
    url = "{}/{}/".format(args.api_url, endpoint)
    object_url = "{}{}/".format(url, lookup_value)
    r = httpx.get(object_url, headers=headers)
    logging.debug(f"{object_url}: {r.status_code} {r.text[:100]}")
    if r.status_code == 200:
        if patch:
            logging.debug(f"{lookup_value} exists, patching...")
            r = httpx.patch(object_url, headers=headers, json=data)
        else:
            logging.debug(f"{lookup_value} exists, updating...")
            r = httpx.put(object_url, headers=headers, json=data)
            # pretty_data = pformat(data)
            # logging.debug(f"{r.status_code} {r.text} {pretty_data}")
    else:  # POST new device
        logging.debug(f"{lookup_value} does not exist, creating...")
        r = httpx.post(url, headers=headers, json=data)
        if r.status_code >= 400:
            pretty_data = pformat(data)
            logging.error(f"{r.status_code} {r.text} {pretty_data}")
            exit(1)
    logging.debug(f"{r.status_code} {r.text}")
    return r.json()


def parse_excel(args: argparse.Namespace):
    wb = read_excel(args.excel_file)

    if args.sheets is None or "DeviceType" in args.sheets:
        placeholder = {"name": "Placeholder", "slug": "placeholder", "description": "Placeholder device type"}
        post_data(args, "device-types", "placeholder", placeholder)
        device_types = read_excel_sheet(wb, "DeviceType")
        for device_type in device_types:
            post_data(args, "device-types", device_type["slug"], device_type)

    if args.sheets is None or "Organization" in args.sheets:
        organizations = read_excel_sheet(wb, "Organization")
        for organization in organizations:
            post_data(args, "organizations", organization["slug"], organization)

    if args.sheets is None or "Device" in args.sheets:
        devices = read_excel_sheet(wb, "Device")
        for device in devices:
            device["owner"] = f"{args.api_url}/users/{args.django_user}/"
            device["type"] = "{}/device-types/{}/".format(args.api_url, device.get("type", "placeholder"))
            # TODO: make these fields optional
            device["logs"] = []
            device["images"] = []
            try:
                post_data(args, "devices", device["device_id"], device)
            except Exception as e:
                print(e)
                pprint(device)
                exit(1)
    wb.close()


def parse_uirasmeta(args: argparse.Namespace):
    from uirasmeta import META

    for device_id, data in META.items():
        location_slug = slugify(data["name"])[:50]
        print(device_id, location_slug, data)
        # POST or PUT locations
        location_data = {
            "slug": location_slug,
            "name": data["name"],
            "locality": data.get("location", ""),
            "district": data.get("district", ""),
            "lat": data["lat"],
            "lon": data["lon"],
            "properties": {},
        }
        for key in ["servicemap_url", "site_url", "site_title"]:
            if data.get(key):
                location_data["properties"][key] = data[key]
        print(location_data)
        res_data = post_data(args, "locations", location_slug, location_data)
        location_url = res_data["url"]
        print(res_data)
        # PATCH devices
        device_data = {
            "properties": data.get("properties", {}),
            "current_location": location_url,
        }
        print(device_data)
        # exit()
        for key in ["servicemap_url", "site_url", "site_title"]:
            if data.get(key):
                device_data["properties"][key] = data[key]
        post_data(args, "devices", device_id, device_data, patch=True)
        # exit()


def main():
    # args = parse_args()
    if args.csv_file:
        parse_csv(args)
    elif args.excel_file:
        parse_excel(args)
    elif args.uirasmeta:
        parse_uirasmeta(args)


if __name__ == "__main__":
    main()
