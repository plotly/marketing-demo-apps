import copy

import dash_design_kit as ddk


def HorizontalControlCard(**kwargs) -> ddk.Card:
    """
    Replace contol card with custom horizontal control card so we can apply styling across application.
    """
    card_kwargs = copy.copy(kwargs)
    if "margin" not in card_kwargs:
        card_kwargs["margin"] = 0
    if "padding" not in card_kwargs:
        card_kwargs["padding"] = 0
    if "orientation" not in card_kwargs:
        card_kwargs["orientation"] = "horizontal"
    if "type" not in card_kwargs:
        card_kwargs["type"] = "flat"
    return ddk.ControlCard(**card_kwargs)
