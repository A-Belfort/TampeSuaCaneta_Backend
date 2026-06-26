# TampeSuaCaneta_Backend
Backend em **Python (Flask)** do aplicativo **TampeSuaCaneta**, responsável por receber a localização do usuário e retornar a lista de unidades de saúde com distribuição gratuita de preservativos no Recife, ordenadas por proximidade.

## 📱 Sobre o projeto

Este backend é a contraparte do app mobile feito em Expo/React Native. Ele consome os dados abertos da Prefeitura do Recife (via API CKAN do [Dados Recife](https://dados.recife.pe.gov.br/)), calcula a distância entre o usuário e cada unidade de saúde, e devolve a lista ordenada da mais próxima para a mais distante.

## ✨ Funcionalidades

- 📥 Recebe e armazena a localização (latitude/longitude) enviada pelo app
- 🌐 Busca a lista de unidades de saúde diretamente da base de dados abertos do Recife (CKAN)
- 📏 Calcula a distância geodésica entre o usuário e cada unidade
- 📋 Retorna a lista de unidades ordenada por distância

## 🛠️ Tecnologias utilizadas

- [Flask](https://flask.palletsprojects.com/) — framework web
- [geopy](https://geopy.readthedocs.io/) — geocoding e cálculo de distância (`Nominatim` e `geodesic`)
- [ckanapi](https://github.com/ckan/ckanapi) — consulta à base de dados abertos do Recife (CKAN)

## 🗂️ Estrutura

```
.
└── app.py   # aplicação Flask com as rotas /pegarcoords e /listarunidades
```

## 🔌 Endpoints

| Endpoint | Método | Descrição |
|----------|--------|-----------|
| `/pegarcoords` | `POST` | Recebe `{ "latitude": ..., "longitude": ... }` e armazena a localização do usuário em memória. |
| `/listarunidades` | `GET` | Retorna a lista de unidades de saúde do Recife, com a distância até o usuário calculada e ordenada da menor para a maior. |

### Exemplo de requisição — `POST /pegarcoords`

```json
{
  "latitude": -8.0476,
  "longitude": -34.8770
}
```

### Exemplo de resposta — `GET /listarunidades`

```json
[
  {
    "_id": 1,
    "nome_oficial": "UPA Recife",
    "fone": "1234-5678",
    "endereço": "Rua Exemplo, 123",
    "latitude": "-8.0500",
    "longitude": "-34.8800",
    "distancia": 0.85
  }
]
```

## ⚠️ Limitações atuais

- **Sem banco de dados:** a localização do usuário fica armazenada apenas em memória (variável global `usuario`), em uma única posição. Isso significa que o sistema atualmente **só suporta um usuário por vez** — múltiplos usuários simultâneos sobrescrevem a mesma localização. Uma evolução natural do projeto seria associar a localização a uma sessão ou ID de usuário, persistido em um banco de dados.
- A lista de unidades é carregada uma única vez na inicialização do servidor (variável `unidades`), então atualizações na base de dados do Recife só serão refletidas após reiniciar a aplicação.

## ⚙️ Como executar localmente

1. Clone o repositório e acesse a pasta do backend:
   ```bash
   git clone <url-do-repositorio>
   cd backend
   ```

2. Crie um ambiente virtual (opcional, mas recomendado):
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. Instale as dependências:
   ```bash
   pip install flask geopy ckanapi
   ```

4. Execute o servidor:
   ```bash
   python app.py
   ```

   O servidor ficará disponível em `http://0.0.0.0:5000`.

## 🚀 Deploy (importante!)

> ⚠️ **Atenção:** o app mobile feito em Expo **não consegue acessar `localhost`** do seu computador, pois ele roda em um dispositivo físico ou emulador separado (e o `localhost` do dispositivo não é o mesmo `localhost` da sua máquina). Por isso, **rodar o backend apenas localmente não é suficiente** para testar o app completo.

Para que o app Expo consiga se conectar ao backend, é necessário fazer o **deploy em uma plataforma acessível pela internet** (ou pelo menos pela mesma rede do dispositivo).

Após o deploy, basta substituir `seu-backend` pela URL pública gerada (ex: `https://tampesuacaneta-backend.onrender.com`) nos arquivos `home.js` e `list.js` do app Expo.

## 📍 Fonte dos dados

Os dados das unidades de saúde são obtidos via API pública do [Dados Recife](https://dados.recife.pe.gov.br/), utilizando o recurso (`resource_id`) referente à distribuição de preservativos.
