"""
This file contains implementation of some needed utility funtions.
"""

import os
import re
import urllib.request
import xml.etree.ElementTree as ET
import zipfile
import glob
import pandas as pd

data_dir = os.path.join(os.path.split(__file__)[0], "..", "data")
dataset_dir = os.path.join(data_dir, "trip_histories")


def download_trips_dataset(force_download=False):
    """Downloads Citi Bike Trip Histories dataset."""
    if not os.path.isdir(data_dir):
            os.mkdir(data_dir)

    if os.path.isdir(dataset_dir) and not force_download:
        print("Dataset trip_histories already exists. Skipping download.")
        return

    if not os.path.isdir(dataset_dir):
        os.mkdir(dataset_dir)

    base_url = "https://s3.amazonaws.com/tripdata/"
    zip_file_name_pattern = "\d+-citibike-tripdata.zip"
    root = ET.parse(urllib.request.build_opener().open(base_url)).getroot()
    for child in root:
        if child.tag.endswith("Contents") and len(child) > 0:
            zip_file_name = child[0].text
            if re.match(zip_file_name_pattern, zip_file_name):
                print("Downloading %s..." % zip_file_name)
                zip_file_url = base_url + zip_file_name
                zip_file_path = os.path.join(dataset_dir, zip_file_name)
                urllib.request.urlretrieve(zip_file_url, zip_file_path)
                print("Extracting %s..." % zip_file_name)
                base_file_path = os.path.splitext(zip_file_path)[-2]
                with zipfile.ZipFile(zip_file_path) as zf:
                    for csv_file in zf.namelist():
                        csv_file_path = os.path.join(dataset_dir, csv_file)
                        zf.extract(csv_file, dataset_dir)
                        os.rename(csv_file_path, "%s.csv" % base_file_path)
                os.remove(zip_file_path)


def load_trips_dataframe():
    """Loads Citi Bike Trips Histories dataset into Pandas' dataframe"""
    trip_histories_pkl = os.path.join(data_dir, "trips_history.pkl")
    if os.path.isfile(trip_histories_pkl):
        print("trip_histories.pkl already exists. Skipping load.")
    else:
        dataframes = []
        all_files = glob.glob(dataset_dir + "/*.csv")
        for file in all_files:
            print("Loading {}...".format(file))
            dataframes.append(pd.read_csv(file, usecols=["starttime", "stoptime", "start station id", "end station id", "bikeid"], parse_dates=["starttime"]))
        print("Concatenating all loaded files...")
        pd.concat(dataframes).to_pickle(trip_histories_pkl)
    print("Pickling result...")
    return pd.read_pickle(trip_histories_pkl)
