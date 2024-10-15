import os
import random

import dash
import dash_design_kit as ddk
import dash_mantine_components as dmc
import pandas as pd
from dash import (
    CeleryManager,
    DiskcacheManager,
    Input,
    Output,
    State,
    callback,
    ctx,
    dcc,
    html,
)
from dash.dependencies import MATCH, Input, Output
from dash_enterprise_libraries import EnterpriseDash, chatbot_builder, ddk
from dash_iconify import DashIconify
from dotenv import load_dotenv

from constants import client
from utils.chart_utils import (
    GFSI_options,
    SP_options,
    generate_GFSI_line_chart,
    generate_herfindahl_hirschman_index,
    generate_SP_500_stocks,
)
from utils.llm_utils import (
    add_gfsi_events,
    generate_ticker_descriptions,
)

load_dotenv()
if "REDIS_URL" in os.environ:
    print("REDIS_URL found")
    from celery import Celery

    celery_app = Celery(
        __name__, broker=os.environ["REDIS_URL"], backend=os.environ["REDIS_URL"]
    )
    background_callback_manager = CeleryManager(celery_app)

else:
    import diskcache

    cache = diskcache.Cache("./cache")
    background_callback_manager = DiskcacheManager(cache)


app = EnterpriseDash(background_callback_manager=background_callback_manager)


app.setup_chatbot_builder_backend(
    url="https://api.openai.com/v1/chat/completions",
    headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}",
    },
    params={"stream": True, "model": "gpt-4-turbo-preview"},
)

app.setup_insights()


def modals():
    annotations = dmc.Modal(
        title="Structured outputs",
        size="lg",
        id={
            "type": "modal",
            "id": "annotations",
        },
        children=[
            html.Div(
                children=[
                    dcc.Markdown(
                        "To enable structured outputs, we first generate a prompt to pass to the model:"
                    ),
                    dmc.CodeHighlight(
                        code=open("snippets/annotations.py").read(),
                        language="python",
                    ),
                    dcc.Markdown(
                        "Because Dash supports the OpenAI API natively, we can run queries from within our app callbacks, and leverage structured responses to ensure consistent quality of outputs."
                    ),
                    dmc.CodeHighlight(
                        code=open("snippets/annotations_2.py").read(),
                        language="python",
                    ),
                    dcc.Markdown(
                        "We apply similar logic when querying for world or financial events, and every time the user submits a question, we send it to the model and display a unique, but structured, response."
                    ),
                ]
            ),
            dmc.Group(
                [
                    dmc.Button(
                        "Close",
                        color="red",
                        variant="outline",
                        id={
                            "type": "modal-close",
                            "id": "annotations",
                        },
                    ),
                ],
                justify="flex-end",
            ),
        ],
        opened=False,
    )

    chat = dmc.Modal(
        title="Chat window",
        size="lg",
        id={
            "type": "modal",
            "id": "chat",
        },
        children=[
            html.Div(
                children=[
                    dcc.Markdown(
                        "In this chat window, we take input from the text box and pass it directly to the OpenAI API, along with the data as additional context."
                    ),
                    dmc.CodeHighlight(
                        code=open("snippets/chat.py").read(),
                        language="python",
                    ),
                    dcc.Markdown(
                        "With traditional Python syntax, we provide the dataset as context to help answer questions, ensure the prompt is well-structured, and can stream back the response."
                    ),
                ]
            ),
            dmc.Group(
                [
                    dmc.Button(
                        "Close",
                        color="red",
                        variant="outline",
                        id={
                            "type": "modal-close",
                            "id": "chat",
                        },
                    ),
                ],
                justify="flex-end",
            ),
        ],
        opened=False,
    )

    insights = dmc.Modal(
        title="Smart Insights",
        size="lg",
        id={
            "type": "modal",
            "id": "insights",
        },
        children=[
            html.Div(
                children=[
                    dcc.Markdown(
                        "Smart Insights is a Dash Enterprise feature which allows users to chat with their data simply by enabling a flag in `ddk.Graph`."
                    ),
                    dmc.CodeHighlight(
                        code=open("snippets/smart_insights.py").read(),
                        language="python",
                    ),
                    dcc.Markdown(
                        "Developers pass their Smart Insights configuration, and the interface is added to charts automatically."
                    ),
                ]
            ),
            dmc.Group(
                [
                    dmc.Button(
                        "Close",
                        color="red",
                        variant="outline",
                        id={
                            "type": "modal-close",
                            "id": "insights",
                        },
                    ),
                ],
                justify="flex-end",
            ),
        ],
        opened=False,
    )

    dropdown = dmc.Modal(
        title="Adding Context",
        size="lg",
        id={
            "type": "modal",
            "id": "dropdown",
        },
        children=[
            html.Div(
                children=[
                    dcc.Markdown(
                        "Similar to the world events toggles, structured outputs can be leveraged in Dash apps to generate prose to add the UI. Here, we add prose automatically to describe selected datasets."
                    ),
                    dmc.CodeHighlight(
                        code=open("snippets/dropdown.py").read(),
                        language="python",
                    ),
                    dcc.Markdown(
                        "The styling capabilities of Dash Design Kit make it easy to give the outputs a great look and feel consistent with the rest of the Dash app."
                    ),
                ]
            ),
            dmc.Group(
                [
                    dmc.Button(
                        "Close",
                        color="red",
                        variant="outline",
                        id={
                            "type": "modal-close",
                            "id": "dropdown",
                        },
                    ),
                ],
                justify="flex-end",
            ),
        ],
        opened=False,
    )

    return html.Div([annotations, chat, insights, dropdown])


