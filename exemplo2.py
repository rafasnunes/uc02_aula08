import pandas as pd
import numpy as np
import matplotlib.pyplot as plt  # biblioteca de gráficos

try:
    ENDERECO_DADOS = "https://www.ispdados.rj.gov.br/Arquivos/BaseDPEvolucaoMensalCisp.csv"
    df_ocorrencia = pd.read_csv(ENDERECO_DADOS, sep=';', encoding='iso-8859-1')

    # Delimitando variáveis
    df_ocorrencia = df_ocorrencia[['munic', 'roubo_veiculo']]

    # Totalizando
    df_roubo_veiculo = df_ocorrencia.groupby('munic').sum(numeric_only=True).reset_index()
    print(df_roubo_veiculo.to_string())

except Exception as e:
    print(f"Erro de conexão: {e}")
    exit()

# Inicializando análise
try:
    print('Obtendo informações sobre padrão de roubos de veículos...')
    array_roubo_veiculo = np.array(df_roubo_veiculo['roubo_veiculo'])
    media_roubo_veiculo = np.mean(array_roubo_veiculo)
    mediana_roubo_veiculo = np.median(array_roubo_veiculo)
    distancia = abs((media_roubo_veiculo - mediana_roubo_veiculo) / mediana_roubo_veiculo)

    # Quartis
    q1 = np.quantile(array_roubo_veiculo, 0.25, method='weibull')
    q2 = np.quantile(array_roubo_veiculo, 0.50, method='weibull')
    q3 = np.quantile(array_roubo_veiculo, 0.75, method='weibull')

    # Medidas de dispersão
    print("\nMEDIDAS DE DISPERSÃO")
    print("~" * 67)
    maximo = np.max(array_roubo_veiculo)
    minimo = np.min(array_roubo_veiculo)
    amplitude_total = maximo - minimo

    # Menores roubos
    df_roubo_veiculo_menores = df_roubo_veiculo[df_roubo_veiculo['roubo_veiculo'] < q1]
    print('\nMunicípio com Menores números de Roubos')
    print(df_roubo_veiculo_menores.sort_values(by='roubo_veiculo', ascending=True))

    # Maiores roubos
    df_roubo_veiculo_maiores = df_roubo_veiculo[df_roubo_veiculo['roubo_veiculo'] > q3]
    print('\nMunicípios com Maior números de Roubos')
    print(df_roubo_veiculo_maiores.sort_values(by='roubo_veiculo', ascending=False))

    # Identificando outliers
    iqr = q3 - q1
    limite_superior = q3 + (1.5 * iqr)
    limite_inferior = q1 - (1.5 * iqr)

    print("\nMEDIDAS")
    print("~" * 67)
    print(f'Limite inferior: {limite_inferior}')
    print(f'Menor Valor: {minimo}')
    print(f'Q1: {q1}')
    print(f'Q2: {q2}')
    print(f'Q3: {q3}')
    print(f'IQR: {iqr}')
    print(f'Maior Valor: {maximo}')
    print(f'Limite superior: {limite_superior}')
    print(f'Média: {media_roubo_veiculo}')
    print(f'Mediana: {mediana_roubo_veiculo}')
    print(f'Distância média e mediana: {distancia:.3f}')

    # Descobrindo outliers
    df_outliers_superiores = df_roubo_veiculo[df_roubo_veiculo['roubo_veiculo'] > limite_superior]
    df_outliers_inferiores = df_roubo_veiculo[df_roubo_veiculo['roubo_veiculo'] < limite_inferior]

    print('\nOutliers Inferiores')
    if df_outliers_inferiores.empty:
        print('Não há outliers inferiores')
    else:
        print(df_outliers_inferiores.sort_values(by='roubo_veiculo', ascending=True))

    print('\nOutliers Superiores')
    if df_outliers_superiores.empty:
        print('Não há outliers superiores')
    else:
        print(df_outliers_superiores.sort_values(by='roubo_veiculo', ascending=False))

except Exception as e:
    print(f"Erro de processamento de dados: {e}")
    exit()

# Gráfico Boxplot
try:
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.boxplot(array_roubo_veiculo, vert=False, patch_artist=True,
               boxprops=dict(facecolor='lightblue'))
    plt.tight_layout()
    plt.show()

except Exception as e:
    print(f"Erro: {e}")
    exit()
