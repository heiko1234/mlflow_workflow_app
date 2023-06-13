

from dash import html, dcc
import base64
import os
from dotenv import load_dotenv


def icon_and_text(
    id,
    text,
    icon,
    href
):
    load_dotenv()
    local_run = os.getenv("LOCAL_RUN", False)
    if local_run:
        img_path = str(f"./dashapp/app/assets/{icon}.png")
    else:
        img_path = str(f"./app/assets/{icon}.png")
    encoded_img = base64.b64encode(open(img_path, "rb").read())

    output = dcc.Link(
        id = id,
        className="icon_and_text",
        children=[
            html.Img(src='data:image/png;base64,{}'.format(encoded_img.decode(),
                className="icon_and_text_img"),
            style={"display": "flex", "height": "60px", "width": "60px"}
            ),
            html.H3(text, style={"margin-left": "15px"})
        ],
        style={"display": "flex", "aling-center": "bottom"},
        href=href,
    )

    return output

