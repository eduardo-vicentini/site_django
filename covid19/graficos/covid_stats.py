from covid_helpers import ESTADOS

# Recebe nome do estado e devolve dicionario dia: obitos
def mortes_dia(dict_df, estado):

    df = dict_df[estado]
    # O máximo do estado é dado pelo valor acumulado de todos os municipios
    # ou seja, o número de mortos no estado todo
    df = df.groupby('data')['obitosAcumulado'].max()

    morte_por_dia = {}
    datas = df.keys()
    
    for i in range(1, len(datas)):
        morte_por_dia[datas[i]] = df[datas[i]] - df[datas[i-1]]

    return morte_por_dia

# Media movel de mortes nos ultimos sete dias para um estado
def mortes_movel(dicionario):

    dates = [i for i in dicionario.keys()]
    mortes = [i for i in dicionario.values()]
    response = {}

    for i in range(6, len(dates)):

        temp_mortes_dia = mortes[(i-6):(i+1)]
        response[dates[i]] = round(sum(temp_mortes_dia) / len(temp_mortes_dia))

    return response

def mortes_milhao(dict_df, estado):
    
    df = dict_df[estado]
    # O máximo do estado é dado pelo valor acumulado de todos os municipios
    # ou seja, o número de mortos no estado todo
    df = df.groupby('data')['obitosAcumulado'].max()

    morte_por_milhao = {}
    datas = df.keys()
    
    for i in range(0, len(datas)):
        morte_por_milhao[datas[i]] = df[datas[i]] * 1000000 / ESTADOS[estado]

    return morte_por_milhao

# Media movel de mortes nos ultimos sete dias para um estado
def mortes_milhao_movel(dict_df, estado):

    dicionario = mortes_milhao(dict_df, estado)
    response = mortes_movel(dicionario)

    return response
