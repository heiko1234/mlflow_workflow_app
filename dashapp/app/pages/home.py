import dash
from dash import html, dcc
from dash import callback_context


from app.utilities.cards import (
    home_card
)


dash.register_page(__name__,path="/")

# dash.register_page(
#     __name__,
#     path='/second',
#     title='Home Dashboard',
#     name='Home Dashboard'
# )


layout = html.Div(
    id="home_page_content",
    className="home_page_content",
    children=[
        html.Div(
            className="home_page_subcontent",
            children=[
                home_card(
                    id="landingcard",
                    header_text="Landing page",
                    text="this is the landing page",
                    icon="get_started",
                    href="landing"
                ),
                home_card(
                    id="datacard",
                    header_text="Data",
                    text="this is the data page, with an extra long description, which should be over and over several lines",
                    icon="data",
                    href="dataload"
                ),
            ],
            #style={"display": "flex"}
            ),
            html.Div(
                className="home_page_subcontent",
                children=[
                    home_card(
                        id="analysiscard",
                        header_text="Analysis page",
                        text="this is the analysis page",
                        icon="analysis3",
                        href="analysis"
                    ),
                    home_card(
                        id="preprocesscard",
                        header_text="Preproessing",
                        text="preprocess your data for best model performance",
                        icon="analysis1",
                        href="preprocess"
                    ),
            ],
            #style={"display": "flex"}
            ),
            html.Div(
                className="home_page_subcontent",
                children=[
                    home_card(
                        id="modellingcard",
                        header_text="Modelling",
                        text="create your Model",
                        icon="ai1",
                        href="model"
                    ),
                ]
            ),
            html.Div(
                className="home_page_subcontent",
                children=[
                    home_card(
                        id="validationcard",
                        header_text="Validation",
                        text="validate your Model",
                        icon="analysis5",
                        href="validation"
                    ),
                    home_card(
                        id="evaluationcard",
                        header_text="Evalution",
                        text="evalidate your Model",
                        icon="analysis6",
                        href="evalidation"
                    ),
            ],
            # style={"display": "flex"}
            )
    ]
)

