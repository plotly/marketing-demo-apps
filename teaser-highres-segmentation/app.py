import os

import dash_mantine_components as dmc
from dash import Dash, dcc

from callbacks.control_bar import *
from callbacks.image_viewer import *
from components.control_bar import layout as control_bar_layout
from components.image_viewer import layout as image_viewer_layout
from utils.data_utils import DEV_download_google_sample_data

DEV_download_google_sample_data()
app = Dash(__name__, update_title=None)
server = app.server


app.layout = dmc.MantineProvider(
    theme={"colorScheme": "light"},
    children=[
        control_bar_layout(),
        image_viewer_layout(),
        dcc.Store(id="current-class-selection", data="#FFA200"),
    ],
)

if __name__ == "__main__":
    app.run_server(debug=True)
