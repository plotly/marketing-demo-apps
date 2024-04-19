import dash, dash_snapshots
from dash import html
from snap import snap

dash.register_page(__name__, title="Reports Archive", path="/reports-archive")


def layout():

    return html.Div(
        [
            snap.ArchiveTable(
                columns=[
                    # Meta data options corresponds to the column displayed in archive table.
                    {
                        "id": dash_snapshots.constants.KEYS["snapshot_id"],
                        "name": "Report View",
                    },
                    # {
                    #     "id": dash_snapshots.constants.KEYS["pdf"],
                    #     "name": "PDF",
                    # },
                    {
                        "id": "report-title",
                        "name": "Report Title",
                    },
                    {
                        "id": "report-creator",
                        "name": "Report Creator",
                    },
                    {
                        "id": dash_snapshots.constants.KEYS["created_time"],
                        "name": "Report Created Date",
                    },
                ]
            )
        ]
    )
