def add_gfsi_events(fig, prompt, line_color):
    responses = client.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",
        messages=[
            {"role": "system", "content": "You work in Finance."},
            {"role": "user", "content": prompt},
        ],
        response_format=CalendarEvent,
    )
    response = responses.choices[0].message.parsed
    try:
        for event, date in zip(response.world_event, response.date):
            fig.add_vline(
                x=datetime.strptime(date, "%Y-%m-%d").timestamp() * 1000,
                line=dict(dash="dash"),
                annotation_text=event,
                annotation=dict(textangle=270, showarrow=False),
                line_color=line_color,
            )
    except:
        fig = dash.no_update
    return fig
