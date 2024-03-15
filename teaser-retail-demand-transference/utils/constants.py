# Sankey Graph
SANKEY_COLORS = [
    "rgba(31, 119, 180, 0.8)",
    "rgba(255, 127, 14, 0.8)",
    "rgba(44, 160, 44, 0.8)",
    "rgba(214, 39, 40, 0.8)",
    "rgba(148, 103, 189, 0.8)",
    "rgba(140, 86, 75, 0.8)",
    "rgba(227, 119, 194, 0.8)",
    "rgba(127, 127, 127, 0.8)",
    "rgba(188, 189, 34, 0.8)",
    "rgba(23, 190, 207, 0.8)",
    "rgba(31, 119, 180, 0.8)",
    "rgba(255, 127, 14, 0.8)",
    "rgba(44, 160, 44, 0.8)",
    "rgba(214, 39, 40, 0.8)",
    "rgba(148, 103, 189, 0.8)",
    "rgba(140, 86, 75, 0.8)",
    "rgba(227, 119, 194, 0.8)",
    "rgba(127, 127, 127, 0.8)",
    "rgba(188, 189, 34, 0.8)",
    "rgba(23, 190, 207, 0.8)",
    "rgba(31, 119, 180, 0.8)",
    "rgba(255, 127, 14, 0.8)",
    "rgba(44, 160, 44, 0.8)",
    "rgba(214, 39, 40, 0.8)",
    "rgba(148, 103, 189, 0.8)",
    "rgba(140, 86, 75, 0.8)",
    "rgba(227, 119, 194, 0.8)",
    "rgba(127, 127, 127, 0.8)",
    "rgba(188, 189, 34, 0.8)",
    "rgba(23, 190, 207, 0.8)",
    "rgba(31, 119, 180, 0.8)",
    "rgba(255, 127, 14, 0.8)",
    "rgba(44, 160, 44, 0.8)",
    "rgba(214, 39, 40, 0.8)",
    "rgba(148, 103, 189, 0.8)",
    "magenta",
    "rgba(227, 119, 194, 0.8)",
    "rgba(127, 127, 127, 0.8)",
    "rgba(188, 189, 34, 0.8)",
    "rgba(23, 190, 207, 0.8)",
    "rgba(31, 119, 180, 0.8)",
    "rgba(255, 127, 14, 0.8)",
    "rgba(44, 160, 44, 0.8)",
    "rgba(214, 39, 40, 0.8)",
    "rgba(148, 103, 189, 0.8)",
    "rgba(140, 86, 75, 0.8)",
    "rgba(227, 119, 194, 0.8)",
    "rgba(127, 127, 127, 0.8)",
    "rgba(31, 119, 180, 0.8)",
    "rgba(255, 127, 14, 0.8)",
    "rgba(44, 160, 44, 0.8)",
    "rgba(214, 39, 40, 0.8)",
    "rgba(148, 103, 189, 0.8)",
    "rgba(140, 86, 75, 0.8)",
    "rgba(227, 119, 194, 0.8)",
    "rgba(127, 127, 127, 0.8)",
    "rgba(188, 189, 34, 0.8)",
    "rgba(23, 190, 207, 0.8)",
    "rgba(31, 119, 180, 0.8)",
    "rgba(255, 127, 14, 0.8)",
    "rgba(44, 160, 44, 0.8)",
    "rgba(214, 39, 40, 0.8)",
    "rgba(148, 103, 189, 0.8)",
    "rgba(140, 86, 75, 0.8)",
    "rgba(227, 119, 194, 0.8)",
    "rgba(127, 127, 127, 0.8)",
    "rgba(188, 189, 34, 0.8)",
    "rgba(23, 190, 207, 0.8)",
    "rgba(31, 119, 180, 0.8)",
    "rgba(255, 127, 14, 0.8)",
    "rgba(44, 160, 44, 0.8)",
    "rgba(214, 39, 40, 0.8)",
    "rgba(148, 103, 189, 0.8)",
    "rgba(140, 86, 75, 0.8)",
    "rgba(227, 119, 194, 0.8)",
    "rgba(127, 127, 127, 0.8)",
    "rgba(188, 189, 34, 0.8)",
    "rgba(23, 190, 207, 0.8)",
    "rgba(31, 119, 180, 0.8)",
    "rgba(255, 127, 14, 0.8)",
    "rgba(44, 160, 44, 0.8)",
    "rgba(214, 39, 40, 0.8)",
    "rgba(148, 103, 189, 0.8)",
    "magenta",
    "rgba(227, 119, 194, 0.8)",
    "rgba(127, 127, 127, 0.8)",
    "rgba(188, 189, 34, 0.8)",
    "rgba(23, 190, 207, 0.8)",
    "rgba(31, 119, 180, 0.8)",
    "rgba(255, 127, 14, 0.8)",
    "rgba(44, 160, 44, 0.8)",
    "rgba(214, 39, 40, 0.8)",
    "rgba(148, 103, 189, 0.8)",
    "rgba(140, 86, 75, 0.8)",
    "rgba(227, 119, 194, 0.8)",
    "rgba(127, 127, 127, 0.8)",
    "rgba(31, 119, 180, 0.8)",
    "rgba(255, 127, 14, 0.8)",
    "rgba(44, 160, 44, 0.8)",
    "rgba(214, 39, 40, 0.8)",
    "rgba(148, 103, 189, 0.8)",
    "rgba(140, 86, 75, 0.8)",
    "rgba(227, 119, 194, 0.8)",
    "rgba(127, 127, 127, 0.8)",
    "rgba(188, 189, 34, 0.8)",
    "rgba(23, 190, 207, 0.8)",
    "rgba(31, 119, 180, 0.8)",
    "rgba(255, 127, 14, 0.8)",
    "rgba(44, 160, 44, 0.8)",
    "rgba(214, 39, 40, 0.8)",
    "rgba(148, 103, 189, 0.8)",
    "rgba(140, 86, 75, 0.8)",
    "rgba(227, 119, 194, 0.8)",
    "rgba(127, 127, 127, 0.8)",
    "rgba(188, 189, 34, 0.8)",
    "rgba(23, 190, 207, 0.8)",
    "rgba(31, 119, 180, 0.8)",
    "rgba(255, 127, 14, 0.8)",
    "rgba(44, 160, 44, 0.8)",
    "rgba(214, 39, 40, 0.8)",
    "rgba(148, 103, 189, 0.8)",
    "rgba(140, 86, 75, 0.8)",
    "rgba(227, 119, 194, 0.8)",
    "rgba(127, 127, 127, 0.8)",
    "rgba(188, 189, 34, 0.8)",
    "rgba(23, 190, 207, 0.8)",
    "rgba(31, 119, 180, 0.8)",
    "rgba(255, 127, 14, 0.8)",
    "rgba(44, 160, 44, 0.8)",
    "rgba(214, 39, 40, 0.8)",
    "rgba(148, 103, 189, 0.8)",
    "magenta",
    "rgba(227, 119, 194, 0.8)",
    "rgba(127, 127, 127, 0.8)",
    "rgba(188, 189, 34, 0.8)",
    "rgba(23, 190, 207, 0.8)",
    "rgba(31, 119, 180, 0.8)",
    "rgba(255, 127, 14, 0.8)",
    "rgba(44, 160, 44, 0.8)",
    "rgba(214, 39, 40, 0.8)",
    "rgba(148, 103, 189, 0.8)",
    "rgba(140, 86, 75, 0.8)",
    "rgba(227, 119, 194, 0.8)",
    "rgba(127, 127, 127, 0.8)",
    "rgba(31, 119, 180, 0.8)",
    "rgba(255, 127, 14, 0.8)",
    "rgba(44, 160, 44, 0.8)",
    "rgba(214, 39, 40, 0.8)",
    "rgba(148, 103, 189, 0.8)",
    "rgba(140, 86, 75, 0.8)",
    "rgba(227, 119, 194, 0.8)",
    "rgba(127, 127, 127, 0.8)",
    "rgba(188, 189, 34, 0.8)",
    "rgba(23, 190, 207, 0.8)",
    "rgba(31, 119, 180, 0.8)",
    "rgba(255, 127, 14, 0.8)",
    "rgba(44, 160, 44, 0.8)",
    "rgba(214, 39, 40, 0.8)",
    "rgba(148, 103, 189, 0.8)",
    "rgba(140, 86, 75, 0.8)",
    "rgba(227, 119, 194, 0.8)",
    "rgba(127, 127, 127, 0.8)",
    "rgba(188, 189, 34, 0.8)",
    "rgba(23, 190, 207, 0.8)",
    "rgba(31, 119, 180, 0.8)",
    "rgba(255, 127, 14, 0.8)",
    "rgba(44, 160, 44, 0.8)",
    "rgba(214, 39, 40, 0.8)",
    "rgba(148, 103, 189, 0.8)",
    "rgba(140, 86, 75, 0.8)",
    "rgba(227, 119, 194, 0.8)",
    "rgba(127, 127, 127, 0.8)",
    "rgba(188, 189, 34, 0.8)",
    "rgba(23, 190, 207, 0.8)",
    "rgba(31, 119, 180, 0.8)",
    "rgba(255, 127, 14, 0.8)",
    "rgba(44, 160, 44, 0.8)",
    "rgba(214, 39, 40, 0.8)",
    "rgba(148, 103, 189, 0.8)",
    "magenta",
    "rgba(227, 119, 194, 0.8)",
    "rgba(127, 127, 127, 0.8)",
    "rgba(188, 189, 34, 0.8)",
    "rgba(23, 190, 207, 0.8)",
    "rgba(31, 119, 180, 0.8)",
    "rgba(255, 127, 14, 0.8)",
    "rgba(44, 160, 44, 0.8)",
    "rgba(214, 39, 40, 0.8)",
    "rgba(148, 103, 189, 0.8)",
    "rgba(140, 86, 75, 0.8)",
    "rgba(227, 119, 194, 0.8)",
    "rgba(127, 127, 127, 0.8)",
]

