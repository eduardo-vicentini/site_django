import covid_plot as cp
from covid_helpers import ESTADOS, save, load, df_dictdf
import schedule
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
def main():

    job()
    # schedule.every(4).hours.do(job)

    # while True:
    #     schedule.run_pending()

    # return 0


def job():
    save(os.path.join(BASE_DIR, "HIST_PAINEL_COVIDBR.xlsx"))
    embed_html_todos_estados_bar()


def embed_html_todos_estados_bar():

    from bokeh.embed import components
    import io
    from jinja2 import Template
    from bokeh.resources import INLINE
    from bokeh.util.browser import view


    corona_df, corona_dictdf = df_dictdf()

    graficos = {}

    for estado in ESTADOS:
        plot = cp.plot_bar_mortes_dia_movel(corona_dictdf, estado)
        graficos[estado] = plot

    script, div = components(graficos)

    template = Template('''<!DOCTYPE html>
    <html lang="en">
        <head>
            <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css" 
            integrity="sha384-9aIt2nRpC12Uk9gS9baDl411NQApFmC26EwAOH8WgZl5MYYxFfc+NcPb1dKGj7Sk" crossorigin="anonymous">
            <meta charset="utf-8">
            <title>Covid-19s</title>
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
            <header>
                <nav class="navbar navbar-expand-lg navbar-dark bg-dark sticky-top">
                    <a class="navbar-brand" href="/covid19">Eduardo Vicentini</a>
                    <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarText" aria-controls="navbarText" aria-expanded="false" aria-label="Toggle navigation">
                    <span class="navbar-toggler-icon"></span>
                    </button>
                    <div class="collapse navbar-collapse" id="navbarText">
                    <ul class="navbar-nav flex-row ml-md-auto d-none d-md-flex">
                        <li class="nav-item">
                            <a class="nav-link" href="/">Home</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="/mediumcre">Blog</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="/projects">Projetos</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="/contact">Contato</a>
                        </li>
                    </ul>
                
                    </div>
                </nav>
            </header>
            <main>
            
            {% for key in div.keys() %}
                {% if loop.index0 % 2 == 0 %}
                    <div class="d-flex flex-row justify-content-center">
                {% endif %}
                    <div class="p-2">
                        <div class="card mb-4">
                            <div class="card-body">
                                <h3> {{ key }} </h3>
                                {{ div[key] }}
                            </div>
                        </div>
                    </div>
                {% if loop.index0 % 2 != 0 %}
                    </div>
                {% endif %}
        
            {% endfor %}
            </main>
        
            <footer>
                <nav class="navbar navbar-expand-lg navbar-light bg-light">
                    <div class="mx-auto">
                        <a href="https://www.linkedin.com/in/eduardo-vicentini-4ab081192/" class="navbar-brand"><ion-icon name="logo-linkedin" size="large"></a>
                        <a href="https://github.com/eduardo-vicentini" class="navbar-brand"><ion-icon name="logo-github" size="large"></a>
                        <a href="/contact" class="navbar-brand"><ion-icon name="mail-outline" size="large"></ion-icon></a>edudiasvicentini@hotmail.com
                    </div>
                    
                </nav>
                <script src="https://unpkg.com/ionicons@5.0.0/dist/ionicons.js"></script>

            </footer>
        </body>
    </html>
    ''')

    resources = INLINE.render()

    filename = os.path.join(BASE_DIR, '../../templates/covid19/covid.html')

    html = template.render(resources=resources,
                        script=script,
                        div=div)

    with io.open(filename, mode='w', encoding='utf-8') as f:
        f.write(html)

    view(filename)

    return 0


main()
