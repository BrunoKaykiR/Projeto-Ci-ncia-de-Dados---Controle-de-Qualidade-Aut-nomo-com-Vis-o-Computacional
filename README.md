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

**🔗 [Acesse o Notebook da EDA no Google Colab Aqui](([https://colab.research.google.com/drive/1uKUpcCgyvqQxBplP7kMnRLN7zjR4lQic?usp=sharing](https://colab.research.google.com/drive/1uKUpcCgyvqQxBplP7kMnRLN7zjR4lQic?usp=sharing)))**

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

## 10. Aprofundamentos Estatísticos (Entregas Individuais)
Como desdobramento da etapa de Análise Exploratória (M2), os membros do grupo aplicaram técnicas de Estatística Inferencial para comprovar matematicamente os padrões visuais encontrados, garantindo que não fossem fruto do acaso. 

Cada validação gerou um notebook específico, integrado a este repositório:

* **Validação Estrutural | Rubens Souza (RA: 062210040):** Focou na detecção de quebras no vidro. Após confirmar a normalidade dos dados (Shapiro-Wilk), aplicou o **Teste T de Student** e comprovou que a variável `edge_density` (densidade de bordas) possui diferença estatisticamente significativa ($p < 0,05$) entre peças íntegras e quebradas. O cálculo do Tamanho do Efeito confirmou o alto impacto prático dessa diferença, consolidando esta métrica como a *feature* geométrica principal para a rede neural.

* **Validação de Anomalias Internas | Bruno Kayki (RA: 062210015):** Focou na detecção de sujeira e líquidos estranhos. Devido à alta presença de outliers nessa classe, utilizou o teste não-paramétrico de **Mann-Whitney** para analisar a Variabilidade de Contraste (`contrast`). O teste resultou na rejeição da hipótese nula ($p < 0,05$), provando matematicamente que a contaminação afeta a estabilidade dos pixels. O Tamanho do Efeito validou que filtros de variância local serão cruciais para a IA identificar essas anomalias.

* **Teste de Sensibilidade a Micro-defeitos | Itamar Junior (RA: 062210003):** Como complemento à validação estrutural, testou a sensibilidade matemática do projeto focando nas microfissuras e pequenas lascas (classe broken_small). Através do teste de Mann-Whitney, rejeitou a hipótese nula ($p < 0,05$), provando que a variável de densidade de bordas possui granularidade suficiente para detectar defeitos sutis, garantindo a alta precisão exigida no controle de qualidade da indústria de bebidas.

* **Inviabilidade de Sensores Luminosos | Augusto Bueno(RA: 062210015):** Em uma abordagem de validação de hipótese nula, testou a capacidade da variável brightness (brilho global) de diferenciar peças boas de defeituosas. Utilizando o Teste T, comprovou-se um P-valor altíssimo ($P \approx 0,98$) e um Tamanho de Efeito irrelevante. Esse resultado matemático atesta que sensores fotoelétricos tradicionais não funcionam para este problema de negócio, justificando tecnicamente e financeiramente o desenvolvimento de Redes Neurais Convolucionais baseadas em textura e estrutura espacial.

* **Separabilidade Multiclasse de Anomalias | Gustavo da Paz (RA: 062210032):** Focou na viabilidade do modelo IA em não apenas detectar falhas, mas classificá-las para fins de roteamento na esteira de produção. Avaliou as três classes de falha simultaneamente (broken_large, broken_small, contamination). Utilizando o teste de Kruskal-Wallis (ANOVA Não-Paramétrica), comprovou ($p < 0,05$) que os defeitos possuem assinaturas estruturais distintas entre si. O cálculo do Efeito ($\eta^2$) validou o uso de uma arquitetura de classificação multiclasse (ao invés de um modelo binário) para a etapa M3, agregando alto valor financeiro através da triagem de descarte.

---

## 11. Etapa 03: Desenvolvimento do Modelo de Machine Learning

Nesta etapa, consolidamos os aprendizados da Análise Exploratória (M2) para construir o motor de decisão da esteira de qualidade. Optamos por uma arquitetura de classificação multiclasse capaz de detectar e rotear os 4 tipos de cenários (`good`, `broken_large`, `broken_small`, `contamination`).

### 1. Protótipo e Lógica no Google AI Studio
Utilizando modelos generativos multimodais de última geração via **Google AI Studio**, implementamos a lógica de software baseada em *Few-Shot Prompting*. O modelo foi instruído com as diretrizes de densidade de bordas e contraste validadas na M2, recebendo exemplos práticos para atuar como um inspetor autônomo.
* **🔗 [Link do Protótipo no Google AI Studio]([COLE_O_LINK_DO_PASSO_2_AQUI](https://aistudio.google.com/app/prompts?state=%7B%22ids%22:%5B%2210QwM7mLXzwyB5hi4zbEJ9v9HtUP9U6ry%22%5D,%22action%22:%22open%22,%22userId%22:%22113200929059837560470%22,%22resourceKeys%22:%7B%7D%7D&usp=sharing, https://drive.google.com/file/d/1M8I3f_LPf5bZiNfxYITe54uyGyCn_6Ov/view?usp=sharing, https://drive.google.com/file/d/1c3D7j3MQdiurCda-7tK6XXXKmX-P5w-2/view?usp=sharing, https://drive.google.com/file/d/1h6iTt6Qc3Ns5-DFx3UOGzy6gE-xJ9oRa/view?usp=sharing, https://drive.google.com/file/d/1oyY_g0RMZC9w2-WaG_7x4c0AW2H8U78l/view?usp=sharing, https://drive.google.com/file/d/1wQz1Q7nl9H1zau17tfH0N0C4mZnv8h-_/view?usp=sharing))**
* O código Python gerado pela plataforma encontra-se versionado no repositório no arquivo `app_classificacao.py`.

### 2. Avaliação de Performance (Baseline e Validação)
Para garantir o rigor estatístico exigido para classificação de imagens industriais, construímos um ambiente de validação técnica das predições:
* **Foco Inicial (Baseline Clássico):** O uso de Machine Learning clássico (Random Forest) alcançou apenas 44% de Acurácia, provando a necessidade de análise espacial (Deep Learning).
* **Validação do Modelo Espacial:** A transição para a avaliação de características em matrizes (utilizando Transfer Learning com MobileNetV2) obteve sucesso na separabilidade inicial.
  * **Acurácia e F1-Score (Macro):** 54% (na primeira iteração com baixo volume de dados).
  * **Matriz de Confusão:** O *Recall* da classe `good` subiu drasticamente, reduzindo o descarte indevido (falsos positivos). A IA demonstrou capacidade de detecção da classe crítica `contamination`, cujo F1-Score anterior era nulo e subiu para 0.55.
* **Próximos Passos (Etapa 04):** As métricas apontam que a arquitetura está correta, porém sofre de *underfitting* pela escassez de dados. Aplicaremos técnicas de *Data Augmentation* na próxima fase para elevar o F1-Score a níveis de produção (>90%).
