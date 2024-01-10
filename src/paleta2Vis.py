import pandas as pd
from pandas.core.frame import DataFrame
import plotly.graph_objects as go
#from colormap import rgb2hex, hex2rgb, rgb2hsv
#from PIL import ImageColor

class Paleta2Vis:

    def __init__(self):
        self.selecaoAtiva = False
        self.ano = 0
    

    # Carrega dados e retorn o dataframe para a visualizacao
    def loadData(self,nomeArtista):
        df = pd.read_csv(f'data/vis-paleta2/paleta_anos_{nomeArtista}.csv')
        df['selecionado'] = False
        return df


    def calcularCordenadas(self, dfPaletaAnos):
        x = list(range(1, 11)) * len(dfPaletaAnos['completitionYear'].unique())
        dfPaletaAnos['ordemVis'] = x
        return list(dfPaletaAnos[['completitionYear','ordemVis','hex','selecionado']].to_records(index=False))


    def calculateCordenadasSelecao(self, dfPaletaAnos, ano):
        copyDf = pd.DataFrame(dfPaletaAnos)
        x = list(range(1, 11)) * len(copyDf['completitionYear'].unique())
        copyDf['ordemVis'] = x

        copyDf.loc[copyDf['completitionYear'] == ano, 'selecionado'] = True
        retorno = list(copyDf[['completitionYear','ordemVis','hex','selecionado']].to_records(index=False))
        return retorno

    # Cria a visualizacao do plotly
    def getPaletaPorAno(self, nomeArtista):
        dfPaletaAnos = self.loadData(nomeArtista)
        coordenadas = self.calcularCordenadas(dfPaletaAnos)
        return self.gerarFigura(coordenadas)

    #Criar visualizacao com click
    def getPaletaPorAnoSelected(self,nomeArtista, ano):
    
        dfPaletaAnos = self.loadData(nomeArtista)
        if(self.selecaoAtiva):
            self.ano = ano
            coordenadas = self.calculateCordenadasSelecao(dfPaletaAnos, ano)
        else:
            self.ano = 0
            coordenadas = self.calcularCordenadas(dfPaletaAnos)
            
        return self.gerarFigura(coordenadas)


    def gerarFigura(self,coordenadas):
        fig = go.Figure()
        if (len(coordenadas)/10)<55:
            tamanho_paleta = 21
        else :
            tamanho_paleta = 11

        for x, y, color, selecionado in coordenadas:
            
            #cor_rgb = ImageColor.getcolor(color, "RGB")
            opacity = 1
            if(self.selecaoAtiva):
                opacity = 1 if selecionado else .4

            fig.add_trace(
                go.Scatter(
                    name = '',
                    mode='markers',
                    x=[x],
                    y=[y],
                    hovertemplate = 'Year: %{x}<br>Color: %{text}',#'Ano: %{x}<br>RGB: %{cor}',
                    text = [color],
                    #text = [cor_rgb], #se quiser o hexa é só usar [color]
                    #text = ['Custom text {}'.format(i + 1) for i in range(5)],
                    marker_symbol='square',
                    marker=dict(
                        color= color,
                        size=tamanho_paleta,
                        opacity=opacity#,
                        #line=dict(width=1,
                        #color='#E5E5E5')
                    ),
                    showlegend=False
                )
            )

        titulo='Color palette along the years'
        eixox='Year'
        eixoy='Colors'
        fig.update_layout(
            title=titulo,
            xaxis_title=eixox,
            yaxis_title=eixoy,
            #yaxis_visible=False, 
            yaxis_showticklabels=False,
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(
                family="Courier New, monospace",
                size=18,
                color="#232023"
            ),
            clickmode='event'
        )


        return fig
