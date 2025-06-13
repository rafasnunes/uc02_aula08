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
    df_roubo_veiculo_outliers_inferiores = df_roubo_veiculo[df_roubo_veiculo['roubo_veiculo'] < q1]
    print('\nMunicípio com Menores números de Roubos')
    print(df_roubo_veiculo_outliers_inferiores.sort_values(by='roubo_veiculo', ascending=True))

    # Maiores roubos
    df_roubo_veiculo_outliers_superiores = df_roubo_veiculo[df_roubo_veiculo['roubo_veiculo'] > q3]
    print('\nMunicípios com Maior números de Roubos')
    print(df_roubo_veiculo_outliers_superiores.sort_values(by='roubo_veiculo', ascending=False))

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
    # import matplotlib.pyplot as plt
    # fig, ax = plt.subplots(figsize=(10, 6))
    # ax.boxplot(array_roubo_veiculo, vert=False, showmeans=True)
    
    plt.subplots(2, 2, figsize=(16, 10))
    plt.suptitle('Análise de roubo de veículos no RJ') 

    # POSIÇÃO 01
    # BOXPLOT
    plt.subplot(2, 2, 1)  
    plt.boxplot(array_roubo_veiculo, vert=False, showmeans=True)
    plt.title("Boxplot dos Dados")

    # POSIÇÃO 02
    # MEDIDAS
    # Exibição de informações estatísticas
    plt.subplot(2, 2, 2)
    plt.title('Medidas Estatísticas')
    plt.text(0.1, 0.9, f'Limite inferior: {limite_inferior}', fontsize=10)
    plt.text(0.1, 0.8, f'Menor valor: {minimo}', fontsize=10) 
    plt.text(0.1, 0.7, f'Q1: {q1}', fontsize=10)
    plt.text(0.1, 0.6, f'Mediana: {mediana_roubo_veiculo}', fontsize=10)
    plt.text(0.1, 0.5, f'Q3: {q3}', fontsize=10)
    plt.text(0.1, 0.4, f'Média: {media_roubo_veiculo:.3f}', fontsize=10)
    plt.text(0.1, 0.3, f'Maior valor: {maximo}', fontsize=10)
    plt.text(0.1, 0.2, f'Limite superior: {limite_superior}', fontsize=10)

    plt.text(0.5, 0.9, f'Distância Média e Mediana: {distancia:.4f}', fontsize=10)
    plt.text(0.5, 0.8, f'IQR: {iqr}', fontsize=10)
    plt.text(0.5, 0.7, f'Amplitude Total: {amplitude_total}', fontsize=10)
    
    # POSIÇÃO 03
    # OUTLIERS INFERIORES
    plt.subplot(2, 2, 3)
    plt.title('Outliers Inferiores')
    # Se o DataFrame do outliers não estiver vazio
    if not df_roubo_veiculo_outliers_inferiores.empty:
        dados_inferiores = df_roubo_veiculo_outliers_inferiores.sort_values(by='roubo_veiculo', ascending=True) #crescente
        # Gráfico de Barras
        plt.barh(dados_inferiores['munic'], dados_inferiores['roubo_veiculo'])
    else:
        # Se não houver outliers
        plt.text(0.5, 0.5, 'Sem Outliers Inferiores', ha='center', va='center', fontsize=12)
        plt.title('Outilers Inferiores')
        plt.xticks([])
        plt.yticks([])
    
    # POSIÇÃO 04
    # OUTLIERS SUPERIORES
    plt.subplot(2, 2, 4)
    plt.title('Outliers Superiores')
    if not df_roubo_veiculo_outliers_superiores.empty:
        dados_superiores = df_roubo_veiculo_outliers_superiores.sort_values(by='roubo_veiculo', ascending=True)

        # Cria o gráfico e guarda as barras
        barras = plt.barh(dados_superiores['munic'], dados_superiores['roubo_veiculo'], color='black')
        # Adiciona rótulos nas barras
        plt.bar_label(barras, fmt='%.0f', label_type='edge', fontsize=8, padding=2)

        # Diminui o tamanho da fonte dos eixos
        plt.xticks(fontsize=8)
        plt.yticks(fontsize=8)

        plt.title('Outliers Superiores')
        plt.xlabel('Total Roubos de Veículos')    
    else:
        # Se não houver outliers superiores, exibe uma mensagem no lugar.
        plt.text(0.5, 0.5, 'Sem outliers superiores', ha='center', va='center', fontsize=12)
        plt.title('Outliers Superiores')
        plt.xticks([])
        plt.yticks([])

    # Ajusta os espaços do layout para que os gráficos não fiquem espremidos
    plt.tight_layout()
    # Mostra a figura com os dois gráficos
    plt.show()
    
except Exception as e:
    print(f'Erro ao plotar {e}')
    exit()