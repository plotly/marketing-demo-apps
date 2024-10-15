import time

import dash
import dash_bootstrap_components as dbc

## Diskcache
import diskcache
from dash import dcc, html
from dash.dependencies import Input, Output
from dash.long_callback import DiskcacheLongCallbackManager

cache = diskcache.Cache("./cache")
long_callback_manager = DiskcacheLongCallbackManager(cache)

app = dash.Dash(__name__, long_callback_manager=long_callback_manager)
app.layout = html.Div(
    [
        dbc.Button("Start", id="start_button"),
        dcc.Markdown(id="progress_output"),
    ]
)


@app.callback(
    output=Output("progress_output", "children"),
    inputs=[Input("start_button", "n_clicks")],
    progress=Output("progress_output", "children"),
    progress_default="",
    background=True,
    interval=100,
)
def read_message(set_progress, n_clicks):
    if n_clicks is None:
        raise dash.exceptions.PreventUpdate

    state = ""

    for chunk in read_chunk():
        # append the chunk
        state += chunk
        # Update the progress component
        set_progress(state)

    # Return the final result
    return state


def read_chunk():
    reply = """
    An h1 header
    ============

    Paragraphs are separated by a blank line.

    2nd paragraph. *Italic*, **bold**, and `monospace`. Itemized lists
    look like:

    * this one
    * that one
    * the other one

    Note that --- not considering the asterisk --- the actual text
    content starts at 4-columns in.

    > Block quotes are
    > written like so.
    >
    > They can span multiple paragraphs,
    > if you like.

    Use 3 dashes for an em-dash. Use 2 dashes for ranges (ex., "it's all
    in chapters 12--14"). Three dots ... will be converted to an ellipsis.
    Unicode is supported. ☺
    """
    chunks = [word + " " for word in reply.split(" ")]
    for chunk in chunks:
        # Simulate some work
        time.sleep(0.02)
        yield chunk


if __name__ == "__main__":
    app.run_server(debug=True)
