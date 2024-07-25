import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import time

# Caminho dos arquivos Excel
path = os.path.dirname(__file__)

# Carregar os dados dos arquivos Excel
colaboradores_df = pd.read_excel(os.path.join(path, 'colaboradores.xlsx'))
metas_df = pd.read_excel(os.path.join(path, 'meta.xlsx'))
gestores_df = pd.read_excel(os.path.join(path, 'gestores.xlsx')) if os.path.exists(os.path.join(path, 'gestores.xlsx')) else pd.DataFrame(columns=['id', 'nome', 'area', 'password'])

# Função para salvar os dados de volta nos arquivos Excel
def save_to_excel(dataframe, filename):
    dataframe.to_excel(f'{path}/{filename}', index=False)

# Função de Login e Cadastro de Gestores
def login_cadastro_gestor():
    global gestores_df  # Declarar global no início da função

    st.title('Login e Cadastro de Gestores')

    login_tab, cadastro_tab = st.tabs(["Login", "Cadastro"])

    with login_tab:
        st.subheader('Login')
        login_nome = st.text_input('Nome', key='login_nome')
        login_password = st.text_input('Senha', type='password')
        login_button = st.button('Login')
        login_nome = login_nome.strip()
        login_password = login_password.strip()

        
        if login_button:
            gestor = gestores_df[(gestores_df['nome'].str.strip() == login_nome) & (gestores_df['password'].str.strip() == login_password)]
            if not gestor.empty:
                st.session_state['gestor_logado'] = gestor.iloc[0].to_dict()
                st.success('Login realizado com sucesso!')
                #st.rerun()
            else:
                st.error('Nome ou senha incorretos.')

    with cadastro_tab:
        st.subheader('Cadastro')
        cadastro_nome = st.text_input('Nome', key='cadastro_nome')
        cadastro_area = st.text_input('Área', key='cadastro_area')
        cadastro_password = st.text_input('Senha (Deve conter números e letras)', type='password', key='cadastro_password')
        cadastro_button = st.button('Cadastrar')

        if cadastro_button:
            if cadastro_nome and cadastro_area and cadastro_password:
                new_gestor = pd.DataFrame([{'id': len(gestores_df) + 1, 'nome': cadastro_nome, 'area': cadastro_area, 'password': cadastro_password}])
                gestores_df = pd.concat([gestores_df, new_gestor], ignore_index=True)
                save_to_excel(gestores_df, 'gestores.xlsx')
                st.success('Gestor cadastrado com sucesso!')
                #st.rerun()
            else:
                st.error('Por favor, preencha todos os campos.')

# Página de Cadastro de Colaboradores
def cadastrar_colaborador():
    global colaboradores_df  # Declarar global no início da função

    st.title('Cadastro de Colaboradores')

    # Usar `st.form` para criar um formulário que pode ser resetado
    with st.form(key='cadastro_colaborador_form'):
        nome = st.text_input('Nome')
        funcao = st.text_input('Função')
        gestor = st.text_input('Gestor', value=st.session_state['gestor_logado']['nome'], disabled=True)
        area = st.text_input('Área', value=st.session_state['gestor_logado']['area'], disabled=True)
        
        submit_button = st.form_submit_button('Cadastrar Colaborador')

        if submit_button:
            if nome and funcao and gestor and area:
                new_colaborador = pd.DataFrame([{'id': len(colaboradores_df) + 1, 'nome': nome, 'funcao': funcao, 'gestor': gestor, 'area': area}])
                colaboradores_df = pd.concat([colaboradores_df, new_colaborador], ignore_index=True)
                save_to_excel(colaboradores_df, 'colaboradores.xlsx')
                # Limpar os campos (não diretamente possível, mas o formulário será reiniciado)
                st.success('Colaborador cadastrado!')
                #st.rerun()
            else:
                st.error('Por favor, preencha todos os campos.')

