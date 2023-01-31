"""
Python script that uses the USGS.gov API to retrieve the SC earthquake swarm data.

Part one of this script, get_eq_events(), retrieves earthquake events and their data.
Part two, get_dyfi_urls(), uses the event detail urls to retrieve each event's DYFI, (cdi_zip.txt file) url.
Part three, get_dyfi_zip_data(), retrieves the cdi_zip.txt file data for each event and saves it as a .csv file,
            cdi_zip.event_id.
if the -f cli argument is given, then the earthquake events retrieved in step one are saved to a geojson file for use in
the data app.

usgs_api.py script contains the following functions:

    get_eq_events() - returns a pandas dataframe containing event ids and event detail urls.
    get_dyfi_urls() - returns a pandas dataframe containing the event ids and the dyfi urls.
    get_dyfi_zip_data() - Retrieves the cdi_zip.txt file data for each event and saves to file.
"""

__version__ = "1.0.0"

from io import BytesIO
import json
import argparse
from pathlib import Path
from datetime import datetime, date, timedelta
import time
import requests
import pandas as pd
from requests.adapters import HTTPAdapter
from urllib3 import Retry
from concurrent import futures
from concurrent.futures import ThreadPoolExecutor

DATA_DIR = r"./data/"
VERBOSE_MODE = False
EVENTS_FILE = False


def create_session():  # pylint: disable='missing-function-docstring'
    retry_strategy = Retry(total=3,
                           backoff_factor=1,
                           status_forcelist=[429, 500, 502, 503, 504],
                           allowed_methods=["HEAD", "GET", "OPTIONS"])
    adapter = HTTPAdapter(max_retries=retry_strategy)
    http = requests.session()
    http.mount("https://", adapter)
    return http


def close_http_session(http):  # pylint: disable='missing-function-docstring'
    http.close()


def get_url(xhttp, url):
    return xhttp.get(url, timeout=(3.05, 27))


def get_eq_events(http):
    """ get_eq_events() Retrieve earthquake events from USGS.gov.

    get_eq_events() function retrieves earthquake events and their event data
    from the USGS.gov website using the provided api. Returns a dataframe of
    event ids and detail urls. If the -f command-line argument is given, then
    the event data is saved to a file.

    Parameters
    ----------
    http : session
        A request session object for context management

    Returns
    -------
    eq_events_df : pandas dataframe
        A pandas dataframe containing two columns:  event ids and event detail urls.
    """
    if VERBOSE_MODE:
        print("Function:  get_eq_events()")
        print("Running API query...")
    url = "https://earthquake.usgs.gov/fdsnws/event/1/query.geojson"
    querystring = {"starttime": "2021-12-01 00:00:00",
                   "endtime": date.today().isoformat() + " 23:59:59",
                   "maxlatitude": "35.261",
                   "minlatitude": "31.977",
                   "maxlongitude": "-77.86",
                   "minlongitude": "-83.485",
                   "minmagnitude": "1",
                   "maxmagnitude": "10",
                   "orderby": "time",
                   "producttype": "dyfi",
                   "format": "geojson"}
#     response = requests.request("GET", url, params=querystring, timeout=(3.05, 27))
    response = http.get(url, params=querystring, timeout=(3.05, 27))
    data = response.json()
    # Write earthquake events data to a file
    if EVENTS_FILE:
        file_pfx = datetime.now().strftime("%Y%m%d")
        filename = Path(DATA_DIR + file_pfx + r"_SC_Earthquake.geojson")  # FIXME:  Maybe make this a generic file name
#        filename = r"./data/" + file_pfx + r"_SC_Earthquake.geojson"
        if VERBOSE_MODE:
            print(f"Saving SC earthquake events data to {filename}")
        with open(filename, 'w', encoding="utf-8") as f:  # pylint: disable='invalid-name'  # noqa
            json.dump(data, f)
    if VERBOSE_MODE:
        print("Saving earthquake event ids. ")
    # Save json response to a pandas dataframe and filter the needed columns to the same dataframe.
    temp_df = pd.json_normalize(data['features'])
    eq_events_df = temp_df[['id', 'properties.detail']]
    return eq_events_df


