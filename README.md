# Sobre

Este arquivo README fornece instruções sobre como executar o projeto que utiliza um ambiente Conda. 

O projeto possui um pré-processamento que deve ser executado antes de realizar as operações no PowerBI para que os dados estejam devidamente tratados.

# Executando o Projeto

1. Primeiro passo é criar o ambiente com base no .yml, rodando o seguinte comando

```conda env create -f preProcEnv.yml```

2. Em seguida, ative o ambiente:

```conda activate preProcEnv.yml```

3. Com isso feito, basta rodar o script de processamento dos dados:

``python pre_processamento.py``

4. Após isso, será gerado um arquivo '.csv' no seguinte formato:

```"CID", "RO", "AC", "AM", "RR", "PA", "AP", "TO", "MA", "PI", "CE", "RN", "PB", "PE", "AL", "SE", "BA", "MG", "ES", "RJ", "SP", "PR", "SC", "RS", "MS", "MT", "GO", "DF", "TOTAL"```

Onde CID significa a doença e as colunas de cada estado é o número de mortes dessa doença em determinado estado. O total também é exibido na última coluna.
# Equipe

Por: João Gabriel Dourado Cervo, Israel Segalin e Pedro Lorea
