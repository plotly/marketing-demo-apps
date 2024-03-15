import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import dash_design_kit as ddk

import json
import os
import pandas as pd

from app import app, snap, dash_snapshots

from datetime import datetime


### Generate Snapshot Archive Table
def create_archive_table():
    t = snap.ArchiveTable(
        # built-in snapshot metadata key name, the IDs of these columns correspond to the keys of your metadata.
        columns=[
            {"id": dash_snapshots.constants.KEYS["snapshot_id"], "name": "Snapshot"},
            {"id": dash_snapshots.constants.KEYS["pdf"], "name": "PDF"},
            {"id": "snapshot_name", "name": "Snapshot Name"},
            {
                "id": dash_snapshots.constants.KEYS["task_create_time"],
                "name": "Created Time",
            },
            {
                "id": dash_snapshots.constants.KEYS["task_finish_time"],
                "name": "Finish Time",
            },
        ]
    )
    return t


def layout():
    layout = [
        ddk.Block(
            style={"height": "calc(100vh - 60px)"},
            children=ddk.Card(children=[create_archive_table()]),
        ),
    ]
    return layout
