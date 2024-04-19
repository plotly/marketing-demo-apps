import dash
from dash import html
from snap import snap

dash.register_page(
    __name__,
    title="Report",
    path_template="/snapshot-<snapshot_id>",
)


def layout(snapshot_id=""):
    snapshot_url = "snapshot-" + snapshot_id
    snapshot_content = snap.snapshot_get(snapshot_url) if snapshot_id else ""
    return html.Div(snapshot_content)
