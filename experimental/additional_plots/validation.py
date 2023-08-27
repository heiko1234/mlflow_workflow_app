



from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import os


# how to give several options for a parameter in a function?
# give several options for a variable in a function on modue 



def plot_validation(df_original, df_predicted, mode="scatter"): 


    if mode == "scatter":
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df_original.index, y=df_original, mode='lines', name='original'))
        fig.add_trace(go.Scatter(x=df_predicted.index, y=df_predicted, mode='lines', name='predicted'))
        fig.update_layout(title='Original vs. Predicted Values', xaxis_title='Time', yaxis_title='Value')
        return fig


    elif mode == "hist":
        fig = go.Figure()
        fig.add_trace(go.Histogram(x=df_original, name='original'))
        fig.add_trace(go.Histogram(x=df_predicted, name='predicted'))
        fig.update_layout(title='Original vs. Predicted Values', xaxis_title='Time', yaxis_title='Value')
        return fig
    
    elif mode == "qq":
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df_original, y=df_predicted, mode='markers', marker=dict(color='blue', size = 12)))
        fig.update_layout(title='Original vs. Predicted Values', xaxis_title='Original', yaxis_title='Predicted')
        return fig



df = pd.DataFrame()

df["Yield"] = [44.0, 43.0, 46.0, 40.1, 42.2]
df["BioMaterial1"]=[5.5, 4.5, 3.5, 1.0, 6.0]
df["BioMaterial2"]=[9.5, 9, 5, 10, 12]
df["ProcessValue1"] = [20, 15, 10, 9, 2]


df["Yield validation"] = [44.2, 43.1, 45.9, 40.2, 42.1]


df

fig =plot_validation(df["Yield"], df["Yield validation"], mode="scatter")
fig.show()


fig =plot_validation(df["Yield"], df["Yield validation"], mode="hist")
fig.show()



fig =plot_validation(df["Yield"], df["Yield validation"], mode="qq")
fig.show()




# fig = make_subplots(rows=2, cols=1, row_heights=[0.25, 0.75], vertical_spacing=0.025, shared_xaxes=True)

# row=1, col=1





diff = df["Yield"] - df["Yield validation"]



fig = go.Figure()
fig.add_trace(go.Scatter(x=diff.index, y=diff, mode='markers', marker=dict(color='blue', size = 12), name='diff'))
fig.update_layout(title='Original vs. Predicted Values', xaxis_title='Time', yaxis_title='Value')

fig.show()






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





fig =validation_plot(df["Yield"], df["Yield validation"])
fig.show()


fig = None


df_original = df["Yield"]
df_predicted = df["Yield validation"]


