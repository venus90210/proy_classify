import pandas as pd

def get_data():
    """
    Descarga los datos de transacciones desde múltiples fuentes JSON en AWS S3,
    los consolida en un único DataFrame de pandas y añade una columna 'source'
    para identificar el origen de cada registro.
    
    Returns:
        pandas.DataFrame: Un DataFrame con todos los datos consolidados.
                          Retorna un DataFrame vacío si no se puede cargar ningún dato.
    """
    data_sources = {
        "C026": "https://dataanaliticaunal.s3.us-east-2.amazonaws.com/deeplearning/100005.json",
        "C025": "https://dataanaliticaunal.s3.us-east-2.amazonaws.com/deeplearning/100004.json",
        "C001": "https://dataanaliticaunal.s3.us-east-2.amazonaws.com/deeplearning/100003.json",
        "P001": "https://dataanaliticaunal.s3.us-east-2.amazonaws.com/deeplearning/100002.json",
        "P047": "https://dataanaliticaunal.s3.us-east-2.amazonaws.com/deeplearning/100001.json",
    }

    list_of_dfs = []

    for name, url in data_sources.items():
        try:
            df = pd.read_json(url)
            df['source'] = name
            list_of_dfs.append(df)
        except Exception as e:
            print(f"Advertencia: No se pudo cargar el archivo desde {url}. Error: {e}")

    if not list_of_dfs:
        print("Error: No se pudo cargar ningún archivo de datos.")
        return pd.DataFrame()

    return pd.concat(list_of_dfs, ignore_index=True)

if __name__ == "__main__":
    main_df = get_data()
    if not main_df.empty:
        print("Primeras 5 filas del DataFrame consolidado:")
        print(main_df.head())
        print("\nInformación del DataFrame:")
        main_df.info()
