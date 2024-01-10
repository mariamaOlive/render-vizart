import pandas as pd
#import plotly_express as px
import plotly.graph_objects as go

def preprocessoDados():

    dfList = []
    dfList.append(pd.read_json('data/artistas/andy-warhol.json', orient='records'))
    dfList.append(pd.read_json('data/artistas/frida-kahlo.json', orient='records'))
    dfList.append(pd.read_json('data/artistas/sandro-botticelli.json', orient='records'))
    dfList.append(pd.read_json('data/artistas/vincent-van-gogh.json', orient='records'))
    dfList.append(pd.read_json('data/artistas/pablo-picasso.json', orient='records'))
    dfList.append(pd.read_json('data/artistas/piet-mondrian.json', orient='records'))

    df = pd.concat(dfList, ignore_index=True)
    df[df.duplicated(['artistName'], keep=False)]
    df = df[df['genre']!='sketch and study']
    df = df[df['tags'].notna()]
    df = df[df['completitionYear'].notna()]
    df = df[df['genre'].notna()]
    df = df[df['style'].notna()]
    
    return df


def func_genero(artista = 'van Gogh Vincent '):
    df = preprocessoDados()

    dfVis = pd.DataFrame({'count' :  df[df['artistName']==artista].groupby(['genre','completitionYear'])['genre'].size().unstack(fill_value=0).stack()}).reset_index()
    top10 = df[df['artistName']==artista]['genre'].value_counts()[:10].index.to_list()
    dfVis = dfVis[dfVis['genre'].isin(top10)]


    x=dfVis['completitionYear'].unique()
    x.sort()

    generos = dfVis['genre'].unique()
    #paletaCores = ['#f44336', '#e91e63', '#9c27b0', '#673ab7', '#3f51b5', '#2196f3', '#ffeb3b','#009688', '#ffc107','#03a9f4','#8bc34a','#ff9800','#00bcd4','#cddc39','#ff5722', '#f44336', '#e91e63' ]
    paletaCores = ['#636EFA', '#EF553B', '#00CC96', '#AB63FA', '#FFA15A', '#19D3F3', '#FF6692', '#B6E880', '#FF97FF', '#FECB52']
    fig = go.Figure()

    for i, genero in zip(range(0, len(generos)), generos):      
        dfGenero = pd.DataFrame(dfVis[dfVis['genre']==genero])
        dfGenero.sort_values(by='completitionYear', inplace=True)
        y = dfGenero['count'].to_list()
        fig.add_trace(go.Scatter(
            x=x, y=y,
            #hoverinfo='x+y',
            hovertemplate = 'Proporção: %{y:.2f}%',#'Ano: %{x}<br>Proporção: %{y:.2f}%'
            mode='lines',
            opacity=0.5,
            line=dict(width=0.5, color=paletaCores[i]),
            fillcolor = paletaCores[i],
            stackgroup='one', # define stack group
            groupnorm='percent', 
            name = genero
    ))
    
    titulo='Gêneros mais populares ao longo dos anos'
    eixox='Ano'
    eixoy='Proporção dos gêneros'
    legenda='Gênero'
    fig.update_layout(
        title=titulo,
        xaxis_title=eixox,
        yaxis_title=eixoy,
        yaxis_range=(0, 100),
        hovermode='x',
        legend_title=legenda,
        font=dict(
            family="Courier New, monospace",
            size=18,
            color="RebeccaPurple"
        )
    )

    if artista == 'Picasso Pablo':
        fig.update_layout(xaxis_range=(1890, 1972))

    return fig
    # fig.update_layout(yaxis_range=(0, 100))
    # fig.show()