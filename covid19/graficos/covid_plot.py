import covid_stats as cs


# Auxilia para criar mortes por dia, mas utilizando a media movel
def plot_bar_mortes_dia_movel(dict_df, estado):
    dicionario = cs.mortes_dia(dict_df, estado)
    dicionario_media = cs.mortes_movel(dicionario)
    return plot_bar_mortes(dicionario, dicionario_media)

# Faz os gráficos de mortes por dia em barras verticais para um estado
def plot_bar_mortes(dicionario, dicionario_media):
    from bokeh.plotting import figure
    from bokeh.models import ColumnDataSource
    from datetime import datetime as dt
    from bokeh.models import HoverTool
    from bokeh.models import DatetimeTickFormatter, DaysTicker, FuncTickFormatter
    from numpy import arange


    # Gerar os datetime com a formatação da string "YYYY-MM-DD"
    datas = [dt(int(i[:4]), int(i[5:7]), int(i[8:])) for i in dicionario.keys()]
    mortes_dia = [i for i in dicionario.values()]

    datas_movel = [dt(int(i[:4]), int(i[5:7]), int(i[8:])) for i in dicionario_media.keys()]
    mortes_dia_movel = [i for i in dicionario_media.values()]

    source = ColumnDataSource(data={
        'datas': datas,
        'mortes_dia': mortes_dia,
    })

    source_movel = ColumnDataSource(data={
        'datas': datas_movel,
        'mortes_dia': mortes_dia_movel,
    })

    # Width bem grande porque em datetime a barra seria na unidade de microsec
    # Ficaria muito fina para o hover
    p = figure(
    x_axis_type='datetime', plot_width=600,
    title="Media dos Últimos Sete Dias da Quantidade Óbitos"
    )

    

    p.vbar(x="datas", top="mortes_dia", width=60000000, source=source)
    p.line(x="datas", y="mortes_dia", line_width=2, source=source_movel, line_color="orange")
    p.circle(x="datas", y="mortes_dia", source=source_movel, line_color="orange")


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

    pass

# Auxilia para criar mortes por milhão, mas utilizando a media movel
def plot_mortes_milhao_movel(dict_df, estado):
    morte_por_milhao = cs.mortes_milhao(dict_df, estado)
    dicionario = cs.mortes_movel(morte_por_milhao)
    pass


def plot_log_acumulado():
    p = figure(
            x_axis_type='datetime', plot_width=500, y_axis_type="log", y_range=(0.001, 10**3),
            title="Medias Móveis dos Últimos Sete Dias da Quantidade de Óbitos por milhão"
        )
    pass