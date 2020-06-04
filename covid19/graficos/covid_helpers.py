
# Habitantes por estado
ESTADOS = {
    "AC": 881935, 
    "AL": 3337357, 
    "AP": 845731, 
    "AM": 4144597, 
    "BA": 14873064, 
    "CE": 9132078, 
    "DF": 3015268, 
    "ES": 4018650,
    "GO": 7018354, 
    "MA": 7075181,
    "MT": 3484466, 
    "MS": 2778986, 
    "MG": 21168791,
    "PA": 8602865, 
    "PB": 4018127, 
    "PR": 11433957, 
    "PE": 9557071, 
    "PI": 3273227, 
    "RJ": 17264943, 
    "RN": 3506853, 
    "RS": 11377239, 
    "RO": 1777225, 
    "RR": 605761, 
    "SC": 7164788, 
    "SP": 45919049, 
    "SE": 2298696, 
    "TO": 1572866}

# Carrega do banco de dados as informações
def load(path):
    import pandas as pd
    import sqlite3

    conn = sqlite3.connect(path)
    df = pd.read_sql_query("SELECT * FROM covid19", conn)
    conn.close()
    return df

# Abre excel e salva em um db
def save(path):     
    import sqlite3
    import pandas as pd
    
    df = pd.read_excel(path)

    conn = sqlite3.connect("covid.db")
    
    df.to_sql("covid19", conn, if_exists="replace")
    
    conn.close()

def df_dictdf():

    df = load("covid.db")

    # Dicionário de dataframes dos estados
    dict_df = {}
    for i in ESTADOS.keys():
        dict_df[i] = df.loc[df['estado'] == i]

    return (df, dict_df)