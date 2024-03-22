import dash_core_components as dcc
import dash_design_kit as ddk
from dash.dependencies import Input, Output
import pandas as pd
import requests
import dash
import dash_html_components as html

import pages

from app import app

## Page content variables
def layout():
    ## Read in Data to create product list
    df_revenue = pd.read_csv("data/Revenue_Dash.csv")
    products = df_revenue.Product.unique()

    page = ddk.Row(
        ddk.Block(
            width=100,
            children=[
                dcc.Dropdown(
                    id="product-dropdown",
                    # change to call upon data file as source of product names
                    options=[{"label": i, "value": i} for i in sorted(products)],
                    # change to show default text and not dafault product
                    value="ProductA",
                    ## Update to style dropdown
                    style={"width": 150, "margin-left": "auto", "margin-right": 10},
                ),
                dcc.Tabs(
                    id="page-tabs",
                    value="product-overview",
                    children=[
                        dcc.Tab(label="Product Overview", value="product-overview"),
                        dcc.Tab(label="Supply Chain Map", value="supply-chain-map"),
                        dcc.Tab(
                            label="Risk Mitigation Strategy",
                            value="risk-mitigation-strategy",
                        ),
                    ],
                ),
                ddk.Block(id="playbook-content", children=[]),
            ],
        )
    )
    return page


## Callback to determine page content based on selected tab
@app.callback(
    Output("playbook-content", "children"),
    [Input("page-tabs", "value"), Input("product-dropdown", "value")],
)
def display_tab_content(tab, product):
    if not product:
        return ddk.Card(
            ddk.Block(
                width=100,
                children=html.H4("Select a product."),
                style={
                    "text-align": "center",
                    "background-color": "#1c60a7",
                    "color": "white",
                }
                # add blue background color, add title and summary in white
                # ensure height is sized correctly, center writing in card
            )
        )
    if tab == "product-overview":
        content = pages.product_summary.layout(product)
    elif tab == "supply-chain-map":
        content = pages.supply_chain_map.layout(product)
    elif tab == "risk-mitigation-strategy":
        content = pages.risk_mitigation_strategy.layout(product)
    else:
        content = "404"
    return content