app.layout = dmc.MantineProvider(
    ddk.App(
        [
            dcc.Location(id="pathname"),
            ddk.Header(
                [
                    dcc.Link(
                        href=app.get_relative_path("/"),
                        id="logo",
                    ),
                    ddk.Title(id="title"),
                ]
            ),
            modals(),
            ddk.Block(
                [
                    html.H4(
                        "Office of Financial Research - Financial Stress Index (OFR FSI)"
                    ),
                    html.P(
                        "The Office of Financial Research Financial Stress Index (OFR FSI) measures the level of stress in the U.S. financial system. It helps identify periods of heightened risk and instability, providing insights into potential financial crises or market disruptions. Spikes in the index indicate elevated stress, often triggered by economic, political, or market events. By monitoring the OFR FSI, users can gain insights into the overall health of the U.S. financial system and anticipate potential risks in the economy.",
                    ),
                ]
            ),
            ddk.Row(
                [
                    ddk.Card(
                        ddk.Row(
                            [
                                ddk.Block(
                                    [
                                        html.Div(
                                            [
                                                DashIconify(
                                                    icon="feather:info",
                                                    color="#012169",
                                                    width=60,
                                                    style={"marginRight": "10px"},
                                                ),
                                                html.Div(
                                                    "This chart uses an LLM with structured outputs to add annotations to the chart. When a user clicks the toggle switches, it sends data to the LLM requesting annotation dynamically."
                                                ),
                                                dmc.Button(
                                                    "Learn more",
                                                    id={
                                                        "type": "modal-open",
                                                        "id": "annotations",
                                                    },
                                                    color="blue",
                                                ),
                                            ],
                                            style={
                                                "display": "flex",
                                                "flexDirection": "row",
                                                "alignItems": "center",
                                            },
                                        ),
                                        html.Br(),
                                        dmc.Select(
                                            id="select_GFSI_ticker",
                                            data=GFSI_options(),
                                            value="OFR FSI",
                                        ),
                                        dcc.Loading(
                                            children=ddk.Graph(
                                                style={"height": "calc(40vh)"},
                                                id="GFSI-line-chart",
                                            ),
                                            type="circle",
                                            color="#5f2167",
                                        ),
                                        dmc.Switch(
                                            label="Add World Events (AI insights)",
                                            id="insights-switch-world",
                                        ),
                                        dmc.Space(h=5),
                                        dmc.Switch(
                                            label="Add Financial Events (AI insights)",
                                            id="insights-switch-finance",
                                        ),
                                    ],
                                    width=50,
                                ),
                                dmc.Space(w=10),
                                dmc.Divider(
                                    orientation="vertical", style={"width": "10px"}
                                ),
                                ddk.Block(
                                    [
                                        html.Div(
                                            [
                                                DashIconify(
                                                    icon="feather:info",
                                                    color="#012169",
                                                    width=60,
                                                    style={"marginRight": "10px"},
                                                ),
                                                html.Div(
                                                    "This chat window allows users to ask questions directly to the dataset contained in the chart. It's powered by traditional Dash callbacks and layouts!"
                                                ),
                                                dmc.Button(
                                                    "Learn more",
                                                    id={
                                                        "type": "modal-open",
                                                        "id": "chat",
                                                    },
                                                    color="blue",
                                                ),
                                            ],
                                            style={
                                                "display": "flex",
                                                "flexDirection": "row",
                                                "alignItems": "center",
                                            },
                                        ),
                                        html.Div(id="chatbot_response"),
                                        html.Div(
                                            [
                                                dmc.TextInput(
                                                    id="user_input",
                                                    placeholder="Ask a question about the selected data...",
                                                    w=500,
                                                ),
                                                dmc.Button(
                                                    "Submit",
                                                    id="submit_button",
                                                    className="submit-button",
                                                ),
                                            ],
                                            className="flex-row",
                                            style={
                                                "position": "absolute",
                                                "bottom": "0",
                                                "width": "100%",  # Ensures it stretches across the parent div
                                            },
                                        ),
                                        dmc.Space(h=10),
                                    ],
                                    width=50,
                                    style={
                                        "position": "relative",
                                        "overflow": "hidden",
                                    },
                                ),
                            ]
                        )
                    ),
                ],
            ),
            ddk.Block(
                [
                    html.P(
                        "This chart illustrates the volatility skew for the UKX options, providing valuable insights into market sentiment and investor behaviour. Monitoring these trends can help identify shifts in risk perception. For example, a rising put skew might indicate growing caution in the market, while a falling call skew can signal lower expectations for significant upward movements.",
                    ),
                ]
            ),
            dmc.Space(h=10),
            dmc.Divider(variant="dashed"),
            dmc.Space(h=10),
            ddk.Row(
                [
                    ddk.DataCard(
                        value="{0:.2f}".format(
                            ddk.datasets.tickers[ticker]().iloc[-1, 1]
                        ),
                        label=ticker,
                        trace_y=random.sample(range(40, 100), 50),
                        color=color,
                    )
                    for ticker, color in zip(
                        ddk.datasets.tickers,
                        ["#ea7600", "#5f2167", "#bababa", "#c41230"],
                    )
                ],
            ),
            ddk.Row(
                [
                    ddk.Card(
                        [
                            html.Div(
                                [
                                    DashIconify(
                                        icon="feather:info",
                                        color="#012169",
                                        width=60,
                                        style={"marginRight": "10px"},
                                    ),
                                    html.Div(
                                        "With Smart Insights, your app's users can get automatically generated text-based insights about the figures in your app and interact with the figure data by asking questions.Insights can be generated using AI—via large language models (LLMs)—or can be manually defined."
                                    ),
                                    dmc.Button(
                                        "Learn more",
                                        id={
                                            "type": "modal-open",
                                            "id": "insights",
                                        },
                                        color="blue",
                                    ),
                                ],
                                style={
                                    "display": "flex",
                                    "flexDirection": "row",
                                    "alignItems": "center",
                                },
                            ),
                            html.Br(),
                            ddk.Graph(
                                figure=generate_herfindahl_hirschman_index(),
                                insights=chatbot_builder.SmartInsights(),
                            ),
                        ],
                        width=35,
                    ),
                    ddk.Card(
                        [
                            html.Div(
                                [
                                    DashIconify(
                                        icon="feather:info",
                                        color="#012169",
                                        width=30,
                                        style={"marginRight": "10px"},
                                    ),
                                    html.Div(
                                        "When stocks are selected in the dropdown, an LLM is queried to provide additional context about the stock."
                                    ),
                                    dmc.Button(
                                        "Learn more",
                                        id={
                                            "type": "modal-open",
                                            "id": "dropdown",
                                        },
                                        color="blue",
                                    ),
                                ],
                                style={
                                    "display": "flex",
                                    "flexDirection": "row",
                                    "alignItems": "center",
                                },
                            ),
                            html.Div(
                                [
                                    dmc.MultiSelect(
                                        id="select_stock",
                                        data=SP_options(),
                                        value=[SP_options()[0]["value"]],
                                        searchable=True,
                                    ),
                                    dmc.Space(w=10),
                                    dmc.SegmentedControl(
                                        data=["Unweighted", "Weighted"],
                                        value="Unweighted",
                                        id="weighted-stocks",
                                        style={"width": "250px", "height": "38px"},
                                    ),
                                ],
                                className="flex-row center-align",
                            ),
                            dmc.Space(h=5),
                            dcc.Loading(
                                children=html.Div(id="ticker-descriptions"),
                                type="circle",
                                color="#5f2167",
                            ),
                            ddk.Graph(id="stock_graph"),
                        ],
                        width=65,
                    ),
                ]
            ),
        ]
    )
)


