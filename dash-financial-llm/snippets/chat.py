data = pd.read_csv("data/GFSI_History.csv")[["Date", ticker]]
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
