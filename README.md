[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/7orQC0e0)
# Web Service REST com MongoDB

## ESTA É UMA APS EM DUPLA! Não pode ser individual.
Apenas um precisa entregar, porém os dois precisam ter commits no repositório.
Adicione o nome dos integrantes aqui no README.md.

Integrante 1:

Integrante 2:

## Aluguel de Bicicletas Compartilhadas com Histórico de Empréstimos

Com o avanço da economia compartilhada, cada vez mais empresas estão buscando soluções sustentáveis e econômicas que atendam às demandas da sociedade moderna. Uma dessas soluções é o aluguel de bicicletas compartilhadas, que tem ganhado popularidade em muitas cidades ao redor do mundo, oferecendo uma alternativa ecológica e saudável aos meios de transporte tradicionais.

Uma startup inovadora no ramo de aluguel de bicicletas contratou você para desenvolver um sistema de gerenciamento para sua operação. Eles precisam de um web service REST de nível 2 de Richardson que permita gerenciar usuários, bicicletas e empréstimos.

## Requisitos

### Usuários
- Cada usuário deve ter um nome (str), CPF (str) e data de nascimento (formato string mesmo, não precisa usar date).
- O CPF é único para cada usuário.
- O CPF não pode ser uma string vazia também.
- Todas as informações são obrigatórias. Se qualquer informação estiver faltando ao criar ou atualizar um usuário, o sistema deve retornar um status HTTP condizente.


### Bicicletas
- Cada bicicleta deve ter uma marca, modelo e a cidade onde está alocada.
- Todas as informações são obrigatórias. Se qualquer informação estiver faltando ao criar ou atualizar uma bicicleta, o sistema deve retornar um status HTTP condizente.
- Bicicleta precisa ter um status indicando se está disponível ou em uso: "disponivel" ou "em uso".



### Empréstimos
- Cada empréstimo relaciona uma bicicleta a um usuário.
- Este recurso deve ter o id do usuário que está alugando e o id da bicicleta que está sendo alugada e a data de quando foi alugada.
- Crie uma rota que receba o id da bicicleta e o id do usuario e registre o aluguel. Mas lembre-se que uma bicicleta que já está alugada, não pode ser alugada novamente. Restrição apenas para bicicleta e não para o usuário.
- Permita visualizar os empréstimos tanto selecionando um usuário quanto selecionando uma bicicleta, mostrando quando foi realizado o empréstimo.
- Registre o emprestimo e a devolução.

Para facilitar: implemente ler todos emprestimos, inserir e deletar um emprestimo.

## Rotas

- Para usuários.
    - Ler todos usuários (/usuarios)
    - Ler apenas um usuário dado um id (/usuarios/<id_usuario>)
    - Inserir um usuário (/usuarios)
    - Atualizar um usuário dado um id (/usuarios/<id_usuario>)
    - Deletar um usuário dado um id (/usuarios/<id_usuario>)
- Para bicicletas. 
    - Ler todas bicicletas (/bikes)
    - Ler apenas uma bicicleta dado um id (/bikes/<id_bike>)
    - Inserir uma bicicleta (/bikes)
    - Atualizar uma bicicleta dado um id (/bikes/<id_bike>)
    - Deletar uma bicicleta dado um id (/bikes/<id_bike>)
- Para empréstimos.
    - Ler todos emprestimos (mostrando apenas os ids - do usuário, da bicicleta e do emprestimo) (/emprestimos)
    - Inserir um emprestimo dado um id de usuario e id da bicicleta (/emprestimos/usuarios/<id_usuario>/bikes/<id_bike>)
    - Deletar um emprestimo dado um id de empréstimo (/emprestimos/<id_emprestimo>)

## Nível 2 de maturidade
- Garanta que seja utilizado os métodos HTTP corretos para cada operação
- Utilize corretamente os status code HTTP para um web service REST. Para facilitar a lista é: (200, 201, 400, 404 e 500)
- Utilize recurso nas rotas. Para facilitar, tem uma collection do Postman para vocês utilizarem.

---

## Etapa 1: Modelagem de Dados

### 1.1: Modelagem NoSQL
Crie a relação entre os documentos utilizando relação por embeeding documents no MongoDB.
- Utilize _embedding_ document para criar a relação entre os documentos: https://www.mongodb.com/basics/embedded-mongodb

## Etapa 2: Configuração do MongoDB

### 2.1: MongoDB Atlas e MongoDB Compass
Configure uma instância no MongoDB Atlas e crie as collections necessárias conforme os modelos definidos na etapa anterior. Utilize o MongoDB Compass para se conectar à sua instância no MongoDB Atlas.

**String de Conexão:**
Uma string de conexão é uma cadeia de caracteres que especifica informações sobre uma fonte de dados e os meios de se conectar a ela. É passada para o driver de conexão/gerenciador de banco de dados para iniciar uma sessão com o banco de dados. Uma string de conexão do MongoDB é composta por:
- Usuário: Um usuário válido na base de dados do MongoDB.
- Senha: A senha do usuário mencionado acima.
- Host: O endereço IP ou hostname onde o MongoDB está hospedado.
- Porta: A porta na qual o MongoDB está rodando (padrão é 27017).

Exemplo: `mongodb+srv://<user>:<password>@cluster0.mongodb.net/myFirstDatabase?retryWrites=true&w=majority`

### 2.2: Adicionando Registros
Utilize o MongoDB Compass para inserir alguns registros nas collections criadas.

## Etapa 3: Ambiente de Desenvolvimento e Conexão com MongoDB

### 3.1: Ambiente Virtual e Instalação de Pacotes
Antes de iniciar o desenvolvimento, crie um ambiente virtual para manter as dependências do projeto isoladas. Em seguida, instale o Flask e o PyMongo.

```bash
pip install Flask
pip install pymongo
pip install Flask-PyMongo
```

### 3.2: Conexão com MongoDB 

Para referência: 
- https://flask-pymongo.readthedocs.io/en/latest/
- https://pymongo.readthedocs.io/en/stable/tutorial.html


## Etapa 4: Desenvolvimento do Web Service REST com Flask e MongoDB

### 4.1: API REST

Desenvolva o web service em Flask, garantindo que os requisitos definidos no enunciado original sejam atendidos e utilizando o MongoDB como seu banco de dados.

### 4.2: Deploy no Render 

Faça o deploy do seu web service no Render e assegure que ele esteja se comunicando corretamente com o MongoDB Atlas.

## Etapa 5: Interface do Usuário

Crie um repositório separado para o desenvolvimento do Streamlit, deixe-o público e adicione o link aqui!
Link do repositório da interface:
Link de deploy do streamlit:

Desenvolva uma interface para o usuário para que ele consiga gerenciar os recursos do back-end. Desenvolvimento livre!