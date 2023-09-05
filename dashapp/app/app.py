

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
project_basic_session_store = dcc.Store(
    id = "project_basic_session_store", storage_type="session"
)
data_session_store = dcc.Store(
    id = "data_session_store", storage_type="session"
)
project_target_feature_session_store = dcc.Store(
    id = "project_target_feature_session_store", storage_type="session"
)
project_data_spc_cleaning_session_store = dcc.Store(
    id = "project_data_spc_cleaning_session_store", storage_type="session"
)
project_data_spc_limit_cleaning_session_store = dcc.Store(
    id = "project_data_spc_limit_cleaning_session_store", storage_type="session"
)
project_data_evaluation_session_store = dcc.Store(
    id = "project_evaluation_session_store", storage_type="session"
)
project_model_name_session_store = dcc.Store(
    id = "project_model_name_session_store", storage_type="session"
)


# localhost/dashapp/pages_id
url_base_pathname="/aimate"

app = Dash(
    __name__,
    server = server,
    url_base_pathname="/aimate/",
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
        icon_and_text(id="side_landing", text="Start", icon="get_started", href=url_base_pathname+dash.page_registry['pages.landing.landing']['path']),
        icon_and_text(id="side_data", text="Data", icon="data", href=url_base_pathname+dash.page_registry['pages.dataload.dataload']['path']),
        icon_and_text(id="side_analysis", text="Analysis", icon="analysis3", href=url_base_pathname+dash.page_registry['pages.analysis.analysis']['path']),
        icon_and_text(id="side_selection", text="Preprocess", icon="analysis1", href=url_base_pathname+dash.page_registry['pages.preprocess.preprocess']['path']),
        icon_and_text(id="side_model", text="Modelling", icon="ai1", href=url_base_pathname+dash.page_registry['pages.model.model']['path']),
        icon_and_text(id="side_validate", text="Validation", icon="analysis5", href=url_base_pathname+dash.page_registry['pages.validation.validation']['path']),
        icon_and_text(id="side_evalidate", text="Evalidation", icon="analysis6", href=url_base_pathname+dash.page_registry['pages.evaluation.evaluation']['path']),
        # icon_and_text(id="side_data", text="Data", icon="analysis1", href=url_base_pathname+dash.page_registry['pages.data']['path']),
        # icon_and_text(id="side_increase", text="Benefit", icon="increase", href=url_base_pathname+dash.page_registry['pages.increase']['path']),
    ],
    className="sidebar"
)

app.layout = html.Div(
    [
        sidebar,
        a_session_store,
        project_basic_session_store,
        data_session_store,
        project_target_feature_session_store,
        project_data_spc_cleaning_session_store,
        project_data_spc_limit_cleaning_session_store,
        project_data_evaluation_session_store,
        project_model_name_session_store,
        html.Div(
            [
                dash.page_container
            ],
            className="content",
        ),
    ]
)

