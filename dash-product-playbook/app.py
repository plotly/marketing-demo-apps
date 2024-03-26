import dash

# Flask syntax: https://pythonhow.com/how-a-flask-app-works/
app = dash.Dash(__name__)
app.title = "Product Playbook"
app.config["suppress_callback_exceptions"] = True
