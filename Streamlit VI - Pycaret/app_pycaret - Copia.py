import pandas as pd
import streamlit as st
from io import BytesIO
from pycaret.classification import load_model, predict_model
from sklearn.metrics import confusion_matrix, accuracy_score

# Função para converter o df para excel
@st.cache_data
def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    writer.save()
    processed_data = output.getvalue()
    return processed_data

# Função principal da aplicação
def main():
    # Configuração inicial da página da aplicação
    st.set_page_config(
        page_title='PyCaret',
        layout="wide",
        initial_sidebar_state='expanded'
    )

    # Título principal da aplicação
    st.write("""## Escorando o modelo gerado no PyCaret""")
    st.markdown("---")
    
    # Botão para carregar arquivo na aplicação
    st.sidebar.write("## Suba o arquivo")
    data_file_1 = st.sidebar.file_uploader("Bank Credit Dataset", type=['csv', 'ftr'])

    # Verifica se há conteúdo carregado na aplicação
    if data_file_1 is not None:
        df_credit = pd.read_feather(data_file_1)
        df_credit = df_credit.sample(50000)

        # Tratamento dos dados
        st.write("### Pré-processamento de Dados")
        
        # Aqui você pode adicionar qualquer tratamento adicional necessário
        
        # Carregar modelo treinado
        model_saved = load_model('lightgbm_model')

        # Aplicar o modelo ao conjunto de dados tratado
        predict = predict_model(model_saved, data=df_credit)

        # Exibir a taxa de acerto em um "card" bonito
        st.write("### Taxa de Acerto")
        y_true = df_credit['mau']
        y_pred = predict['prediction_label']
        accuracy = accuracy_score(y_true, y_pred)
        st.metric(label="Accuracy", value=f"{accuracy:.2%}")

        # Exibir a matriz de confusão
        st.write("### Matriz de Confusão")
        cm = confusion_matrix(y_true, y_pred)
        st.text("True Positives: {}".format(cm[0, 0]))
        st.text("False Positives: {}".format(cm[0, 1]))
        st.text("False Negatives: {}".format(cm[1, 0]))
        st.text("True Negatives: {}".format(cm[1, 1]))

        # Exibir tabela com previsões
        st.write("### Tabela com Previsões")
        st.write(predict)

        # Botão de download do Excel para as predições
        st.write("### Download das Predições")
        df_to_download = predict.copy()
        df_xlsx = to_excel(df_to_download)
        st.download_button(label='📥 Download',
                            data=df_xlsx ,
                            file_name= 'predictions.xlsx')

if __name__ == '__main__':
    main()