SANKEY_LINK_COLORS = [
    "rgba(31, 119, 180, 0.5)",
    "rgba(255, 127, 14, 0.5)",
    "rgba(44, 160, 44, 0.5)",
    "rgba(214, 39, 40, 0.5)",
    "rgba(148, 103, 189, 0.5)",
    "rgba(140, 86, 75, 0.5)",
    "rgba(227, 119, 194, 0.5)",
    "rgba(127, 127, 127, 0.5)",
    "rgba(188, 189, 34, 0.5)",
    "rgba(23, 190, 207, 0.5)",
    "rgba(31, 119, 180, 0.5)",
    "rgba(255, 127, 14, 0.5)",
    "rgba(44, 160, 44, 0.5)",
    "rgba(214, 39, 40, 0.5)",
    "rgba(148, 103, 189, 0.5)",
    "rgba(140, 86, 75, 0.5)",
    "rgba(227, 119, 194, 0.5)",
    "rgba(127, 127, 127, 0.5)",
    "rgba(188, 189, 34, 0.5)",
    "rgba(23, 190, 207, 0.5)",
    "rgba(31, 119, 180, 0.5)",
    "rgba(255, 127, 14, 0.5)",
    "rgba(44, 160, 44, 0.5)",
    "rgba(214, 39, 40, 0.5)",
    "rgba(148, 103, 189, 0.5)",
    "rgba(140, 86, 75, 0.5)",
    "rgba(227, 119, 194, 0.5)",
    "rgba(127, 127, 127, 0.5)",
    "rgba(188, 189, 34, 0.5)",
    "rgba(23, 190, 207, 0.5)",
    "rgba(31, 119, 180, 0.5)",
    "rgba(255, 127, 14, 0.5)",
    "rgba(44, 160, 44, 0.5)",
    "rgba(214, 39, 40, 0.5)",
    "rgba(148, 103, 189, 0.5)",
    "rgba(227, 119, 194, 0.5)",
    "rgba(127, 127, 127, 0.5)",
    "rgba(188, 189, 34, 0.5)",
    "rgba(23, 190, 207, 0.5)",
    "rgba(31, 119, 180, 0.5)",
    "rgba(255, 127, 14, 0.5)",
    "rgba(44, 160, 44, 0.5)",
    "rgba(214, 39, 40, 0.5)",
    "rgba(148, 103, 189, 0.5)",
    "rgba(140, 86, 75, 0.5)",
    "rgba(227, 119, 194, 0.5)",
    "rgba(127, 127, 127, 0.5)",
    "rgba(31, 119, 180, 0.5)",
    "rgba(255, 127, 14, 0.5)",
    "rgba(44, 160, 44, 0.5)",
    "rgba(214, 39, 40, 0.5)",
    "rgba(148, 103, 189, 0.5)",
    "rgba(140, 86, 75, 0.5)",
    "rgba(227, 119, 194, 0.5)",
    "rgba(127, 127, 127, 0.5)",
    "rgba(188, 189, 34, 0.5)",
    "rgba(23, 190, 207, 0.5)",
    "rgba(31, 119, 180, 0.5)",
    "rgba(255, 127, 14, 0.5)",
    "rgba(44, 160, 44, 0.5)",
    "rgba(214, 39, 40, 0.5)",
    "rgba(148, 103, 189, 0.5)",
    "rgba(140, 86, 75, 0.5)",
    "rgba(227, 119, 194, 0.5)",
    "rgba(127, 127, 127, 0.5)",
    "rgba(188, 189, 34, 0.5)",
    "rgba(23, 190, 207, 0.5)",
    "rgba(31, 119, 180, 0.5)",
    "rgba(255, 127, 14, 0.5)",
    "rgba(44, 160, 44, 0.5)",
    "rgba(214, 39, 40, 0.5)",
    "rgba(148, 103, 189, 0.5)",
    "rgba(140, 86, 75, 0.5)",
    "rgba(227, 119, 194, 0.5)",
    "rgba(127, 127, 127, 0.5)",
    "rgba(188, 189, 34, 0.5)",
    "rgba(23, 190, 207, 0.5)",
    "rgba(31, 119, 180, 0.5)",
    "rgba(255, 127, 14, 0.5)",
    "rgba(44, 160, 44, 0.5)",
    "rgba(214, 39, 40, 0.5)",
    "rgba(148, 103, 189, 0.5)",
    "rgba(227, 119, 194, 0.5)",
    "rgba(127, 127, 127, 0.5)",
    "rgba(188, 189, 34, 0.5)",
    "rgba(23, 190, 207, 0.5)",
    "rgba(31, 119, 180, 0.5)",
    "rgba(255, 127, 14, 0.5)",
    "rgba(44, 160, 44, 0.5)",
    "rgba(214, 39, 40, 0.5)",
    "rgba(148, 103, 189, 0.5)",
    "rgba(140, 86, 75, 0.5)",
    "rgba(227, 119, 194, 0.5)",
    "rgba(127, 127, 127, 0.5)",
    "rgba(31, 119, 180, 0.5)",
    "rgba(255, 127, 14, 0.5)",
    "rgba(44, 160, 44, 0.5)",
    "rgba(214, 39, 40, 0.5)",
    "rgba(148, 103, 189, 0.5)",
    "rgba(140, 86, 75, 0.5)",
    "rgba(227, 119, 194, 0.5)",
    "rgba(127, 127, 127, 0.5)",
    "rgba(188, 189, 34, 0.5)",
    "rgba(23, 190, 207, 0.5)",
    "rgba(31, 119, 180, 0.5)",
    "rgba(255, 127, 14, 0.5)",
    "rgba(44, 160, 44, 0.5)",
    "rgba(214, 39, 40, 0.5)",
    "rgba(148, 103, 189, 0.5)",
    "rgba(140, 86, 75, 0.5)",
    "rgba(227, 119, 194, 0.5)",
    "rgba(127, 127, 127, 0.5)",
    "rgba(188, 189, 34, 0.5)",
    "rgba(23, 190, 207, 0.5)",
    "rgba(31, 119, 180, 0.5)",
    "rgba(255, 127, 14, 0.5)",
    "rgba(44, 160, 44, 0.5)",
    "rgba(214, 39, 40, 0.5)",
    "rgba(148, 103, 189, 0.5)",
    "rgba(140, 86, 75, 0.5)",
    "rgba(227, 119, 194, 0.5)",
    "rgba(127, 127, 127, 0.5)",
    "rgba(188, 189, 34, 0.5)",
    "rgba(23, 190, 207, 0.5)",
    "rgba(31, 119, 180, 0.5)",
    "rgba(255, 127, 14, 0.5)",
    "rgba(44, 160, 44, 0.5)",
    "rgba(214, 39, 40, 0.5)",
    "rgba(148, 103, 189, 0.5)",
    "rgba(227, 119, 194, 0.5)",
    "rgba(127, 127, 127, 0.5)",
    "rgba(188, 189, 34, 0.5)",
    "rgba(23, 190, 207, 0.5)",
    "rgba(31, 119, 180, 0.5)",
    "rgba(255, 127, 14, 0.5)",
    "rgba(44, 160, 44, 0.5)",
    "rgba(214, 39, 40, 0.5)",
    "rgba(148, 103, 189, 0.5)",
    "rgba(140, 86, 75, 0.5)",
    "rgba(227, 119, 194, 0.5)",
    "rgba(127, 127, 127, 0.5)",
    "rgba(31, 119, 180, 0.5)",
    "rgba(255, 127, 14, 0.5)",
    "rgba(44, 160, 44, 0.5)",
    "rgba(214, 39, 40, 0.5)",
    "rgba(148, 103, 189, 0.5)",
    "rgba(140, 86, 75, 0.5)",
    "rgba(227, 119, 194, 0.5)",
    "rgba(127, 127, 127, 0.5)",
    "rgba(188, 189, 34, 0.5)",
    "rgba(23, 190, 207, 0.5)",
    "rgba(31, 119, 180, 0.5)",
    "rgba(255, 127, 14, 0.5)",
    "rgba(44, 160, 44, 0.5)",
    "rgba(214, 39, 40, 0.5)",
    "rgba(148, 103, 189, 0.5)",
    "rgba(140, 86, 75, 0.5)",
    "rgba(227, 119, 194, 0.5)",
    "rgba(127, 127, 127, 0.5)",
    "rgba(188, 189, 34, 0.5)",
    "rgba(23, 190, 207, 0.5)",
    "rgba(31, 119, 180, 0.5)",
    "rgba(255, 127, 14, 0.5)",
    "rgba(44, 160, 44, 0.5)",
    "rgba(214, 39, 40, 0.5)",
    "rgba(148, 103, 189, 0.5)",
    "rgba(140, 86, 75, 0.5)",
    "rgba(227, 119, 194, 0.5)",
    "rgba(127, 127, 127, 0.5)",
    "rgba(188, 189, 34, 0.5)",
    "rgba(23, 190, 207, 0.5)",
    "rgba(31, 119, 180, 0.5)",
    "rgba(255, 127, 14, 0.5)",
    "rgba(44, 160, 44, 0.5)",
    "rgba(214, 39, 40, 0.5)",
    "rgba(148, 103, 189, 0.5)",
    "rgba(227, 119, 194, 0.5)",
    "rgba(127, 127, 127, 0.5)",
    "rgba(188, 189, 34, 0.5)",
    "rgba(23, 190, 207, 0.5)",
    "rgba(31, 119, 180, 0.5)",
    "rgba(255, 127, 14, 0.5)",
    "rgba(44, 160, 44, 0.5)",
    "rgba(214, 39, 40, 0.5)",
    "rgba(148, 103, 189, 0.5)",
    "rgba(140, 86, 75, 0.5)",
    "rgba(227, 119, 194, 0.5)",
    "rgba(127, 127, 127, 0.5)",
]
