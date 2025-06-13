# Importa a biblioteca Matplotlib para criar os gráficos
# pip install matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


try:
    print("Obtendo dados...")
    ENDERECO_DADOS = "https://www.ispdados.rj.gov.br/Arquivos/BaseDPEvolucaoMensalCisp.csv"

    # Buscar a base de dados CSV online do site ISP (Instituto de Segurança Pública)
    # encoding='iso-8859-1' - Codificação dos caracteres com acentuação
    # outras opções: utf-8, iso-8859-1, latin1, cp1252
    # encodings principais: https://docs.python.org/3/library/codecs.html#standard-encodings
    df_ocorrencias = pd.read_csv(ENDERECO_DADOS, sep=';', encoding='iso-8859-1')

    # Demilitando somente as variáveis do Exemplo01: munic e roubo_veiculo
    df_ocorrencias = df_ocorrencias[['munic', 'roubo_veiculo']]

    # Totalizar roubo de veiculo por municipio (agrupar e somar)
    # reset_index(), traz de volta os índices que numera as colunas, pois se
    # perdem nesta operação
    df_roubo_veiculo = df_ocorrencias.groupby('munic').sum(['roubo_veiculo']).reset_index()

    # Printando as linhas iniciais com o método head() apenas para ver se os dados
    # foram obtidos corretamente
    print(df_roubo_veiculo.head())

except Exception as e:
    print(f"Erro ao obter dados: {e}")
    exit()


