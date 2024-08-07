# ProMeta

## Descrição
O ProMeta é uma aplicação desenvolvida para facilitar a gestão de metas e o acompanhamento do desempenho de colaboradores dentro de uma organização. A aplicação permite o cadastro de gestores, colaboradores, definição de metas e o monitoramento das mesmas através de dashboards interativos.

## Funcionalidades
- **Cadastro de Gestores:** Permite o cadastro de gestores com nome, área e senha.
- **Login de Gestores:** Autenticação de gestores para acesso às funcionalidades da aplicação.
- **Cadastro de Colaboradores:** Gestores podem cadastrar colaboradores sob sua responsabilidade.
- **Cadastro de Metas:** Definição de metas específicas para cada colaborador, com descrição e prazo.
- **Dashboard de Metas:** Visualização e atualização do status das metas dos colaboradores, além de gráficos e métricas de acompanhamento.

## Tecnologias Utilizadas
- Python
- Streamlit
- Pandas
- Plotly

## Estrutura do Projeto
- **ProMeta.py:** Script principal que contém a lógica da aplicação.
- **colaboradores.xlsx:** Arquivo Excel com os dados dos colaboradores.
- **meta.xlsx:** Arquivo Excel com as metas definidas.
- **gestores.xlsx:** Arquivo Excel com os dados dos gestores.

## Como Executar
1. Clone o repositório:
    ```bash
    git clone https://github.com/seu-usuario/ProMeta.git
    cd ProMeta
    ```
2. Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```
3. Execute a aplicação:
    ```bash
    streamlit run ProMeta.py
    ```

## Exemplos de Uso
- **Cadastro de Gestores:** Os gestores podem ser cadastrados na aba "Cadastro de Gestores". Após o cadastro, é possível realizar o login para acessar as funcionalidades da aplicação.
- **Cadastro de Colaboradores:** Os gestores podem cadastrar colaboradores sob sua responsabilidade na aba "Cadastro de Colaboradores".
- **Cadastro de Metas:** As metas são definidas para cada colaborador na aba "Cadastro de Metas", onde é possível especificar o nome da meta, descrição e prazo.
- **Dashboard de Metas:** O dashboard permite a visualização e atualização do status das metas dos colaboradores, além de apresentar gráficos e métricas para acompanhamento.

## Contribuições
Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e enviar pull requests.

## Licença
Este projeto está licenciado sob a MIT License.
