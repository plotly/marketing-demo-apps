responses = client.beta.chat.completions.parse(
    model="gpt-4o-2024-08-06",
    messages=[
        {"role": "system", "content": "You work in Finance."},
        {
            "role": "user",
            "content": f"Give me a on sentence description of each ticker in this list {stocks}. Dont include the ticker name in the description.",
        },
    ],
    response_format=TickerInformation,
)

response = responses.choices[0].message.parsed

layout = []
for i, (ticker, description) in enumerate(zip(response.ticker, response.description)):
    layout.append(
        html.Div(
            [
                html.Span(
                    ticker,
                    className="badge",
                    style={
                        "background-color": layout_colorway[i]
                        if i < len(layout_colorway)
                        else "#012169",
                        "color": "white",
                        "padding": "5px 10px",
                        "border-radius": "10px",
                        "margin-right": "10px",
                    },
                ),
                html.Span(description, style={"font-size": "16px"}),
            ],
            style={"margin-bottom": "10px"},
        )
    )