# Página de Cadastro de Metas
def cadastrar_meta():
    global metas_df  # Declarar global no início da função

    st.title('Cadastro de Metas')

    colaboradores_gestor = colaboradores_df[colaboradores_df['gestor'] == st.session_state['gestor_logado']['nome']]
    colaborador_nome = st.selectbox('Selecionar Colaborador', colaboradores_gestor['nome'])
    colaborador_id = colaboradores_gestor[colaboradores_gestor['nome'] == colaborador_nome]['id'].values[0]

    nome_meta = st.text_input('Nome da Meta')
    descricao_meta = st.text_area('Descrição da Meta')
    prazo_meta = st.date_input('Prazo para Avaliação')

    if st.button('Cadastrar Meta'):
        if nome_meta and descricao_meta and prazo_meta:
            new_meta = pd.DataFrame([{'id': len(metas_df) + 1, 'colaborador_id': colaborador_id, 'nome_meta': nome_meta, 'descricao_meta': descricao_meta, 'prazo_meta': prazo_meta, 'porcentagem': 0}])
            metas_df = pd.concat([metas_df, new_meta], ignore_index=True)
            save_to_excel(metas_df, 'meta.xlsx')
            st.success('Meta cadastrada!')
            #st.rerun()

        else:
            st.error('Por favor, preencha todos os campos.')

# Página de Visualização e Dashboard
def dashboard_colaborador():
    st.title('Dashboard de Metas')

    colaboradores_gestor = colaboradores_df[colaboradores_df['gestor'] == st.session_state['gestor_logado']['nome']]
    colaborador_nome = st.selectbox('Selecionar Colaborador para Visualização', colaboradores_gestor['nome'])
    colaborador_id = colaboradores_gestor[colaboradores_gestor['nome'] == colaborador_nome]['id'].values[0]

    metas_colaborador = metas_df[metas_df['colaborador_id'] == colaborador_id]

    if not metas_colaborador.empty:
        st.write('Meta:')
        for idx, (_, meta) in enumerate(metas_colaborador.iterrows()):
            col1, col2 = st.columns(2)
            bg_color = "#f9f9f9" if idx % 2 == 0 else "#e0e0e0"  # Alternar cores de fundo

            with col1:
                st.markdown(f"""
                <div style="background-color: {bg_color}; padding: 10px; border-radius: 5px;">
                    <p><strong>Nome:</strong> {meta['nome_meta']}</p>
                    <p><strong>Descrição:</strong> {meta['descricao_meta']}</p>
                    <p><strong>Prazo:</strong> {meta['prazo_meta'].strftime('%d/%m/%Y')}</p>
                    <p><strong>Status:</strong> {meta['porcentagem']}%</p>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                nova_porcentagem = st.slider(f"Atualizar Status ({meta['nome_meta']})", 0, 100, meta['porcentagem'])
                if st.button(f'Atualizar {meta["nome_meta"]}'):
                    metas_df.loc[metas_df['id'] == meta['id'], 'porcentagem'] = nova_porcentagem
                    save_to_excel(metas_df, 'meta.xlsx')
                    st.success(f'Status da meta "{meta["nome_meta"]}" atualizada para {nova_porcentagem}%!')
                    st.rerun()

        col1, col2 = st.columns([3, 1])

        with col2:
            # Média das porcentagens das metas alcançadas

            media_porcentagens = metas_colaborador['porcentagem'].mean()
            col2.metric(label="Média das Metas Alcançadas", value=f"{media_porcentagens:.2f}%")

        # Usar um layout de coluna completa para centralizar o gráfico
        st.markdown("<div style='display: flex; justify-content: center;'>", unsafe_allow_html=True)
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=metas_colaborador['porcentagem'],
            theta=metas_colaborador['nome_meta'],
            fill='toself'
        ))
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )
            ),
            showlegend=False,
            width=700,  # Largura do gráfico
            height=700  # Altura do gráfico
        )

        st.plotly_chart(fig)
        st.markdown("</div>", unsafe_allow_html=True)


# Verificar se o gestor está logado
if 'gestor_logado' not in st.session_state:
    login_cadastro_gestor()
else:
    # Menu de navegação
    st.sidebar.title('Menu')
    menu = st.sidebar.radio('Escolha uma página', ['Login e Cadastro de Gestores', 'Cadastrar Colaborador', 'Cadastrar Meta', 'Dashboard'])

    if menu == 'Login e Cadastro de Gestores':
        login_cadastro_gestor()
    elif menu == 'Cadastrar Colaborador':
        cadastrar_colaborador()
    elif menu == 'Cadastrar Meta':
        cadastrar_meta()
    elif menu == 'Dashboard':
        dashboard_colaborador()