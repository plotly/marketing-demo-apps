import dash_snapshots
import dash

app = dash.get_app()

snap = dash_snapshots.DashSnapshots(app)
