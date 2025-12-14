# Chatbot para Suporte Psicológico e Bem-Estar Mental

Projeto desenvolvido como Trabalho de Conclusão de Curso (TCC) no curso de **Tecnologia em Análise e Desencolvimento de Sistemas** do **Centro Universitário de Adamantina (UniFAI)**.

Autor: **Endrew Silva**
--
Orientadora: **Profª Dra. Míriam Regina Bordinhon**  
--

---

## 1. Descição do Projeto
Este projeto consiste em um **chatbot simples em Python**, com interface web desenvolvida em **Flask**, cujo objetivo é fornecer **apoio emocional inicial** e promover **bem-estar mental**.

O sistema:  
- Utiliza **técnicas breves de acolhimento** (respiração, grounding, gratidão).  
- Detecta possíveis **situações de crise** (ideação suicida, autolesão).  
- Apresenta **mensagens de segurança e encaminhamento** (CVV 188, SAMU 192, emergência 190).  
- Armazena as conversas em um **banco SQLite** para posterior análise.

⚠️ **Aviso Importante:** Este chatbot **não substitui psicoterapia nem atendimento médico**. É apenas um recurso complementar de apoio emocional inicial.

---

## 2. Funcionalidades Principais  
- Respostas baseadas em **intents** (saudação, ansiedade, tristeza, estresse, sono, autocuidado, gratidão, encerrar).  
- **Fallback**: resposta genérica quando não compreende a mensagem.  
- **Detecção de crise** com mensagens de encaminhamento seguro.  
- Registro de conversas no **SQLite** com:  
  - mensagem do usuário  
  - resposta do bot  
  - sentimento (quando disponível)  
  - intent  
  - flag de crise  
- Interface web simples e responsiva em Flask.  
- Script de avaliação `eval_report.py` para métricas básicas.

---

## 3. Tecnologias Utilizadas  
- **Python 3.12+**  
- **Flask** (servidor web)  
- **SQLite** (banco de dados local)  
- **spaCy** (processamento de linguagem natural)  
- **NLTK** (stopwords em português)  
- **Transformers** (opcional, para análise de sentimento com PyTorch/TensorFlow)  
- **HTML + CSS** (interface web)  

---

## 4. Pré-Requisitos  
- Python 3.12 ou superior  
- VS Code (opcional, mas recomendado)  
- Navegador web atualizado  

---

## 5. Instalação  

### Passo 1 — Clonar ou extrair o projeto
- powershell
- git clone https://github.com/silvaEndrew1/chatbot-bemestar.git
- cd chatbot-bemestar
### Passo 2 — Criar ambiente virtual
python -m venv .venv
- .\.venv\Scripts\activate.bat
### Passo 3 — Instalar dependências
- pip install -r requirements.txt
### Passo 4 — Baixar modelos de PLN
- python -m spacy download pt_core_news_sm
- python -c "import nltk; import nltk; nltk.download('punkt'); nltk.download('stopwords')"
### Passo 5 — (opcional, para análise de sentimento com Transformers)**
- pip install torch --index-url https://download.pytorch.org/whl/cpu

---

## 6. Execução

### Passo 1 — Criar banco de dados:
- python init_db.py
### Passo 2 — Rodar o servidor Flask:
- python app.py
### Passo 3 — Acessar o navegador:
- Acessar no navegador: http://127.0.0.1:5000

---

## 7. Uso

### Exemplo 1:
Usuário: "Estou ansioso hoje"
Bot: Sugere exercício de respiração.

### Exemplo 2:
Usuário: "Tenho dormido mal"
Bot: Sugere práticas de higiene do sono.

### Exemplo 3 (crise):
Usuário: "Penso em me machucar"
Bot: Aciona mensagem de segurança + encaminhamento.

---

## 8. Estrutura de Arquivos

📂 projeto_tcc_chatbot
 ├── app.py                  # Servidor Flask
 ├── db.py                   # Conexão e funções do banco
 ├── init_db.py              # Criação das tabelas no SQLite
 ├── safety.py               # Regras de segurança e detecção de crise
 ├── nlp_utils.py            # NLP com spaCy/NLTK/Transformers
 ├── bot_core.py             # Núcleo do chatbot (intents, respostas)
 ├── seed_corpus.json        # Dicionário inicial de intents
 ├── eval_report.py          # Script de avaliação (métricas e export CSV)
 ├── requirements.txt        # Dependências do projeto
 ├── README.md               # Este documento
 ├── RESULTADOS_DISCUSSÃO.md # Rascunho do capítulo de resultados
 ├── templates/
 │    └── index.html       # Interface web (HTML)
 └── static/
      └── styles.css       # Estilo da interface (CSS)

---

## 9. Avaliação (Resultados e Discussão)

- O script eval_report.py gera relatórios a partir das conversas salvas no banco.
Exemplo de saída:

==== RELATÓRIO ====
Total de turnos: 42
Intents:
  - ansiedade: 10
  - sono: 8
  - saudacao: 5
Crises detectadas: 2 (4,8%)
(Também pode exportar os dados para conversations.csv).

---

## 10. Considerações Éticas

### • O chatbot não substitui atendimento profissional.
### • Mensagens claras de encaminhamento são fornecidas em casos de risco.
### • O sistema não faz diagnóstico; apenas sugere técnicas simples de autocuidado.

---

## 11. Autor e Orientação

### Autor: Endrew Silva

### Orientadora: Profª Dra. Míriam Regina Bordinhon

### Curso: Tecnologia em Análise e Desenvolvimento de Sistemas – UniFAI
