


# TODO: mae marginal plots

# https://community.plotly.com/t/rug-plot-without-plotly-express/38752/2
# https://stackoverflow.com/questions/70952672/plotly-plot-with-multiple-marginal 


import pandas as pd




from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px


from dashapp.app.utilities.nelson import apply_rules, rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8


from dashapp.app.utilities.plots import control_chart


df = pd.read_parquet("data/ChemicalManufacturingProcess.parquet")

data=df

data
list(data.columns)



y_name="Yield"


data1 = data.loc[rule1(original=data[y_name]), y_name]
data2 = data.loc[rule2(original=data[y_name]), y_name]
data3 = data.loc[rule3(original=data[y_name]), y_name]
data4 = data.loc[rule4(original=data[y_name]), y_name]
data5 = data.loc[rule5(original=data[y_name]), y_name]
data6 = data.loc[rule6(original=data[y_name]), y_name]
data7 = data.loc[rule7(original=data[y_name]), y_name]
data8 = data.loc[rule8(original=data[y_name]), y_name]


data1
data2
data3
data4
data5
data6
data7
data8

data_sum = [data1, data2, data3, data4, data5, data6, data7, data8]


data2t = pd.DataFrame(data2, columns=[y_name])
data2t

# fig2 = px.ecdf(df, x="total_bill", color="sex", markers=True, lines=False, marginal="rug")
fig2 = px.ecdf(data2t, x=data2t.index, markers=True, lines=False, marginal="rug")

fig2.show()

fig = make_subplots(rows=2, cols=1, row_heights=[0.25, 0.75], vertical_spacing=0.1, shared_xaxes=True)  



# fig.add_trace(go.Box(
#    x=x, 
#    marker_symbol='line-ns-open', 
#    marker_color='blue',
#    boxpoints='all',
#    jitter=0,
#    fillcolor='rgba(255,255,255,0)',
#    line_color='rgba(255,255,255,0)',
#    hoveron='points',
#    name='rug'
#), row=1, col=1)





fig = go.Figure()

for i in range(len(data_sum)):
    
    data_i = data_sum[i]
    
    rule_name = f"rule {int(i+1)}"
    
    print(rule_name)

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
        name = f"rule {int(i+1)}"
        # name=data_i.name
    ))


fig.show()



fig2 = control_chart(
    data=df,
    y_name=y_name,
    xlabel= None,
    title = "Controlchart",
    lsl = None,
    usl = None,
    outliers = True,
    annotations = True,
    lines = True,
    nelson=True,
    mean = None,
    sigma = None,
    markersize = 6,
    show=False)


fig2

fig2.show()

fig2.data[0]

fig2.data
fig2.layout

fig2.layout.yaxis.range[0]
fig2.layout.yaxis.range



fig = make_subplots(rows=2, cols=1, row_heights=[0.25, 0.75], vertical_spacing=0.025, shared_xaxes=True)  

# fig.add_trace(fig2.data[1],row=1, col=1)

for i in range(len(data_sum)):
    
    data_i = data_sum[i]
    
    rule_name = f"rule {int(i+1)}"
    
    print(rule_name)

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
        name = f"rule {int(i+1)}"
        # name=data_i.name
    ),
    row=1, col=1)

for i in range(len(fig2.data)):
    fig.add_trace(fig2.data[i], row=2, col=1)

for j in range(len(fig2.layout.annotations)):
    fig.add_annotation(fig2.layout.annotations[j], row=2, col=1)
    
for z in range(len(fig2.layout.shapes)):
    fig.add_shape(fig2.layout.shapes[z], row=2, col=1)
    

# fig.update_layout(yaxis_range=[fig2.layout.yaxis.range], row=2, col=1)
# update yaxis range for plot in row 2 col 1
fig.update_yaxes(range=[fig2.layout.yaxis.range[0], fig2.layout.yaxis.range[1]], row=2, col=1) 

fig.update_layout(showlegend=False) 


fig.show()






fig3 = control_chart(
    data=df,
    y_name=y_name,
    xlabel= None,
    title = "Controlchart",
    lsl = None,
    usl = None,
    outliers = True,
    annotations = True,
    lines = True,
    nelson=True,
    mean = None,
    sigma = None,
    markersize = 6,
    show=False)


fig3.show()




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
    
            print(rule_name)
    
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
                name = f"rule {int(i+1)}"
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

    if show==True:
        fig.show()
    else:
        return fig







# # ###################


import pandas as pd

from dashapp.app.utilities.plots import (
    control_chart,
    control_chart_marginal
)


df = pd.read_parquet("data/ChemicalManufacturingProcess.parquet")

data=df

# list(data.columns)

#['Yield', 'BiologicalMaterial01', 'BiologicalMaterial02', 'BiologicalMaterial03', '
# BiologicalMaterial04', 'BiologicalMaterial05', 'BiologicalMaterial06', 'BiologicalMaterial07', 
# 'BiologicalMaterial08', 'BiologicalMaterial09', 'BiologicalMaterial10', 'BiologicalMaterial11', 
# 'BiologicalMaterial12', 'ManufacturingProcess01', 'ManufacturingProcess02', 'ManufacturingProcess03', 
# 'ManufacturingProcess04', 'ManufacturingProcess05', 'ManufacturingProcess06', 'ManufacturingProcess07', 
# 'ManufacturingProcess08', 'ManufacturingProcess09', 'ManufacturingProcess10', 'ManufacturingProcess11', 
# 'ManufacturingProcess12', 'ManufacturingProcess13', 'ManufacturingProcess14', 'ManufacturingProcess15', 
# 'ManufacturingProcess16', 'ManufacturingProcess17', 'ManufacturingProcess18', 'ManufacturingProcess19', 
# 'ManufacturingProcess20', 'ManufacturingProcess21', 'ManufacturingProcess22', 'ManufacturingProcess23', 
# 'ManufacturingProcess24', 'ManufacturingProcess25', 'ManufacturingProcess26', 'ManufacturingProcess27', 
# 'ManufacturingProcess28', 'ManufacturingProcess29', 'ManufacturingProcess30', 'ManufacturingProcess31', 
# 'ManufacturingProcess32', 'ManufacturingProcess33', 'ManufacturingProcess34', 'ManufacturingProcess35',
# 'ManufacturingProcess36', 'ManufacturingProcess37', 'ManufacturingProcess38', 'ManufacturingProcess39', 
# 'ManufacturingProcess40', 'ManufacturingProcess41', 'ManufacturingProcess42', 'ManufacturingProcess43', 
# 'ManufacturingProcess44', 'ManufacturingProcess45']


my_fig = control_chart_marginal(
    data=df,
    y_name="Yield",
    xlabel= None,
    title = "Controlchart",
    lsl = None,
    usl = None,
    outliers = True,
    annotations = True,
    lines = True,
    nelson=True,
    mean = None,
    sigma = None,
    markersize = 6,
    showlegend= False,
    show=False
    )

my_fig.show()


