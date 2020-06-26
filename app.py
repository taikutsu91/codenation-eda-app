import streamlit as st
import pandas as pd
pd.options.plotting.backend = "plotly"
import numpy as np
import seaborn as sns
import plotly.express as px
from PIL import Image
cmap = 'ggplot2'

codenation = Image.open('codenation.png')


def main ():
    st.sidebar.title('O que você gostaria de ver?')
    opcao = ['Análise Estatística', 'Gráficos', 'Referências']
    choice = st.sidebar.radio(' ', opcao)

    st.sidebar.title('Data')
    st.sidebar.info(
        """
        Caso não tenha um arquivo csv por perto, você pode baixar por aqui:\n
        [Titanic](http://kopasite.net/up/1/titanic.csv)\n
        [Iris](http://kopasite.net/up/0/iris.csv)\n
        [Tips](http://kopasite.net/up/0/tips.csv)\n
        """
    )
    st.sidebar.title('Créditos')
    st.sidebar.info("""
    Feito por Raul.\n
    [github](https://github.com/taikutsu91)
    [linkedin](https://www.linkedin.com/in/raul-avelino-959b16149)\n
    Duvidas ou informações:
    raul1991@prontonmail.com ou 
    ravels1991@gmail.com\n
    Para mais informações do projeto ver Referências.
    """)
    if choice == 'Análise Estatística':
        st.header('Análise Estatística')
        st.subheader("""
        Para começar carregue um arquivo csv.
        """)
        data = st.file_uploader(' ', type=['csv'])
        if data is not None:
            df = pd.read_csv(data)
            st.write(df.head())
            aux = pd.DataFrame({'colunas': df.columns, 'tipos': df.dtypes})
            col_num = list(aux[aux['tipos'] != 'object']['colunas'])
            col_obj = list(aux[aux['tipos'] == 'object']['colunas'])
            colunas = list(df.columns)
            hue = df.columns[df.nunique() < 10].values.tolist()

            if st.checkbox('Tamanho DataFrame'):
                st.write('Número de linhas', df.shape[0])
                st.write('Número de colunas', df.shape[1])

            if st.checkbox('Mostrar colunas'):
                colunas = list(df.columns)
                st.write(colunas)


            if st.checkbox('Mostrar tipos das colunas'):
                st.write(df.dtypes)

            if st.checkbox('Mostrar Sumário'):
                st.write(df.describe())

            if st.checkbox('Mostrar % valores nulos'):
                st.write(df.isnull().mean() * 100)

            if st.checkbox('Escolha uma coluna númerica'):
                coluna_num = st.selectbox('Coluna', col_num)
                st.write('Média', df[coluna_num].mean())
                st.write('Moda', df[coluna_num].mode()[0])
                st.write('Desvio Padrão', df[coluna_num].std())
                st.write('Maior Valor', df[coluna_num].max())
                st.write('Menor Valor', df[coluna_num].min())
                st.write('% datos faltantes', (df[coluna_num].isnull().mean() * 100))
                st.write('Valores únicos na coluna', df[coluna_num].nunique())

    elif choice == 'Gráficos':
        st.header('Visualização dos Dados.')
        st.subheader('Para começar carregue um arquivo csv.')
        st.info(""" Alguns gráficos terão uma opção para selecionar a cor.
                A opção cor vai determinar qual coluna no dataframe deve ser usada para codificação de cores, 
                adicionando o parâmetro cor, indica para o gráfico que você deseja colorir os dados de maneira diferente com base na coluna selecionada.
                """)
        data = st.file_uploader(' ', type=['csv'], key='graficos')
        if data is not None:
            df = pd.read_csv(data)
            st.write(df.head())
            aux = pd.DataFrame({'colunas': df.columns, 'tipos': df.dtypes})
            col_num = list(aux[aux['tipos'] != 'object']['colunas'])
            col_obj = list(aux[aux['tipos'] == 'object']['colunas'])
            colunas = list(df.columns)
            hue = df.columns[df.nunique() < 10].values.tolist()

            st.info("""
            Caso seu dataframe seja muito grande, você pode selecionar um sample do mesmo,
             escolhendo qual a porcentagem dos dados que serão usadas.
            """)
            pct = st.slider("Sample size % :", int(0), int(100), int(100))
            frame = df.sample(frac=(pct/100))

            if st.checkbox('Tamanho do DataFrame'):
                st.write('Número de linhas', frame.shape[0])
                st.write('Número de colunas', frame.shape[1])



            if st.checkbox('Scatter Plot'):

                eixo_x = st.selectbox('Selecione Eixo X', col_num, key='unique')
                eixo_y = st.selectbox('Selecione Eixo Y', col_num, key='unique')
                cor = st.selectbox('Cor', hue, key='unique')
                fig = px.scatter(frame, x=eixo_x, y=eixo_y, color=cor, template=cmap,
                                 title=f'Scatter Plot {eixo_x} x {eixo_y}')
                st.plotly_chart(fig, use_container_width=True)



            if st.checkbox('Histogram'):
                st.info("""
                Caso o parâmetro cor tenha algum dado faltante o mesmo será preenchido,
                 automaticamente com a moda da coluna selecionada.
                """
                        )
                coluna_num = st.selectbox('Selecione Eixo X', col_num, key='coluna_num')
                color = st.selectbox('Cor', hue, key='color')
                fig1 = px.histogram(frame, x=coluna_num,
                                    color=frame[color].fillna(frame[color].mode()), histfunc='sum',
                                    title=f'Histogram {coluna_num}')
                st.plotly_chart(fig1, use_container_width=True)

            if st.checkbox('Counts'):
                st.info("""
                Este gráfico retorna, os valores únicos do dataframe em porcetagem,
                com base na coluna selecionada.
                
                """)
                value = st.selectbox('Selecione uma coluna', colunas, key='value')
                plot_value = frame[value].value_counts(normalize=True)
                fig = plot_value.plot(kind='bar', title=f'Count Coluna: {value}')
                st.plotly_chart(fig, use_container_width=True)

            if st.checkbox('Bar Plot'):
                cols = st.selectbox('Selecione uma coluna', colunas, key='cols')
                target = st.selectbox('Cor', hue, key='target')
                gb = pd.crosstab(frame[cols], frame[target])
                fig = gb.plot(kind='bar', title=f'Bar Plot {cols} x {target}')
                st.plotly_chart(fig, use_container_width=True)

            if st.checkbox('Violin Plot'):
                coluna_num1 = st.selectbox('Selecione o Eixo X', col_obj, key='coluna_num1')
                coluna_x1 = st.selectbox('Selecione o Eixo Y', col_num, key='coluna_x1')
                color1 = st.selectbox('Cor', hue, key='color1')
                fig = px.violin(frame, x=coluna_num1, y=coluna_x1, color=color1,
                                title=f'Violet Plot {coluna_num1} x {coluna_x1}')
                st.plotly_chart(fig, use_container_width=True)


            if st.checkbox('Box Plot'):
                coluna_num2 = st.selectbox('Selecione o Eixo X', col_obj, key='coluna_num2')
                coluna_x2 = st.selectbox('Selecione o Eixo Y', col_num, key='coluna_x2')
                color2 = st.selectbox('Cor', hue, key='color2')
                fig = px.box(frame, x=coluna_num2, y=coluna_x2, color=color2,
                             title=f'Box Plot {coluna_num2} x {coluna_x2}')
                st.plotly_chart(fig, use_container_width=True)

            if st.checkbox('Line Plot'):
                st.info("""
                Line Plot é normalmanete usado para medir variações atráves do tempo,
                caso seu dataframe não tenha uma coluna que seja datetime , não é recomendado o uso do Line Plot,
                use Scatter Plot ou Bar Plot.
                """)
                eixo_x2 = st.selectbox('Selecione o Eixo X', colunas, key='eixo_x2')
                eixo_y2 = st.selectbox('Selecione o Eixo Y', colunas, key='eixo_y2')
                fig = frame.plot(kind='line', x=eixo_x2, y=eixo_y2, title=f'Line Plot {eixo_x2} x {eixo_y2}')
                st.plotly_chart(fig, use_container_width=True)


            if st.checkbox('Heatmap'):
                metodo = st.selectbox('Selecione o Método de correlação',
                                      ['pearson', 'kendall', 'spearman'], key='metodo')
                corr = frame.corr(method=metodo)
                ax = sns.heatmap(corr, annot=True, fmt=".2f", cmap="YlGnBu")
                st.pyplot()

            if st.checkbox('Heatmap Colunas'):
                st.info("""Você pode selecionar quais colunas você quer usar para fazer seu heatmap.
                """)
                metodo1 = st.selectbox('Selecione o Método de correlação',
                                       ['pearson', 'kendall', 'spearman'], key='metodo1')

                cols = st.multiselect('Selecione colunas que serão usadas', col_num, key='cols')

                corr = frame[cols].corr(method=metodo1)
                ax = sns.heatmap(corr, annot=True, fmt=".2f", cmap="YlGnBu")
                st.pyplot()

    elif choice == 'Referências':
        st.image(codenation, width=800, format='PNG')
        st.header('Referências')
        st.write("""
        Esse projeto foi proposto pelo Professor [Túlio Souza](https://www.linkedin.com/in/tuliovieira/) da [Codenation](https://www.codenation.dev/), na semana 3 do Acelera Dev Data Science turma do meio do ano de 2020.
        Para saber mais sobre a codenation e seus "Aceleramentos" de carreira e ver o trabalho incrível que eles fazem, podem entra no [Site Codenation](https://www.codenation.dev/), [facebook](https://pt-br.facebook.com/dev.codenation) ou pelo
        [linkedin](https://br.linkedin.com/company/code-nation).
        """)
        st.subheader('Gráficos')
        st.write("""
        Alguns gráficos desse projeto foram feitos usando a biblioteca plotly e sua extensão para pandas.
        https://plotly.com/python/bar-charts/ \n
        https://plotly.com/python/pandas-backend/ \n
        
        Heatmap foi feito usando seaborn.\n
        https://seaborn.pydata.org/generated/seaborn.heatmap.html\n
        
        Os datasets no menu lateral foram arquivados no site kopasite.net, uma ótima forma de guardar arquivos curtos e com download simples.\n
        http://kopasite.net/upload
        
        Para informações adicionais do streamlit acesse: \n
        https://docs.streamlit.io/ \n
        https://www.streamlit.io/ \n
        
        Tips e iris data set foram retirados.\n
        https://github.com/mwaskom/seaborn-data\n
        Titanic data set.\n
        https://www.kaggle.com/c/titanic\n
        
        Deploy do projeto feito no heroku:\n
        https://www.youtube.com/watch?v=mQ7rGcE766k
        
        
        Obrigado por ver meu primeiro app e obrigado codenation pela oportunidade de aprender, qualquer dúvida manda um email.\n
        ravels1991@gmail.com ou raul1991@prontonmail.com
        """)

if __name__ == '__main__':
    main()

