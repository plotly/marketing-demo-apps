import plotly.graph_objects as go
import plotly.io as pio

layout_colorway = [
    "#013169",
    "#00ACEE",
    "#F2B900",
    "#007990",
    "#28AF00",
    "#FA7600",
    "#6F3177",
    "#CACACA",
    "#D41240",
    "#50D1BC",
    "#90A0C4",
    "#90DDFE",
    "#FFE490",
    "#90C4CF",
    "#A3DF90",
    "#FFCA90",
    "#BFA0C3",
    "#E5E5E5",
    "#F298A7",
    "#AFF0E5",
]

pio.templates["custom_theme"] = go.layout.Template(layout_colorway=layout_colorway)
