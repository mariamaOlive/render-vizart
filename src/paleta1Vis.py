import pandas as pd
import plotly.graph_objects as go

# Carrega dados e retorn o dataframe para a visualizacao
def loadData(nomeArtista):
    return pd.read_csv(f'data/vis-paleta1/{nomeArtista}-area.csv')

def loadPaletaCores(nomeArtista):
    return pd.read_csv(f'data/paletas/paleta_{nomeArtista}.csv')


# Cria a visualizacao do plotly
def getPaletaGeral(nomeArtista):
    dfVis = loadData(nomeArtista)
    paletaCores = loadPaletaCores(nomeArtista)

    x=dfVis.columns
    x=x.to_list()
    x=[int(float(i)) for i in x]
    fig = go.Figure()

    freqAnosArray = dfVis.values

    for index in range(len(freqAnosArray)):

        fig.add_trace(go.Scatter(
            name='',
            x=x, y=freqAnosArray[index],
            hovertemplate = 'Ano: %{x}<br>Proporção: %{y:.2f}%',
            mode='lines',
            line=dict(width=0.5, color=paletaCores['hex'][index]),
            fillcolor = paletaCores['hex'][index],
            stackgroup='one',
            groupnorm='percent' # sets the normalization for the sum of the stackgroup
        ))

    titulo='Paleta de cores ao longo dos anos'
    eixox='Ano'
    eixoy='Proporção das cores'
    #legenda='Cores'
    fig.update_layout(
        title=titulo,
        xaxis_title=eixox,
        yaxis_title=eixoy,
        #legend_title=legenda,
        showlegend=False,
        xaxis_type='category',
        font=dict(
            family="Courier New, monospace",
            size=18,
            color="RebeccaPurple"
        ),
        yaxis=dict(
            type='linear',
            range=[1, 100],
            ticksuffix='%'))

    
    

    return fig