def get_dyfi_urls(eq_id_url_df, http):
    """ get_dyfi_urls() Retrieve dyfi, cdi_zip.txt file urls.

    get_dyfi_urls() By using the detail urls in eq_id_url_df, get dyfi,
    cdi_zip.txt, file urls from each earthquake event. The event id and its
    dyfi url are saved to the eq_ids_df dataframe.

    Parameters
    ----------
    eq_id_url_df : pandas dataframe
        A pandas dataframe containing earthquake event ids and their event detail urls.
    http : session
        A request session object for context management.

    Returns
    -------
    eq_ids_df : pandas dataframe
        The dataframe containing the earthquake ids and cdi_zip.txt file urls.
    """
    start_time = time.monotonic()
    if VERBOSE_MODE:
        print("Function:  get_dyfi_urls()")
        print("Retrieving cdi_zip.txt urls.")
    dyfi_zip_urls = []
    querystring_list = list(eq_id_url_df['properties.detail'])
    with ThreadPoolExecutor(max_workers=8) as pool:
        task_list = [pool.submit(get_url, http, qry) for qry in querystring_list]
        for f in futures.as_completed(task_list):
            res_data = f.result().json()
            event_id = res_data['id']
            res_data_df = pd.DataFrame(res_data['properties']['products']['dyfi'])
            temp_df = res_data_df.loc[res_data_df['preferredWeight'] ==
                                      res_data_df['preferredWeight'].max()]
            temp_df = pd.json_normalize(temp_df['contents'])
            dyfi_zip_urls.append(dict(e_id=event_id, e_url=temp_df['cdi_zip.txt.url'][0]))
    eq_ids_df = pd.DataFrame(dyfi_zip_urls)
    end_time = time.monotonic()
    func_time = (timedelta(seconds=end_time - start_time))
    print(f"Function: get_dyfi_urls took {func_time} seconds to run.")
    return eq_ids_df


def get_dyfi_zip_data(zip_df, http):
    """ get_dyfi_zip_data() Process each dyfi zip url.

    get_dyfi_zip_data() Retrieve the cdi_zip.txt file at url for each event and
    save it to a file (cdi_zip.{eventid}).

    Parameters
    ----------
    zip_df : Pandas dataframe
        A pandas dataframe containing the event ids and the cdi_zip.txt urls.
    http : session
        A request session object for context management.

    Returns
    -------
    Nothing. Saves a cdi_zip.txt file for each earthquake event.
    """
    start_time = time.monotonic()
    if VERBOSE_MODE:
        print("Function:  get_dyfi_zip_data()")
    for idx in range(0, len(zip_df)):
        url = zip_df['e_url'][idx]
        eid = zip_df['e_id'][idx]
        if VERBOSE_MODE:
            print(f"Processing url {url}")
#        response = requests.request("GET", url, timeout=(3.05, 27))
        response = http.get(url, timeout=(3.05, 27))
        res_data = BytesIO(response.content)
        res_data_dff = pd.read_csv(res_data)
        res_data_dff.rename({'# Columns: ZIP/Location': 'ZIP/Location',
                             'No. of responses': 'Response_Count',
                             'Hypocentral distance': 'Hypocentral_Distance',
                             'Standard deviation': 'Std_Dev',
                             'State[': 'State'},
                            axis=1, inplace=True)
        res_data_dff.drop('cityid]', axis=1, inplace=True)
#        filename = data_dir + "cdi_zip" + "." + eid
        filename = Path(DATA_DIR + "cdi_zip" + "." + eid)
        if VERBOSE_MODE:
            print(f"Saving file {filename}")
        res_data_dff.to_csv(filename, index=False)
    end_time = time.monotonic()
    func_time = (timedelta(seconds=end_time - start_time))
    print(f"Function: get_dyfi_zip_data took {func_time} seconds to run.")


if __name__ == '__main__':
    """Driver function."""
    my_parser = argparse.ArgumentParser(prog='usgs_api',
                                        description='Retrieve earthquake data from USGS.gov')
    my_parser.add_argument('-f',
                           action='store_true',
                           help='Extract earthquake events to file')
    my_parser.add_argument('-v',
                           '--verbose',
                           action='store_true',
                           dest='v',
                           help='Display verbose output')
    args = my_parser.parse_args()
    if args.v:
        VERBOSE_MODE = True
    if args.f:
        EVENTS_FILE = True

    sess = create_session()
    print("Processing USGS API request - part 1")
    if VERBOSE_MODE:
        print("Retrieving earthquake events from USGS.gov. ")
    eq_event_ids = get_eq_events(sess)

    print("Processing USGS API request - part 2")
    if VERBOSE_MODE:
        print("Retrieving cdi_zip.txt urls from earthquake events. ")
    zip_urls_df = get_dyfi_urls(eq_event_ids, sess)

    print("Processing USGS API request - part 3")
    if VERBOSE_MODE:
        print("Retrieving dyfi data from each cdi_zip.txt url and saving to a file. ")
    get_dyfi_zip_data(zip_urls_df, sess)
    close_http_session(sess)
    print("Processing USGS API request - finished")
