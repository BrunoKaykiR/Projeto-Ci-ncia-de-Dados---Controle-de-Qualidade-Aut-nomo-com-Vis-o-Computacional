Projeto: Controle de Qualidade Autônomo com Visão Computacional

1. Identificação do Grupo
Instituição: Faculdade Engenheiro Salvador Arena
Curso: [Engenharia de Controle e Automação]
Grupo: [Grupo 3]
Integrantes:
	[Augusto Bueno] - RA: [062210015]
	[Bruno Kayki] - RA: [062210018]
	[Itamar Junior] - RA: [062210003]
	[Gustavo da Paz] - RA: [062210032]
	[Rubens Souza] - RA: [062210040]
---
2. Área Problema Selecionada
O grupo seleciona uma das áreas norteadoras abaixo para o desenvolvimento do projeto:
[ ] Manutenção Preditiva de Zero-Downtime
[ ] Eficiência Energética e Descarbonização via Smart Grids
[X] Controle de Qualidade Autônomo com Visão Computacional
[ ] Gêmeos Digitais (Digital Twins) e Analytics em Tempo Real
> \*\*Nota:\*\* Marque com um \[x] a opção escolhida.
---
3. Diagnóstico e Definição do Problema
Esta seção apresenta a fundamentação do desafio. O grupo descreve o cenário de atuação e justifica a importância da solução proposta.
Contexto: O projeto aborda o cenário da Indústria 4.0 aplicada ao setor de bebidas e envase automatizado. Em linhas de produção que operam em altíssima velocidade, a inspeção visual de recipientes de vidro é um componente crítico para garantir a integridade do produto e a segurança do consumidor final.
Problema: A dificuldade central reside na ineficiência da inspeção manual e na limitação de sensores tradicionais para detectar anomalias complexas. Falhas como microfissuras no vidro, contaminações internas ou quebras sutis no gargalo são difíceis de identificar por sensores de presença ou peso, resultando em lotes comprometidos que geram desperdício ou riscos de recall..
Impacto: A solução visa otimizar o índice de conformidade da linha de produção (Yield). Espera-se reduzir drasticamente o descarte indevido de peças boas (falsos positivos) e, principalmente, eliminar a passagem de peças defeituosas para o mercado, resultando em redução de custos operacionais e mitigação de riscos à saúde pública.
---
4. Arquitetura de Dados (Fonte e Dataset)
O projeto utiliza dados estruturados para alimentar os modelos preditivos.
Origem dos Dados: [https://www.mvtec.com/company/research/datasets/mvtec-ad].
Características: O conjunto de dados apresenta categorias de imagens em alta resolução (RGB) divididas em:
Controle (Good): Garrafas íntegras para treino de padrão.
Anomalias (Defects): Categorias rotuladas como broken_large (quebras estruturais), broken_small (lascas) e contamination (sujeira ou partículas estranhas).
Volume: O dataset de garrafas conta com 209 imagens de treino (apenas peças boas) e 83 imagens de teste (mistura de peças boas e com os 3 tipos de defeitos), totalizando 292 arquivos com resolução original de 900x 900.
---
5. Plano de Tratamento de Dados (ETL)
O pipeline de dados segue as seguintes etapas de processamento:
Extração: A ingestão ocorre via carregamento de arquivos de imagem (.png) organizados em subdiretórios que definem as classes de treinamento e validação.
Transformação: O grupo aplica as seguintes etapas de tratamento:Redimensionamento: Conversão de 900x900 para 224x224 pixels para otimizar o uso de memória (RAM/GPU).Normalização: Conversão da escala de cores de inteiros (0-255) para ponto flutuante (0.0-1.0), essencial para a estabilidade matemática das redes neurais.Filtragem Bi-dimensional: Aplicação de filtros para redução de ruído de compressão e realce de bordas onde rachaduras são mais prováveis de ocorrer.Data Augmentation: Geração sintética de variações (brilho e rotação leve) para aumentar a robustez do modelo.
3. Carga: Os dados tratados e os tensores gerados são disponibilizados na pasta /data/processed ou em objetos de memória (DataLoaders) prontos para consumo dos modelos de Machine Learning.

6. Estrutura do Repositório
A organização das pastas facilita a manutenção e o versionamento do projeto:
`/docs`: Contém os diagramas de fluxo de dados e a documentação técnica.
`/data/raw`: Armazena os arquivos de dados originais (não modificados).
`/data/processed`: Armazena os dados após a execução do script de ETL.
`/scripts`: Contém os códigos Python responsáveis pelo tratamento dos dados.
`requirements.txt`: Lista todas as bibliotecas necessárias para a execução do projeto.
---
7. Instruções para Execução
Para reproduzir o ambiente de dados e executar o pipeline de ETL:
Clona-se este repositório.
Instalam-se as dependências através do comando:
```bash
   pip install -r requirements.txt
