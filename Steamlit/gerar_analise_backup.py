import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
from pathlib import Path

sns.set()  

def plota_pivot_table(df, value, index, func, ylabel, xlabel, opcao='nada'):
    if opcao == 'nada':
        pd.pivot_table(df, values=value, index=index,aggfunc=func).plot(figsize=[15, 5])
    elif opcao == 'unstack':
        pd.pivot_table(df, values=value, index=index,aggfunc=func).unstack().plot(figsize=[15, 5])
    elif opcao == 'sort':
        pd.pivot_table(df, values=value, index=index,aggfunc=func).sort_values(value).plot(figsize=[15, 5])
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    st.pyplot(fig=plt)
    return None

st.set_page_config(page_title = 'SINASC Rondônia',
                    page_icon='https://upload.wikimedia.org/wikipedia/commons/e/ea/Flag_map_of_Rondonia.png',
                    layout='wide')

st.title('Análise SINASC - Rondônia')
st.header('Explorando recursos streamlit')
st.subheader('Projeto EBAC - Cientista de dados')


# Obtém o caminho relativo da imagem em relação ao diretório do script
image_path = Path(__file__).with_name("mapa_rondonia.png").relative_to(Path.cwd())

# Exibe a imagem
st.image(str(image_path))


st.write('--------')



sinasc = pd.read_csv(r"C:\Users\Igor\Documents\GitHub\volta-zero\Steamlit\input_M15_SINASC_RO_2019.csv")

sinasc.DTNASC = pd.to_datetime(sinasc.DTNASC)

min_data = sinasc.DTNASC.min()
max_data = sinasc.DTNASC.max()


data_inicial = st.sidebar.date_input('Data inicial', 
                value = min_data,
                min_value = min_data,
                max_value = max_data)
data_final = st.sidebar.date_input('Data final', 
                value = max_data,
                min_value = min_data,
                max_value = max_data)    


st.sidebar.selectbox("Filtro - Sexo", sinasc["SEXO"].unique())

st.toggle("Usar para apenas liberar as analises finais caso esteja ligado")


sinasc  = sinasc[(sinasc['DTNASC'] <= pd.to_datetime(data_final)) & (sinasc['DTNASC'] >=pd.to_datetime(data_inicial) )]

plota_pivot_table(sinasc, 'IDADEMAE', 'DTNASC', 'mean', 'média idade mãe por data', 'data nascimento')
plota_pivot_table(sinasc, 'IDADEMAE', ['DTNASC', 'SEXO'], 'mean', 'media idade mae','data de nascimento','unstack')
plota_pivot_table(sinasc, 'PESO', ['DTNASC', 'SEXO'], 'mean', 'media peso bebe','data de nascimento','unstack')
plota_pivot_table(sinasc, 'PESO', 'ESCMAE', 'median', 'PESO mediano','escolaridade mae','sort')
plota_pivot_table(sinasc, 'APGAR1', 'GESTACAO', 'mean', 'apgar1 medio','gestacao','sort')





