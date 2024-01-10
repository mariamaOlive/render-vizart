import pandas as pd
import plotly.express as px
#import plotly.graph_objects as go

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


def func_estilo(artista = 'van Gogh Vincent '):
    df = preprocessoDados()

    dfVis = pd.DataFrame({'count' :  df[df['artistName']==artista].groupby(['style','completitionYear'])['style'].size()}).reset_index()

    fig = px.bar(dfVis, x="completitionYear", y="count", color="style",labels={
                     "completitionYear": "Year",
                     "count": "Number of works",
                     "style": "Art Movement"
                 },
                #hover_name="Estilo", hover_data="style",
                title="Art Movement in time")

    fig.update_layout(
    #font_family="Courier New, monospace",
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(
            family="Courier New, monospace",
            size=18,
            color="#232023"
        )
    )
    
    return fig
    # fig.update_layout(yaxis_range=(0, 100))
    # fig.show()