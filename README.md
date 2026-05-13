# 🔧 Projeto: Controle de Qualidade Autônomo com Visão Computacional

![Status do Projeto](https://img.shields.io/badge/Status-Conclu%C3%ADdo%20/%20M4-brightgreen)
![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python)
![TensorFlow](https://img.shields.io/badge/Keras--TensorFlow-Modelagem-orange?logo=tensorflow)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red?logo=streamlit)

---

## 👥 1. Identificação do Grupo
* **Instituição:** Faculdade Engenheiro Salvador Arena
* **Curso:** Engenharia de Controle e Automação
* **Grupo:** Visão Industrial Avançada
* **Integrantes:**
  * Augusto Bueno - RA: 062210015
  * Bruno Kayki - RA: 062210018
  * Itamar Junior - RA: 062210003
  * Gustavo da Paz - RA: 062210032
  * Rubens Souza - RA: 062210040

---

## 🎯 2. Área Problema Selecionada
O grupo seleciona uma das áreas norteadoras abaixo para o desenvolvimento do projeto:
- [ ] Manutenção Preditiva de Zero-Downtime
- [ ] Eficiência Energética e Descarbonização via Smart Grids
- [X] Controle de Qualidade Autônomo com Visão Computacional
- [ ] Gêmeos Digitais (Digital Twins) e Analytics em Tempo Real

---

## 🧩 3. Diagnóstico e Definição do Problema
Esta seção apresenta a fundamentação do desafio. O grupo descreve o cenário de atuação e justifica a importância da solução proposta.

* **Contexto:** O projeto aborda o cenário da Indústria 4.0 aplicada ao setor de bebidas e envase automatizado. Em linhas de produção que operam em altíssima velocidade, a inspeção visual de recipientes de vidro é um componente crítico para garantir a integridade do produto e a segurança do consumidor final.
* **Problema:** A dificuldade central reside na ineficiência da inspeção manual e na limitação de sensores tradicionais para detectar anomalias complexas. Falhas como microfissuras no vidro, contaminações internas ou quebras sutis no gargalo são difíceis de identificar por sensores de presença ou peso, resultando em lotes comprometidos que geram desperdício ou riscos de recall.
* **Impacto:** A solução visa otimizar o índice de conformidade da linha de produção (Yield). Espera-se reduzir drasticamente o descarte indevido de peças boas (falsos positivos) e, principalmente, eliminar a passagem de peças defeituosas para o mercado, resultando em redução de custos operacionais e mitigação de riscos à saúde pública.

---

## 🗂️ 4. Arquitetura de Dados (Fonte e Dataset)
O projeto utiliza dados estruturados para alimentar os modelos preditivos.

* **Origem dos Dados:** [MVTec AD Dataset - Bottle](https://www.mvtec.com/company/research/datasets/mvtec-ad).
* **Características:** O conjunto de dados apresenta categorias de imagens em alta resolução (RGB) divididas em:
  * **Controle (Good):** Garrafas íntegras para treino de padrão.
  * **Anomalias (Defects):** Categorias rotuladas como `broken_large` (quebras estruturais), `broken_small` (lascas) e `contamination` (sujeira ou partículas estranhas).
* **Volume:** O dataset de garrafas conta com 209 imagens de treino (apenas peças boas) e 83 imagens de teste (mistura de peças boas e com os 3 tipos de defeitos), totalizando 292 arquivos com resolução original de 900x900.

---

## 🔄 5. Plano de Tratamento de Dados (ETL)
O pipeline de dados segue as seguintes etapas de processamento:

1. **Extração:** A ingestão ocorre via carregamento de arquivos de imagem (`.png`) organizados em subdiretórios que definem as classes de treinamento e validação.
2. **Transformação:** O grupo aplica as seguintes etapas de tratamento:
   * **Redimensionamento:** Conversão de 900x900 para 224x224 pixels para otimizar o uso de memória (RAM/GPU).
   * **Normalização:** Conversão da escala de cores de inteiros (0-255) para ponto flutuante (0.0-1.0), essencial para a estabilidade matemática das redes neurais.
   * **Filtragem Bi-dimensional:** Aplicação de filtros para redução de ruído de compressão e realce de bordas onde rachaduras são mais prováveis de ocorrer.
   * **Data Augmentation:** Geração sintética de variações (brilho e rotação leve) para aumentar a robustez do modelo espacial.
3. **Carga:** Os dados tratados e os tensores gerados são disponibilizados na pasta `/data/processed` ou em objetos de memória (DataLoaders) prontos para consumo dos modelos de Machine Learning.

---

## 📊 6. Análise Exploratória de Dados - EDA (Entrega M2)
A fase de "conversa com os dados" foi realizada via Google Colab e focou em validar se métricas globais eram suficientes ou se seria necessário o uso de Redes Neurais para a detecção de defeitos.

**🔗 [Acesse o Notebook da EDA no Google Colab Aqui](https://colab.research.google.com/drive/1uKUpcCgyvqQxBplP7kMnRLN7zjR4lQic?usp=sharing)**

### Descobertas e Identificação de Padrões:
* **O Paradoxo do Brilho ($P=0,98$):** Realizamos um teste de hipótese para verificar se a média de brilho diferenciava as garrafas. O resultado ($P=0,98$) falhou em rejeitar a hipótese nula, provando que o brilho global **não é um indicador viável**.
* **Diferenciação Estrutural (Canny Edge):** O uso de filtros de borda revelou que garrafas íntegras possuem uma densidade de borda mais estável e superior, enquanto quebras grandes (`broken_large`) destroem a silhueta contínua do vidro, permitindo separação estatística.
* **Detecção de Outliers e Dispersão:** O gráfico de violino comprovou que a classe `contamination` possui instabilidade extrema e outliers severos, indicando que agentes externos afetam o desvio padrão dos pixels.
* **Mapas de Calor:** A subtração de imagens validou a localização espacial das quebras nas áreas de maior estresse (fundo e gargalo).
* **Validação de Hipótese:** Como as variáveis globais falharam e as variáveis locais (textura/borda) demonstraram separabilidade, **justifica-se tecnicamente o avanço para modelos de Deep Learning (CNNs)**.

---

## 📈 7. Desenvolvimento do Modelo de Machine Learning (Etapa 03)
Nesta etapa, consolidamos os aprendizados da Análise Exploratória para construir o motor de decisão da esteira de qualidade. Optamos por uma arquitetura de classificação multiclasse capaz de detectar e rotear os 4 tipos de cenários (`good`, `broken_large`, `broken_small`, `contamination`).

### Protótipo e Lógica no Google AI Studio
Utilizando modelos generativos multimodais de última geração via **Google AI Studio**, implementamos a lógica de software baseada em *Few-Shot Prompting*. O modelo foi instruído com as diretrizes de densidade de bordas e contraste validadas na M2.
* 🔗 **[Acessar Protótipo no Google AI Studio](https://aistudio.google.com/app/prompts?state=%7B%22ids%22:%5B%2210QwM7mLXzwyB5hi4zbEJ9v9HtUP9U6ry%22%5D,%22action%22:%22open%22,%22userId%22:%22113200929059837560470%22,%22resourceKeys%22:%7B%7D%7D&usp=sharing)**
* *(O código Python gerado pela plataforma encontra-se versionado na pasta `/scripts` no arquivo `app_classificacao.py`)*.

### Avaliação de Performance (Baseline e Validação)
* **Foco Inicial (Baseline Clássico):** O uso de Machine Learning clássico (Random Forest) alcançou apenas 44% de Acurácia, provando a necessidade de análise espacial.
* **Validação do Modelo Espacial:** A transição para a avaliação de características em matrizes (Transfer Learning com MobileNetV2) obteve sucesso na separabilidade multiclasse. A capacidade de detecção da classe crítica `contamination` subiu drasticamente, garantindo um direcionamento preciso para triagem na esteira.

---

## 🖥️ 8. Dashboard de Monitoramento e Inferência (Etapa 04)
Para atender à necessidade de uma interface visual aplicável ao chão de fábrica, desenvolvemos um painel interativo em **Streamlit**:
- **Funcionalidades:** Monitoramento ao vivo das métricas (Acurácia, F1-Score, Recall), distribuição gráfica de probabilidade de falhas e um **Simulador de Inferência**.
- **Edge Computing Simulado:** O operador pode realizar o upload de uma imagem da esteira e receber o diagnóstico instantâneo da IA, visualizando a decisão de roteamento (Aprovação, Lavagem ou Triturador) diretamente na tela.

---

## 🧱 9. Estrutura do Repositório
A organização das pastas facilita a manutenção e o versionamento do projeto:

/
├── data/               
│   ├── raw/            # Arquivos de dados originais (não modificados)
│   └── processed/      # Imagens tratadas e transformadas
├── docs/               # Documentação técnica e relatórios do projeto
├── images/             # Gráficos da EDA e prints do Dashboard Streamlit
├── notebooks/          # Notebooks Jupyter/Colab (EDA e Modelagem MobileNetV2)
├── scripts/            # Códigos-fonte (.py), incluindo o Dashboard e AI Studio
├── requirements.txt    # Dependências mapeadas
└── README.md           # Documentação principal

## 🚀 10. Instruções para ExecuçãoPara reproduzir o ambiente de dados, executar o pipeline e iniciar o Dashboard:Clone este repositório.Instale as dependências através do comando:Bashpip install -r requirements.txt
Para iniciar o painel de monitoramento, execute:Bashstreamlit run scripts/dashboard.py

---

## 🧪 11. Aprofundamentos Estatísticos (Entregas Individuais) Como desdobramento da etapa de Análise Exploratória (M2), os membros do grupo aplicaram técnicas de Estatística Inferencial para comprovar matematicamente os padrões visuais encontrados, garantindo que não fossem fruto do acaso.

---

## Validação Estrutural | Rubens Souza (RA: 062210040): Focou na detecção de quebras no vidro. Após confirmar a normalidade dos dados (Shapiro-Wilk), aplicou o Teste T de Student e comprovou que a variável edge_density (densidade de bordas) possui diferença estatisticamente significativa ($p < 0,05$) entre peças íntegras e quebradas. O cálculo do Tamanho do Efeito confirmou o alto impacto prático dessa diferença, consolidando esta métrica como a feature geométrica principal para a rede neural.

---

## Validação de Anomalias Internas | Bruno Kayki (RA: 062210018): Focou na detecção de sujeira e líquidos estranhos. Devido à alta presença de outliers nessa classe, utilizou o teste não-paramétrico de Mann-Whitney para analisar a Variabilidade de Contraste (contrast). O teste resultou na rejeição da hipótese nula ($p < 0,05$), provando matematicamente que a contaminação afeta a estabilidade dos pixels. O Tamanho do Efeito validou que filtros de variância local serão cruciais para a IA identificar essas anomalias.

---

## Teste de Sensibilidade a Micro-defeitos | Itamar Junior (RA: 062210003): Como complemento à validação estrutural, testou a sensibilidade matemática do projeto focando nas microfissuras e pequenas lascas (broken_small). Através do teste de Mann-Whitney, rejeitou a hipótese nula ($p < 0,05$), provando que a variável de densidade de bordas possui granularidade suficiente para detectar defeitos sutis, garantindo a alta precisão exigida no controle de qualidade da indústria de bebidas.

---

## Inviabilidade de Sensores Luminosos | Augusto Bueno (RA: 062210015): Em uma abordagem de validação de hipótese nula, testou a capacidade da variável brightness (brilho global) de diferenciar peças boas de defeituosas. Utilizando o Teste T, comprovou-se um P-valor altíssimo ($P \approx 0,98$) e um Tamanho de Efeito irrelevante. Esse resultado matemático atesta que sensores fotoelétricos tradicionais não funcionam para este problema de negócio, justificando tecnicamente e financeiramente o desenvolvimento de Redes Neurais Convolucionais.

---
## Separabilidade Multiclasse de Anomalias | Gustavo da Paz (RA: 062210032): Focou na viabilidade do modelo IA em não apenas detectar falhas, mas classificá-las para fins de roteamento na esteira de produção. Avaliou as três classes de falha simultaneamente. Utilizando o teste de Kruskal-Wallis (ANOVA Não-Paramétrica), comprovou ($p < 0,05$) que os defeitos possuem assinaturas estruturais distintas entre si. O cálculo do Efeito ($\eta^2$) validou o uso de uma arquitetura de classificação multiclasse (ao invés de um modelo binário).


## 12. Apêndice de IA (Transparência)A Inteligência Artificial Generativa (Gemini) foi utilizada sob a premissa de pair-programming e co-criação durante todo o ciclo de desenvolvimento (M2 a M4).Aplicações:Estruturação e debug de scripts Python para ETL utilizando opencv-python e pandas.Geração de gráficos estatísticos complexos (seaborn.violinplot e mapas de calor de diferença absoluta).Auxílio na interpretação técnica do P-valor (0.98), sugerindo a busca por métricas texturais (bordas) em detrimento de métricas globais de cor.Estruturação do Front-end em Streamlit para o Dashboard.Validação Humana: A IA não realizou cálculos autônomos definitivos. Todos os insights sugeridos foram ativamente codificados no Colab pelo grupo e submetidos à validação da biblioteca scipy.stats. Os padrões visuais indicados pelos gráficos foram conferidos um a um mediante amostragem visual direta no dataset original para garantir rigor científico e industrial.
