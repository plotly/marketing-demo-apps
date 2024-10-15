import os

import dash
from openai import OpenAI

from dotenv import load_dotenv

load_dotenv()

dash._dash_renderer._set_react_version("18.2.0")

app = dash.Dash(
    "Dash app",
    suppress_callback_exceptions=True,
)

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", None))