# Inicando a obtenção das medidas fundamentadas em estatística descritiva
try:
    print('Obtendo informações sobre padrão de roubo de veículos...')

    # Numpy
    # Uso do ARRAY
    # Array faz parte da biblioteca numpy
    # Array é uma estrutura de dados que armazena uma coleção de dados
    # https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html
    # pip install numpy
    # import numpy as np
    # NumPy significa numerical python e tem como objetivo adicionar suporte
    # para arrays e matrizes multidimensionais, juntamente com uma grande
    # coleção de funções matemáticas de alto nível.
    # Uso do array significa ganho computacional
    array_roubo_veiculo = np.array(df_roubo_veiculo['roubo_veiculo'])

    # Obtendo média de roubo_veiculo
    media_roubo_veiculo = np.mean(array_roubo_veiculo)

    # Obtendo mediana de roubo_veiculo
    # Mediana é o valor que divide a distribuição em duas partes iguais
    # (50% dos dados estão abaixo e 50% acima)
    mediana_roubo_veiculo = np.median(array_roubo_veiculo)

    # Distânicia entre média e mediana
    # A distância entre a média e a mediana é uma medida de assimetria
    # A distância é obtida dividindo a diferença entre a média e a mediana
    # pela mediana
    # Se a distância for pequena, a distribuição é simétrica
    # Se a distância for grande, a distribuição é assimétrica
    # A distância é dada em porcentagem
    # Exemplo: 0.1 significa 10%
    # Se a distância for menor que 0.1, a distribuição tende a ser simétrica
    # Se a distância for maior que 0.1 e menor que 0.25, a distribuição tende
    # a ser assimétrica moderada. Pode ser que a média esteja sofrendo 
    # influência de valores extremos. Se a distância for maior que 0.25, a
    # distribuição tende a ser assimétrica forte. A tendência é, que nestes 
    # caso, a média esteja sofrendo influência de valores extremos.
    distancia = abs((media_roubo_veiculo-mediana_roubo_veiculo) / mediana_roubo_veiculo)

    # Medidas de tendência central
    # Se a média for muito diferente da mediana, distribuição é assimétrica. 
    # Não tende a haver um padrão e pode ser, que existam outliers (valores discrepantes)
    # Se a média for próxima (25%) a mediana, distribuição é simétrica. Neste 
    # caso, tende a haver um padrão
    # print('\nMedidas de tendência central: ')
    # print(30*'-')
    # print(f'Média de roubo de veículos: {media_roubo_veiculo}')
    # print(f'Mediana de roubo de veículos: {mediana_roubo_veiculo}')
    # print(f'Distância entre média e mediana: {distancia:.3f}')


    # Quartis
    # Os quartis são os valores que dividem a distribuição em 4 partes iguais.
    # O primeiro quartil (Q1) é o valor que divide a distribuição em 25% e 75%.
    # O segundo quartil (Q2) é o valor que divide a distribuição em 50% e 50%.
    # O terceiro quartil (Q3) é o valor que divide a distribuição em 75% e 25%.
    # O quartil é uma medida de posição que indica a posição de um valor em relação
    # a uma distribuição.
    
    # OBS: O método weibull é o método padrão, mas NÃO é necessário passá-lo
    # como parâmetro ao calcular os quartis.
    # Podemos emos usar o método 'linear' ou 'hazen' também.
    # A sintaxe pode ser assim, sem os métodos:
    # q1 = np.quantile(array_roubo_veiculo, 0.25)
    # q2 = np.quantile(array_roubo_veiculo, 0.50)
    # q3 = np.quantile(array_roubo_veiculo, 0.75)
    q1 = np.quantile(array_roubo_veiculo, 0.25, method='weibull') # Q1 é 25% 
    q2 = np.quantile(array_roubo_veiculo, 0.50, method='weibull') # Q2 é 50% (mediana)
    q3 = np.quantile(array_roubo_veiculo, 0.75, method='weibull') # Q3 é 75%

    # print('\nMedidas de posição: ')
    # print(30*'-')
    # print(f'Q1: {q1}')
    # print(f'Q2: {q2}')
    # print(f'Q3: {q3}')

    # print("\nMedidas de Dispersão: ")
    # print(30*"-")
    # medidas de dispersão são estatísticas que medem a variabilidade ou a dispersão
    # da distribuição.
    # A amplitude total é a diferença entre o maior e o menor valor de
    # uma distribuição.
    # Serve para identificar a variabilidade dos dados. Quanto maior a
    # amplitude, maior a variabilidade. Quanto mais perto do zero, menor
    # a variabilidade.
    maximo = np.max(array_roubo_veiculo)
    minimo = np.min(array_roubo_veiculo)
    amplitude_total = maximo - minimo

    # OBTENDO OS MUNÍCIPIOS COM MAIORES E MONORES NÚMEROS DE ROUBOS DE VEÍCULOS
    # Filtramos os registros do DataFrame df_roubo_veiculo para achar os municípios
    # com menores e maiores números de roubos de veículos.
    df_roubo_veiculo_menores = df_roubo_veiculo[df_roubo_veiculo['roubo_veiculo'] < q1]
    df_roubo_veiculo_maiores = df_roubo_veiculo[df_roubo_veiculo['roubo_veiculo'] > q3]

    print('\nMunicípios com Menores números de Roubos: ')
    print(70*'-')
    print(df_roubo_veiculo_menores.sort_values(by='roubo_veiculo', ascending=True))
    print('\nMunicípios com Maiores números de Roubos:')
    print(45*'-')
    print(df_roubo_veiculo_maiores.sort_values(by='roubo_veiculo', ascending=False))

    # ##### DESCOBRIR OUTLIERS #########
    # IQR (Intervalo interquartil)
    # q3 - q1
    # É a amplitude do intervalo dos 50% dos dados centrais
    # Ela ignora os valores extremos.
    # Não sofre a interferência dos valores extremos.
    # Quanto mais próximo de zero, mais homogêneo são os dados.
    # Quanto mais próximo do q3, mais heterogêneo são os dados.
    iqr = q3 - q1

    # Limite superior
    # Vai identificar os outliers acima de q3
    limite_superior = q3 + (1.5 * iqr)

    # Limite inferior
    # Vai identificar os outliers abaixo de q1
    limite_inferior = q1 - (1.5 * iqr)

    # print('\nLimites - Medidas de Posição')
    # print(45*'-')
    # print(f'Limite inferior: {limite_inferior}')
    # print(f'Limite superior: {limite_superior}')

    # PRINTANDO AS MEDIDAS
    print('\nPRINTANDO AS MEDIDAS: ')
    print(30*'-')
    print(f'Limite Inferior: {limite_inferior}')
    print(f'Mínimo: {minimo}')
    print(f'1º Quartil: {q1}')
    print(f'2º Quartil: {q2}')  # Mediana
    print(f'3º Quartil: {q3}')
    print(f'IQR: {iqr}')
    print(f'Máximo: {maximo}')
    print(f'Limite Superior: {limite_superior}')
    
    print('\nOUTRAS AS MEDIDAS: ')
    print(30*'-')
    print(f'Amplitude Total: {amplitude_total}')
    print(f'Média: {media_roubo_veiculo:.3f}')
    print(f'Mediana: {mediana_roubo_veiculo}')
    print(f'Distância Média e Mediana: {distancia:.4f}')
    

    # #### OUTLIERS
    # Obtendo os ouliers inferiores
    # Filtrar o dataframe df_roubo_veiculo para o munics com roubo de veículo
    # abaixo limite inferior (OUTLIERS INFERIORES)
    df_roubo_veiculo_outliers_inferiores = df_roubo_veiculo[df_roubo_veiculo['roubo_veiculo'] < limite_inferior]
    
    # Obtendo os ouliers superiores
    # Filtrar o dataframe df_roubo_veiculo para o munics com roubo de veículo
    # acima de limite superior (OUTLIERS SUPERIORES)
    df_roubo_veiculo_outliers_superiores = df_roubo_veiculo[df_roubo_veiculo['roubo_veiculo'] > limite_superior]

    print('\nMunicípios com outliers inferiores: ')
    print(45*'-')
    if len(df_roubo_veiculo_outliers_inferiores) == 0:
        print('Não existem outliers inferiores!')
    else:
        print(df_roubo_veiculo_outliers_inferiores.sort_values(by='roubo_veiculo', ascending=True))

    print('\nMunicípios com outliers superiores: ')
    print(45*'-')
    if len(df_roubo_veiculo_outliers_superiores) == 0:
        print('Não existe outliers superiores!')
    else:
        print(df_roubo_veiculo_outliers_superiores.sort_values(by='roubo_veiculo', ascending=False))

