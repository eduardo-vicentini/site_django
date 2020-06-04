import covid_stats as cs


# Auxilia para criar morte por dia
def plot_bar_mortes_dia(dict_df, estado):
    dicionario = cs.mortes_dia(dict_df, estado)
    return plot_bar_mortes(dicionario)

# Auxilia para criar mortes por dia, mas utilizando a media movel
def plot_bar_mortes_dia_movel(dict_df, estado):
    dicionario = cs.mortes_dia(dict_df, estado)
    dicionario = cs.mortes_movel(dicionario)
    return plot_bar_mortes(dicionario)

# Faz os gráficos de mortes por dia em barras verticais para um estado
def plot_bar_mortes(dicionario, mode="bar"):
    from bokeh.plotting import figure
    from bokeh.models import ColumnDataSource
    from datetime import datetime as dt
    from bokeh.models import HoverTool
    from bokeh.models import DatetimeTickFormatter, DaysTicker, FuncTickFormatter
    from numpy import arange


    # Gerar os datetime com a formatação da string "YYYY-MM-DD"
    datas = [dt(int(i[:4]), int(i[5:7]), int(i[8:])) for i in dicionario.keys()]
    mortes_dia = [i for i in dicionario.values()]

    source = ColumnDataSource(data={
        'datas': datas,
        'mortes_dia': mortes_dia,
    })

    if mode == "bar":
        # Width bem grande porque em datetime a barra seria na unidade de microsec
        # Ficaria muito fina para o hover
        p = figure(
        x_axis_type='datetime', plot_width=1200,
        title="Medias Móveis dos Últimos Sete Dias da Quantidade Óbitos"
        )

        p.vbar(x="datas", top="mortes_dia", width=60000000, source=source)

    elif mode == "line":

        p = figure(
            x_axis_type='datetime', plot_width=1200, y_axis_type="log", y_range=(0.001, 10**3),
            title="Medias Móveis dos Últimos Sete Dias da Quantidade de Óbitos por milhão"
        )

        p.line(x="datas", y="mortes_dia", line_width=1, source=source)

    else:
        return("Opção para mode inválida")

    p.xaxis.axis_label = "Data"
    p.yaxis.axis_label = "Óbitos"

    p.add_tools(HoverTool(
        tooltips=[
            ( 'Mes/Dia',   '@datas{%d/%m}' ),
            ( 'Obitos',  '@mortes_dia' )
        ],

        formatters={
            '@datas': 'datetime',
        },

        # Aparece tooltip sempre que estiver acima de uma barra
        mode='vline'
    ))
    
    # formatar o eixo x para aparecer dia/mes
    p.xaxis.formatter=DatetimeTickFormatter(
    hours=["%d/%m"],
    days=["%d/%m"],
    months=["%d/%m"],
    years=["%d/%m"],
    )   

    p.xaxis.ticker = DaysTicker(days=arange(1, 32))


    # Seleciona para aparecer a label de cinco em cinco dias
    # utilizando apenas o dia/mes
    p.xaxis.formatter = FuncTickFormatter(code="""
        let date = new Date(tick)
        let day = date.getUTCDate(date)
        let month = date.getUTCMonth(date)
        let r = day + "/" + month
        if ( day%5 == 0 ) { return r }
        else { return "" }
    """)


    p.xaxis.major_label_orientation = 1
    p.y_range.start = 0
    p.x_range.range_padding = 0.1
    p.xgrid.grid_line_color = None
    p.axis.minor_tick_line_color = None
    p.outline_line_color = None

    return p


# Grafico da media movel de mortes para um dado estado por milhao de habitante
def plot_mortes_milhao(dict_df, estado):
    morte_por_milhao = cs.mortes_milhao(dict_df, estado)

    return plot_bar_mortes(morte_por_milhao, mode="line")

# Auxilia para criar mortes por milhão, mas utilizando a media movel
def plot_mortes_milhao_movel(dict_df, estado):
    morte_por_milhao = cs.mortes_milhao(dict_df, estado)
    dicionario = cs.mortes_movel(morte_por_milhao)
    return plot_bar_mortes(dicionario)