@callback(
    Output({"type": "modal", "id": MATCH}, "opened"),
    Input({"type": "modal-open", "id": MATCH}, "n_clicks"),
    Input({"type": "modal-close", "id": MATCH}, "n_clicks"),
    State({"type": "modal", "id": MATCH}, "opened"),
    prevent_initial_call=True,
)
def modal_demo(nc1, nc2, opened):
    return not opened


@callback(
    Output("GFSI-line-chart", "figure"),
    Output("user_input", "value"),
    Output("chatbot_response", "children"),
    Input("select_GFSI_ticker", "value"),
    Input("insights-switch-world", "checked"),
    Input("insights-switch-finance", "checked"),
)
def update_GFSI_line_chart(ticker, world_switch, finance_switch):
    fig = generate_GFSI_line_chart(ticker)
    user_prompt = dash.no_update
    response_output = dash.no_update
    if ctx.triggered_id == "select_GFSI_ticker":
        user_prompt = None
        response_output = None

    if world_switch:
        prompt = f"I would like the top 10 world events that could have influenced the GFSI after the year 2000, just name the event. The year should be in the foramt %Y-%m-%d"
        line_color = "#f2a900"
        fig = add_gfsi_events(fig, prompt, line_color)
    if finance_switch:
        prompt = f"I would like the top 10 financial events that could have influenced the GFSI after the year 2000, just name the event. The year should be in the foramt %Y-%m-%d"
        line_color = "#279f00"
        fig = add_gfsi_events(fig, prompt, line_color)
    return fig, user_prompt, response_output


