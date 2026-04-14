# Projeto: Controle de Qualidade Autônomo com Visão Computacional

## 1. Identificação do Grupo
* **Instituição:** Faculdade Engenheiro Salvador Arena
* **Curso:** Engenharia de Controle e Automação
* **Grupo:** Grupo 3
* **Integrantes:**
  * Augusto Bueno - RA: 062210015
  * Bruno Kayki - RA: 062210018
  * Itamar Junior - RA: 062210003
  * Gustavo da Paz - RA: 062210032
  * Rubens Souza - RA: 062210040

---

## 2. Área Problema Selecionada
O grupo seleciona uma das áreas norteadoras abaixo para o desenvolvimento do projeto:
- [ ] Manutenção Preditiva de Zero-Downtime
- [ ] Eficiência Energética e Descarbonização via Smart Grids
- [X] Controle de Qualidade Autônomo com Visão Computacional
- [ ] Gêmeos Digitais (Digital Twins) e Analytics em Tempo Real

---

## 3. Diagnóstico e Definição do Problema
Esta seção apresenta a fundamentação do desafio. O grupo descreve o cenário de atuação e justifica a importância da solução proposta.

* **Contexto:** O projeto aborda o cenário da Indústria 4.0 aplicada ao setor de bebidas e envase automatizado. Em linhas de produção que operam em altíssima velocidade, a inspeção visual de recipientes de vidro é um componente crítico para garantir a integridade do produto e a segurança do consumidor final.
* **Problema:** A dificuldade central reside na ineficiência da inspeção manual e na limitação de sensores tradicionais para detectar anomalias complexas. Falhas como microfissuras no vidro, contaminações internas ou quebras sutis no gargalo são difíceis de identificar por sensores de presença ou peso, resultando em lotes comprometidos que geram desperdício ou riscos de recall.
* **Impacto:** A solução visa otimizar o índice de conformidade da linha de produção (Yield). Espera-se reduzir drasticamente o descarte indevido de peças boas (falsos positivos) e, principalmente, eliminar a passagem de peças defeituosas para o mercado, resultando em redução de custos operacionais e mitigação de riscos à saúde pública.

---

## 4. Arquitetura de Dados (Fonte e Dataset)
O projeto utiliza dados estruturados para alimentar os modelos preditivos.

