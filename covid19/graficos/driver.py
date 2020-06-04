from CovidPorEstado import CovidPorEstado
from helper import ESTADOS, save
import schedule

def main():

    schedule.every(4).hours.do(job)

    while True:
        schedule.run_pending()

    return 0


def job():
    save("HIST_PAINEL_COVIDBR.xlsx")
    embed_html_todos_estados_bar()


def embed_html_todos_estados_bar():

    from bokeh.embed import components
    import io
    from jinja2 import Template
    from bokeh.resources import INLINE
    from bokeh.util.browser import view

    corona = CovidPorEstado()

    graficos = {}

    for estado in ESTADOS:
        plot = corona.plot_bar_mortes_dia_movel(estado)
        graficos[estado] = plot

    script, div = components(graficos)

    template = Template('''<!DOCTYPE html>
    <html lang="en">
        <head>
            <meta charset="utf-8">
            <title>Bokeh Scatter Plots</title>
            {{ resources }}
            {{ script }}
            <style>
                .embed-wrapper {
                    display: flex;
                    justify-content: space-evenly;
                }
            </style>
        </head>
        <body>

            {% for key in div.keys() %}
                <div class="embed-responsive">
                    <p> {{ key }}: </p>
                    {{ div[key] }}
                </div>
            {% endfor %}

        </body>
    </html>
    ''')

    resources = INLINE.render()

    filename = 'embed_multiple.html'

    html = template.render(resources=resources,
                        script=script,
                        div=div)

    with io.open(filename, mode='w', encoding='utf-8') as f:
        f.write(html)

    view(filename)

    return 0


main()
