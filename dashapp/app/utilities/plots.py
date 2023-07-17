


import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import numpy as np

from dashapp.app.utilities.nelson import apply_rules, rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8



# plotly graphic for quality control with plotly go , outlier detection, values outside of 3 standard deviations or limits are colored red



def control_chart(data, y_name, xlabel= None, title = "Controlchart", lsl = None, usl = None, outliers = True, annotations = True, lines = True, nelson=True, mean = None, sigma = None, markersize = 6, show=False):
    """_summary_

    Args:
        data (_type_): pandas dataframe
        y_name (_type_): string of column name
        xlabel (_type_, optional): string of column name of labels. Defaults to None.
        title (str, optional): string of a title. Defaults to "Controlchart".
        lsl (_type_, optional): number. Defaults to None.
        usl (_type_, optional): number. Defaults to None.
        outliers (bool, optional): Defaults to True.
        annotations (bool, optional): Defaults to True.
        lines (bool, optional): Defaults to True.
        nelson (bool, optional): Defaults to True.
        mean (_type_, optional): number. Defaults to None.
        sigma (_type_, optional): number. Defaults to None.
        markersize (int, optional): number. Defaults to 6.
        show (bool, optional): give dict or plotly figure. Defaults to False.

    Raises:
        ValueError: _description_

    Returns:
        _type_: plotly figure
    """


    if mean == None:
        mean_data = np.nanmean(data[y_name])
    else:
        mean_data = mean
    if sigma == None:
        sigma_data = np.nanstd(data[y_name])
    else:
        sigma_data = sigma

    min_data = min(data[y_name])
    max_data = max(data[y_name])

    abs_min_x = min([min_data, lsl, mean_data - 3*sigma_data])
    abs_max_x = max([max_data, usl, mean_data + 3*sigma_data])

    spread = abs_max_x - abs_min_x

    plot_expansion = spread * 0.1

    df_out_of_control = data[(data[y_name] < mean_data - 3*sigma_data) | (data[y_name] > mean_data + 3*sigma_data)]

    if xlabel is not None:
        if isinstance(data[xlabel], pd.Series):
            label_list = data[xlabel].tolist()
            label_list = [str(i) for i in label_list]
            label_values = list(data.index)
        else:
            label_list = None
            label_values = None

    if usl < lsl:
        # usl, lsl = lsl, usl
        raise ValueError("usl must be greater than lsl")

    fig = go.Figure()

    # red areas for out of control
    # lsl
    fig.add_hline(y=float(lsl), line_color="red")
    y0 = abs_min_x-plot_expansion
    y1 = lsl
    fig.add_hrect(y0=y0, y1=y1, fillcolor="red", opacity=0.1)

    # usl
    fig.add_hline(y=float(usl), line_color="red")
    y0 = abs_max_x+plot_expansion
    y1 = usl
    fig.add_hrect(y0=y0, y1=y1, fillcolor="red", opacity=0.1)

    # normal plot
    fig.add_traces(go.Scatter(
        x=data.index,
        y=data[y_name],
        mode="markers",
        name=y_name,
        marker = dict(
            size=markersize,
        )
    ))

    if lines:
        fig.add_hline(y=mean_data, line = dict(color="blue", width=2), name="mean")
        fig.add_hline(y=mean_data + 3*sigma_data, line = dict(color="red"))
        fig.add_hline(y=mean_data - 3*sigma_data, line = dict(color="red"))
        fig.add_hline(y=mean_data + 2*sigma_data, line = dict(color="orange"), line_dash="dot")
        fig.add_hline(y=mean_data - 2*sigma_data, line = dict(color="orange"), line_dash="dot")
        fig.add_hline(y=mean_data + sigma_data, line = dict(color="black"), line_dash="dot")
        fig.add_hline(y=mean_data - sigma_data, line = dict(color="black"), line_dash="dot")

    if lsl:
        fig.add_hline(y=lsl, line = dict(color="orange"))

        lsl_data = data[data[y_name] < lsl]

        fig.add_traces(go.Scatter(
            x=lsl_data.index,
            y=lsl_data[y_name],
            mode="markers",
            name="below_lsl",
            marker = dict(
                size=markersize,
                color="orange",
                symbol="square"
            )
        ))

    if usl:
        fig.add_hline(y=usl, line = dict(color="orange"))

        usl_data = data[data[y_name] > usl]

        fig.add_traces(go.Scatter(
            x=usl_data.index,
            y=usl_data[y_name],
            mode="markers",
            name="above_usl",
            marker = dict(
                size=markersize,
                color="orange",
                symbol="square"
            )
        ))

    if outliers:
        fig.add_traces(go.Scatter(
            x=df_out_of_control.index,
            y=df_out_of_control[y_name],
            mode="markers",
            name="3 \u03B4 outliers",
            marker = dict(
                size=markersize,
                color="red",
                symbol="square"
            )
        ))


    if nelson:
        data1 = data.loc[rule1(original=data[y_name]), y_name]
        data2 = data.loc[rule2(original=data[y_name]), y_name]
        data3 = data.loc[rule3(original=data[y_name]), y_name]
        data4 = data.loc[rule4(original=data[y_name]), y_name]
        data5 = data.loc[rule5(original=data[y_name]), y_name]
        data6 = data.loc[rule6(original=data[y_name]), y_name]
        data7 = data.loc[rule7(original=data[y_name]), y_name]
        data8 = data.loc[rule8(original=data[y_name]), y_name]

        fig.add_trace(go.Scatter(x=data1.index, y=data1, mode='markers', name="rule1"))
        fig.add_trace(go.Scatter(x=data2.index, y=data2, mode='markers', name="rule2"))
        fig.add_trace(go.Scatter(x=data3.index, y=data3, mode='markers', name="rule3"))
        fig.add_trace(go.Scatter(x=data4.index, y=data4, mode='markers', name="rule4"))
        fig.add_trace(go.Scatter(x=data5.index, y=data5, mode='markers', name="rule5"))
        fig.add_trace(go.Scatter(x=data6.index, y=data6, mode='markers', name="rule6"))
        fig.add_trace(go.Scatter(x=data7.index, y=data7, mode='markers', name="rule7"))
        fig.add_trace(go.Scatter(x=data8.index, y=data8, mode='markers', name="rule8"))



    if xlabel is not None:
        fig.update_xaxes(
                tickvals=label_values,
                ticktext=label_list
            )

    if annotations:
        r_mean = round(mean_data, 2)
        r_std_data = round(sigma_data, 2)



        mean_sigma = round(mean_data + sigma_data, 2)
        mean_2sigma = round(mean_data + 2*sigma_data, 2)
        mean_3sigma = round(mean_data + 3*sigma_data, 2)

        mean_sigma_neg = round(mean_data - sigma_data, 2)
        mean_2sigma_neg = round(mean_data - 2*sigma_data, 2)
        mean_3sigma_neg = round(mean_data - 3*sigma_data, 2)

        if lines:

            fig.add_annotation(
                {
                    "font_color": "blue",
                    "xref": "paper",
                    "x": 1,
                    "y": mean_data,
                    "text": f"mean: {r_mean}",
                    "showarrow": False,
                    "yanchor": "top",
                    "yshift": 20
                }
            )

            fig.add_annotation(
                {
                    "font_color": "black",
                    "xref": "paper",
                    "x": 1,
                    "y": mean_data + sigma_data,
                    "text": f"+ \u03B4: {r_std_data}",
                    "showarrow": False,
                    "yanchor": "top",
                    "yshift": 20
                }
            )

            fig.add_annotation(
                {
                    "font_color": "black",
                    "xref": "paper",
                    "x": 1,
                    "y": mean_data - sigma_data,
                    "text": f"- \u03B4: {r_std_data}",
                    "showarrow": False,
                    "yanchor": "top",
                    "yshift": 20
                }
            )

            fig.add_annotation(
                {
                    "font_color": "orange",
                    "xref": "paper",
                    "x": 1,
                    "y": mean_data + 2*sigma_data,
                    "text": f"+ 2\u03B4: {mean_2sigma}",
                    "showarrow": False,
                    "yanchor": "top",
                    "yshift": 20
                }
            )

            fig.add_annotation(
                {
                    "font_color": "orange",
                    "xref": "paper",
                    "x": 1,
                    "y": mean_data - 2*sigma_data,
                    "text": f"- 2\u03B4: {mean_2sigma_neg}",
                    "showarrow": False,
                    "yanchor": "top",
                    "yshift": 20
                }
            )

            fig.add_annotation(
                {
                    "font_color": "red",
                    "xref": "paper",
                    "x": 1,
                    "y": mean_data + 3*sigma_data,
                    "text": f"+ 3\u03B4: {mean_3sigma}",
                    "showarrow": False,
                    "yanchor": "top",
                    "yshift": 20
                }
            )

            fig.add_annotation(
                {
                    "font_color": "red",
                    "xref": "paper",
                    "x": 1,
                    "y": mean_data - 3*sigma_data,
                    "text": f"- 3\u03B4: {mean_3sigma_neg}",
                    "showarrow": False,
                    "yanchor": "top",
                    "yshift": 20
                }
            )

        if usl:
            fig.add_annotation(
                {
                    "font_color": "orange",
                    "xref": "paper",
                    "x": 1,
                    "y": usl,
                    "text": f"USL: {usl}",
                    "showarrow": False,
                    "yanchor": "top",
                    "yshift": 0
                }
            )

        if lsl:
            fig.add_annotation(
                {
                    "font_color": "orange",
                    "xref": "paper",
                    "x": 1,
                    "y": lsl,
                    "text": f"LSL: {lsl}",
                    "showarrow": False,
                    "yanchor": "top",
                    "yshift": 0
                }
            )

    if show:
        fig.show()

    else:
        return fig



data = pd.DataFrame()

data["x"] = np.random.normal(0, 1, 50)
data["y"] = np.random.normal(0, 1, 50)
# random labels, not repeated, 1000
data["text"] = np.random.choice(list("ABCDEFGHIJ"), 50, replace=True)

data


control_chart(
    data=data,
    y_name="y",
    usl=3,
    lsl=-3,
    xlabel="text",
    outliers=True,
    nelson=True,
    annotations=True,
    lines=True,
    mean = None,
    sigma = None,
    markersize = 6,
    show=True
    )








