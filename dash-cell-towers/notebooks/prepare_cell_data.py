import dask.dataframe as dd
import pandas as pd
import pyproj
from pyproj import Transformer
import requests
import os
from dotenv import load_dotenv


# This preprocesses the cell towers dataset into an efficient set of parquet files. First register for an API key with [opencellid](https://www.opencellid.org/) and then download the `cell_towers.csv.gz` file.  Unzip it and modify the `cell_towers_path` below to the path to your `cell_towers.csv` file.  Then execute this notebook to write out a compressed parquet to the `../data` directory.
cell_towers_path = "/home/jmmease/PyDev/datasets/geo/cell_towers/cell_towers.csv"

load_dotenv()
api_key = os.getenv('API_KEY')
url = f"https://api.opencellid.org/v2/measurements.csv.gz?token={api_key}"
response = requests.get(url, stream=True)

if response.status_code == 200:
    with open('database.csv.gz', 'wb') as f:
        for chunk in response.iter_content(chunk_size=1024): 
            if chunk:
                f.write(chunk)
else:
    print(f"Failed to download file, status code: {response.status_code}")

print(chunk)

# From https://www.opencellid.org/downloads.php
# Field Descriptions: http://wiki.opencellid.org/wiki/Menu_map_view#Cells_database:
ddf = dd.read_csv(cell_towers_path)
ddf.head()

# Categorize radio
ddf['radio'] = ddf.radio.astype('category')
# Created and updated to datetime integers
ddf['created'] = dd.to_datetime(ddf.created, unit='s').astype('int')
ddf['updated'] = dd.to_datetime(ddf.updated, unit='s').astype('int')
# Filter out outliers created before 2003
ddf = ddf[dd.to_datetime(ddf.created) >= '2003']


# convert lon/lat to epsg:3857 (psuedo-mercator) so generated images
# can be overlayed on a Mercator projected map
transformer = Transformer.from_crs("epsg:4326", "epsg:3857")
def to3857(df):
    x_3857, y_3857 = transformer.transform(df.lat.values, df.lon.values)
    return df.assign(x_3857=x_3857, y_3857=y_3857)

ddf = ddf.map_partitions(to3857)

ddf.head()


# Download network info for mcc/mnc from 'https://cellidfinder.com/mcc-mnc'
html = requests.get('https://cellidfinder.com/mcc-mnc')
tables = pd.read_html(html.content)
mcc_mnc_df = pd.concat(tables).reset_index(drop=True)

# Create description column as Network, falling back to "Operator or branch" if Network not found
mcc_mnc_df['Description'] = mcc_mnc_df.Network.where(
    ~pd.isnull(mcc_mnc_df.Network), mcc_mnc_df['Operator or brand name']
)

# Drop unneeded columns
codes = mcc_mnc_df.drop(['Network', 'Operator or brand name'], axis=1)
codes.head()


# Categorize non-numeric columns
for col, dtype in codes.dtypes.items():
    if dtype == 'object':
        codes[col] = codes[col].astype('category')


# Merge mnc/mcc info with cell towers dataset
ddf_merged = ddf.merge(codes, left_on=['mcc', 'net'], right_on=['MCC', 'MNC'], how='left')
ddf_merged


# Write parquet file to ../data directory
os.makedirs('../data', exist_ok=True)
parquet_path = '../data/cell_towers.parq'
ddf_merged.to_parquet(parquet_path, compression='snappy')


# Read and display the first three rows (Transpose so can see all of the columns)
dd.read_parquet(parquet_path).head(3).T

