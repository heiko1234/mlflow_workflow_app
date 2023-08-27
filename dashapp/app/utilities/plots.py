

from plotly.subplots import make_subplots
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import numpy as np


try:
    from dashapp.app.utilities.nelson import apply_rules, rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8

except Exception:
    from app.utilities.nelson import apply_rules, rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8


# plotly graphic for quality control with plotly go , outlier detection, values outside of 3 standard deviations or limits are colored red



def control_chart(data, y_name, xlabel= None, title = "Controlchart", lsl = None, usl = None, outliers = True, annotations = True, lines = True, nelson=True, mean = None, sigma = None, markersize = 6, showlegend= False, show=False):
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
        showlegend (bool, optional): Defaults to False.
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

    if lsl is not None:
        abs_min_x = min([min_data, lsl, (mean_data - 3*sigma_data)])
    else:
        abs_min_x = min([min_data, (mean_data - 3*sigma_data)])

    if usl is not None:
        abs_max_x = max([max_data, usl, (mean_data + 3*sigma_data)])
    else:
        abs_max_x = max([max_data, (mean_data + 3*sigma_data)])

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

    if (usl is None) and (lsl is None):
        try:
            if usl < lsl:
                print(f"use usl: {usl} and lsl: {lsl}")
                # usl, lsl = lsl, usl
                raise ValueError("usl must be greater than lsl")
        except:
            pass


    # TODO add marginal
    # fig = make_subplots(rows=2, cols=1, row_heights=[0.25, 0.75])

    fig = go.Figure()

    # red areas for out of control
    # lsl
    if lsl is not None:
        fig.add_hline(y=float(lsl), line_color="red")
        y0 = abs_min_x-plot_expansion
        y1 = lsl
        fig.add_hrect(y0=y0, y1=y1, fillcolor="red", opacity=0.1)

    # usl
    if usl is not None:
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
            
    fig.update_layout(showlegend=showlegend)   # showlegend default = False
    
    fig.update_layout(yaxis_range=[abs_min_x-plot_expansion, abs_max_x+plot_expansion])

    if show:
        fig.show()

    else:
        return fig






def control_chart_marginal(data, y_name, xlabel= None, title = "Controlchart", lsl = None, usl = None, outliers = True, annotations = True, lines = True, nelson=True, mean = None, sigma = None, markersize = 6, showlegend= False, show=False):
    
    fig2 = control_chart(
        data=data,
        y_name=y_name,
        xlabel= xlabel,
        title = title,
        lsl = lsl,
        usl = usl,
        outliers = outliers,
        annotations = annotations,
        lines = lines,
        nelson=nelson,
        mean = mean,
        sigma = sigma,
        markersize = markersize,
        showlegend= showlegend,
        show=False)
    
    # rule base analysis
    data1 = data.loc[rule1(original=data[y_name]), y_name]
    data2 = data.loc[rule2(original=data[y_name]), y_name]
    data3 = data.loc[rule3(original=data[y_name]), y_name]
    data4 = data.loc[rule4(original=data[y_name]), y_name]
    data5 = data.loc[rule5(original=data[y_name]), y_name]
    data6 = data.loc[rule6(original=data[y_name]), y_name]
    data7 = data.loc[rule7(original=data[y_name]), y_name]
    data8 = data.loc[rule8(original=data[y_name]), y_name]
    
    data_sum = [data1, data2, data3, data4, data5, data6, data7, data8]

    fig = make_subplots(rows=2, cols=1, row_heights=[0.25, 0.75], vertical_spacing=0.025, shared_xaxes=True)
    
    for i in range(len(data_sum)):
        
            data_i = data_sum[i]
    
            rule_name = f"rule {int(i+1)}"

            fig.add_trace(go.Box(
                x=data_i.index,
                marker_symbol='line-ns-open',
                # marker size
                marker_size=12,
                # marker thickness
                marker_line_width=3,
                marker_color='violet',
                boxpoints='all',
                jitter=0,
                fillcolor='rgba(255,255,255,0)',
                line_color='rgba(255,255,255,0)',
                hoveron='points',
                name = rule_name,
                # name=data_i.name
            ),
            row=1, col=1)

    for i in range(len(fig2.data)):
        fig.add_trace(fig2.data[i], row=2, col=1)

    for j in range(len(fig2.layout.annotations)):
        fig.add_annotation(fig2.layout.annotations[j], row=2, col=1)
        
    for z in range(len(fig2.layout.shapes)):
        fig.add_shape(fig2.layout.shapes[z], row=2, col=1)
    


    fig.update_yaxes(range=[fig2.layout.yaxis.range[0], fig2.layout.yaxis.range[1]], row=2, col=1)
    
    if showlegend==True:
        fig.update_layout(showlegend=True)
    else:
        fig.update_layout(showlegend=False)

    if show==True:
        fig.show()
    else:
        return fig




def validation_plot(df_original, df_predicted): 

    try:

        fig_output = make_subplots(rows=2, cols=1, row_heights=[0.75, 0.25], vertical_spacing=0.025, shared_xaxes=True)


        # Main plot
        fig_output.add_trace(go.Scatter(x=df_original.index, y=df_original, mode='markers', marker=dict(color='blue', size = 12), name='original'), row=1, col=1)
        fig_output.add_trace(go.Scatter(x=df_predicted.index, y=df_predicted, mode='markers', marker=dict(color='red', size = 12), name='prediction'), row=1, col=1)

        # Residuals
        diff = df_original - df_predicted
        fig_output.add_trace(go.Scatter(x=diff.index, y=diff, mode='markers', marker=dict(color='black', size = 12), name='diff'), row=2, col=1)
        fig_output.update_layout(title='Original vs. Predicted Values', xaxis_title='Time', yaxis_title='Index')

    except Exception as e:
        print(e)
        fig_output = None

    return fig_output





# data = pd.DataFrame()

# data["x"] = np.random.normal(0, 1, 50)
# data["y"] = np.random.normal(0, 1, 50)
# # random labels, not repeated, 1000
# data["text"] = np.random.choice(list("ABCDEFGHIJ"), 50, replace=True)
# data["text2"] = np.random.choice(list("ABCDEFGHIJ"), 50, replace=True)


# data


# control_chart(
#     data=data,
#     y_name="y",
#     usl=3,
#     lsl=-3,
#     xlabel="text",
#     outliers=True,
#     nelson=True,
#     annotations=True,
#     lines=True,
#     mean = None,
#     sigma = None,
#     markersize = 6,
#     show=True
#     )


# # https://github.com/heiko1234/data_science_tutorials/blob/main/polymer_process_improvement/source/control_chart.py

# # add phasis to control chart
# # https://plotly.com/python/marginal-plots/

# # https://stackoverflow.com/questions/70952672/plotly-plot-with-multiple-marginal


# import plotly.express as px


# fig = px.scatter(
#     data,
#     x=data.index,
#     y="y",
#     color=["text","text2"],     # "text",
#     # facet_col="text",
#     marginal_x="rug"
#     )

# fig.show()