@callback(
    Output("chatbot_response", "style"),
    Input("submit_button", "n_clicks"),
    Input("select_GFSI_ticker", "value"),
    State("user_input", "value"),
)
def show_chatbot_response_box(n_clicks, ticker, user_input):
    if n_clicks is None or n_clicks == 0 or user_input is None or user_input == "":
        return {"display": "none"}
    return {
        "background-color": "#d4eccd50",
        "color": "black",
        "border": "1px solid #d4eccd",
        "padding": "10px",
        "border-radius": "4px",
    }


@callback(
    Output("chatbot_response", "children", allow_duplicate=True),
    Input("submit_button", "n_clicks"),
    State("user_input", "value"),
    State("select_GFSI_ticker", "value"),
    progress=Output("chatbot_response", "children"),
    progress_default="",
    background=True,
    interval=100,
    prevent_initial_call=True,
)
def update_chatbot_response(set_progress, n_clicks, user_input, ticker):
    if n_clicks is None or n_clicks == 0 or user_input is None or user_input == "":
        raise dash.exceptions.PreventUpdate
    data = pd.read_csv("data/fsi.csv")[["Date", ticker]]
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "You are a data analyst for a bank, provide insightful calculations and answers. Answer in 4 sentences or less.",
            },
            {"role": "user", "content": f"Given this data {str(data)}, {user_input}"},
        ],
        stream=True,
    )
    state = ""
    for chunk in response:
        if chunk.choices[0].delta.content:
            state += chunk.choices[0].delta.content
            set_progress(state)
    return state


@callback(
    Output("stock_graph", "figure"),
    Input("select_stock", "value"),
    Input("weighted-stocks", "value"),
)
def update_SP_500_stocks(stocks, weighted_stocks):
    return generate_SP_500_stocks(stocks, weighted_stocks)


@callback(
    Output("logo", "children"), Output("title", "children"), Input("pathname", "hash")
)
def set_logo(query):
    title = "Financial Market Insights"
    logo = ddk.Logo(src=app.get_asset_url("plotly_logo.png"))
    return logo, title


@callback(
    Output("ticker-descriptions", "children"),
    Input("select_stock", "value"),
)
def add_stock_descriptions(stocks):
    response = generate_ticker_descriptions(stocks)
    if not response:
        return dash.no_update
    layout = []
    for i, (ticker, description) in enumerate(
        zip(response.ticker, response.description)
    ):
        layout.append(
            html.Div(
                [
                    html.Span(
                        ticker,
                        className="badge",
                        style={
                            "background-color": "#012169" "#012169",
                            "color": "white",
                            "padding": "5px 10px",
                            "border-radius": "10px",
                            "margin-right": "10px",
                        },
                    ),
                    html.Span(description, style={"font-size": "16px"}),
                ],
            )
        )
    return layout


server = app.server
if __name__ == "__main__":
    app.run_server(debug=True)