* **Origem dos Dados:** [MVTec AD Dataset - Bottle](https://www.mvtec.com/company/research/datasets/mvtec-ad).
* **Características:** O conjunto de dados apresenta categorias de imagens em alta resolução (RGB) divididas em:
  * **Controle (Good):** Garrafas íntegras para treino de padrão.
  * **Anomalias (Defects):** Categorias rotuladas como `broken_large` (quebras estruturais), `broken_small` (lascas) e `contamination` (sujeira ou partículas estranhas).
* **Volume:** O dataset de garrafas conta com 209 imagens de treino (apenas peças boas) e 83 imagens de teste (mistura de peças boas e com os 3 tipos de defeitos), totalizando 292 arquivos com resolução original de 900x900.

---

## 5. Plano de Tratamento de Dados (ETL)
O pipeline de dados segue as seguintes etapas de processamento:

1. **Extração:** A ingestão ocorre via carregamento de arquivos de imagem (`.png`) organizados em subdiretórios que definem as classes de treinamento e validação.
2. **Transformação:** O grupo aplica as seguintes etapas de tratamento:
   * **Redimensionamento:** Conversão de 900x900 para 224x224 pixels para otimizar o uso de memória (RAM/GPU).
   * **Normalização:** Conversão da escala de cores de inteiros (0-255) para ponto flutuante (0.0-1.0), essencial para a estabilidade matemática das redes neurais.
   * **Filtragem Bi-dimensional:** Aplicação de filtros para redução de ruído de compressão e realce de bordas onde rachaduras são mais prováveis de ocorrer.
   * **Data Augmentation:** Geração sintética de variações (brilho e rotação leve) para aumentar a robustez do modelo.
3. **Carga:** Os dados tratados e os tensores gerados são disponibilizados na pasta `/data/processed` ou em objetos de memória (DataLoaders) prontos para consumo dos modelos de Machine Learning.

---

## 6. Análise Exploratória de Dados - EDA (Entrega M2)
A fase de "conversa com os dados" foi realizada via Google Colab e focou em validar se métricas globais eram suficientes ou se seria necessário o uso de Redes Neurais para a detecção de defeitos.

**🔗 [Acesse o Notebook da EDA no Google Colab Aqui]((https://colab.research.google.com/drive/1uKUpcCgyvqQxBplP7kMnRLN7zjR4lQic?usp=sharing))**

### 📊 Descobertas e Identificação de Padrões:
* **O Paradoxo do Brilho ($P=0,98$):** Realizamos um teste de hipótese para verificar se a média de brilho diferenciava as garrafas. O resultado ($P=0,98$) falhou em rejeitar a hipótese nula, provando que o brilho global **não é um indicador viável**.
* **Diferenciação Estrutural (Canny Edge):** O uso de filtros de borda revelou que garrafas íntegras possuem uma densidade de borda mais estável e superior, enquanto quebras grandes (`broken_large`) destroem a silhueta contínua do vidro, permitindo separação estatística.
* **Detecção de Outliers e Dispersão:** O gráfico de violino comprovou que a classe `contamination` possui instabilidade extrema e outliers severos, indicando que agentes externos afetam o desvio padrão dos pixels.
* **Mapas de Calor:** A subtração de imagens validou a localização espacial das quebras nas áreas de maior estresse (fundo e gargalo).
* **Validação de Hipótese:** Como as variáveis globais falharam e as variáveis locais (textura/borda) demonstraram separabilidade, **justifica-se tecnicamente o avanço para modelos de Deep Learning (CNNs)** na próxima fase do projeto.

---

## 7. Estrutura do Repositório
A organização das pastas facilita a manutenção e o versionamento do projeto:
* `/docs`: Contém os diagramas de fluxo de dados, imagens dos gráficos da EDA e documentação técnica.
* `/data/raw`: Armazena os arquivos de dados originais (não modificados).
* `/data/processed`: Armazena os dados após a execução do script de ETL.
* `/notebooks`: Contém o notebook Google Colab com a Análise Exploratória de Dados (EDA).
* `/scripts`: Contém os códigos Python responsáveis pelo tratamento dos dados.
* `requirements.txt`: Lista todas as bibliotecas necessárias para a execução do projeto.

---

## 8. Instruções para Execução
Para reproduzir o ambiente de dados e executar o pipeline de ETL:
1. Clona-se este repositório.
2. Instalam-se as dependências através do comando:
   ```bash
   pip install -r requirements.txt
---

## 9. 🤖 Apêndice de IA (Transparência)
A Inteligência Artificial Generativa (Gemini) foi utilizada sob a premissa de *pair-programming* e co-criação durante a etapa M2.

* **Aplicações:** * Estruturação e debug de scripts Python para ETL utilizando `opencv-python` e `pandas`.
  * Geração de gráficos estatísticos complexos (`seaborn.violinplot` e mapas de calor de diferença absoluta).
  * Auxílio na interpretação técnica do P-valor (0.98), sugerindo a busca por métricas texturais (bordas) em detrimento de métricas globais de cor.
* **Validação Humana:** A IA não realizou cálculos autônomos definitivos. Todos os *insights* sugeridos foram ativamente codificados no Colab pelo grupo e submetidos à validação da biblioteca `scipy.stats`. Os padrões visuais indicados pelos gráficos foram conferidos um a um mediante amostragem visual direta no dataset original para garantir que as diferenças estatísticas correspondiam à realidade das peças no ambiente de manufatura.
