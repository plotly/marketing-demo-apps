if world_switch:
    prompt = f"I would like the top 10 world events that could have influenced the GFSI after the year 2000, just name the event. The year should be in the foramt %Y-%m-%d"
    line_color = "#f2a900"
    fig = add_gfsi_events(fig, prompt, line_color)
if finance_switch:
    prompt = f"I would like the top 10 financial events that could have influenced the GFSI after the year 2000, just name the event. The year should be in the foramt %Y-%m-%d"
    line_color = "#279f00"
    fig = add_gfsi_events(fig, prompt, line_color)
