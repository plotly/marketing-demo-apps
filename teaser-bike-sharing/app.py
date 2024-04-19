import dash, os
from dash import Dash, dcc
import dash_design_kit as ddk
import dash_snapshots
from assets.settings.theme import theme
from utils.components import header

app = Dash(__name__, title="Bike-sharing", update_title=None, use_pages=True)

os.environ["REDIS_URL"] = os.environ.get("REDIS_URL", "redis://127.0.0.1:6379")

server = app.server

from snap import snap

celery_instance = snap.celery_instance


app.layout = ddk.App(
    [
        header("Bike-sharing", app),
        dcc.Location(id="url"),
        dash.page_container,
    ],
    theme=theme["dark"],
    show_editor=True,
)


if __name__ == "__main__":
    app.run_server(debug=True)
