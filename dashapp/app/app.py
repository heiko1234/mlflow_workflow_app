

import dash
from dash import Dash, html, dcc

from app.utilities.sidebar_utils import (
    icon_and_text
)


from flask import Flask



server = Flask(__name__)

# session store
a_session_store = dcc.Store(
    id = "a_session_store", storage_type="session"
)

# localhost/dashapp/pages_id
url_base_pathname="/mlflowapp"

app = Dash(
    __name__,
    server = server,
    url_base_pathname="/mlflowapp/",
    use_pages=True
    )

app.title = "MLFlow App"





sidebar = html.Div(
    [
        html.Div(
            [
                html.H2("Basic App", style={"color": "white"}),
            ],
            className="sidebar-header",
            ),
        html.Div(
            dcc.Markdown("\n---\n")
        ),
        icon_and_text(id="side_home", text="Home", icon="home", href=url_base_pathname+dash.page_registry['pages.home']['path']),
        icon_and_text(id="side_landing", text="Landing", icon="update", href=url_base_pathname+dash.page_registry['pages.landing.landing']['path']),
        # icon_and_text(id="side_data", text="Data", icon="analysis1", href=url_base_pathname+dash.page_registry['pages.data']['path']),
        # icon_and_text(id="side_increase", text="Benefit", icon="increase", href=url_base_pathname+dash.page_registry['pages.increase']['path']),
    ],
    className="sidebar"
)

app.layout = html.Div(
    [
        sidebar,
        a_session_store,
        html.Div(
            [
                dash.page_container
            ],
            className="content",
        ),
    ]
)