except Exception as e:
    print(f'Erro ao obter informações sobre padrão de roubo de veículos: {e}')
    exit()


# Plotando Gráfico de Barras
# Barras e Colunas (barh e bar)
try:
    # Cria uma figura com 1 linha e 2 colunas de subgráficos (side by side)
    # figsize define o tamanho da figura total
    fig, ax = plt.subplots(1, 2, figsize=(18, 6))
    

    # OUTLIERS INFERIORES
    # Verifica se existem outliers inferiores
    if not df_roubo_veiculo_outliers_inferiores.empty:
        # Ordena os dados de forma crescente pelo número de roubos
        dados_inferiores = df_roubo_veiculo_outliers_inferiores.sort_values(by='roubo_veiculo', ascending=True)
        
        # Cria gráfico de barras horizontais com os municípios e seus valores
        ax[0].barh(dados_inferiores['munic'], dados_inferiores['roubo_veiculo'])
    
    else:
        # Caso não haja outliers inferiores, exibe os 10 municípios que obtiveram menos roubos (bootom 10)
        dados_inferiores = df_roubo_veiculo_menores.sort_values(by='roubo_veiculo', ascending=True).head(10)

        # ax[0].text(0.5, 0.5, 'Sem Outliers Inferiores', ha='center', va='center', fontsize=12)
        barras = ax[0].bar(dados_inferiores['munic'], dados_inferiores['roubo_veiculo'], color='black')
        ax[0].bar_label(barras, label_type='edge', padding=3, fontsize=8)
        ax[0].tick_params(axis='x', rotation=75, labelsize=8)
        # Define o título do subplot
        ax[0].set_title('Menores Roubos')
        # Remove os marcadores dos eixos x e y
        ax[0].set_xticks([])
        ax[0].set_yticks([])

        # ##### VISUAL ######
        # Rótulo no final das barras e com tam 8
        # barras = ax[0].bar(dados_inferiores['munic'], dados_inferiores['roubo_veiculo'], color='green')
        # ax[0].bar_label(barras, label_type='edge', padding=3, fontsize=8)
        # # rotaciona o eixo x para melhorar a visualização
        # ax[0].tick_params(axis='x', rotation=75, labelsize=8)
 
    # OUTLIERS SUPERIORES
    # Verifica se existem outliers superiores
    if not df_roubo_veiculo_outliers_superiores.empty:
        # Ordena os dados de forma crescente
        dados_superiores = df_roubo_veiculo_outliers_superiores.sort_values(by='roubo_veiculo', ascending=True)

        # Cria o gráfico de barras horizontais com os municípios e seus valores
        # ax[1].barh(dados_superiores['munic'], dados_superiores['roubo_veiculo'], color='black')
        # Define o título e o rótulo do eixo x
        ax[1].set_title('Outliers Superiores')
        ax[1].set_xlabel('Total Roubos de Veículos')

        # ###### "VISUAL" #####
        # Rótulo de dados 0 casas decimais, edge "final da barra", tamanho 8 a 1 padding "distância"
        barras = ax[1].barh(dados_superiores['munic'], dados_superiores['roubo_veiculo'], color='black')
        ax[1].bar_label(barras, fmt='%.0f', label_type='edge', fontsize=8, padding=1)  
        # Tamanho do conteúdo do eixo Vertical "Y"
        ax[1].tick_params(axis='y', labelsize=8)

    else:
        # Caso não haja outliers superiores, exibe uma mensagem centralizada
        ax[1].text(0.5, 0.5, 'Sem outliers superiores', ha='center', va='center', fontsize=12)

        # Define o título do subplot
        ax[1].set_title('Outliers Superiores')

        # Remove os marcadores dos eixos x e y
        ax[1].set_xticks([])
        ax[1].set_yticks([])

    # Ajusta automaticamente os elementos do layout para não se sobreporem
    plt.tight_layout()

    # Exibe os gráficos
    plt.show()

except Exception as e:
    print(f'Erro ao plotar {e}')