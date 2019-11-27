
# Crawler
Crawler feito em python que acessa 40.000 links de páginas entre Mercado Livre, Magazine Luiza e Casas Bahia


## Início

O Crawler é executado no arquivo crawler.py. Primeiro ele lê o arquivo offers.csv onde estão localizados os 40 000 links.
Após finalizar a coleta, os dados coletados (nome do produto, preço, nome do site e link) são salvos em um banco de dados MySQL trabalhando localhost ( nome do banco etl ) . Também é criado um arquivo dados.csv com os mesmos dados.

### Pré Requisitos

Python3 e bibliotecas BeautifulSoup4, Pandas, csv, pymysql, sqlalchemy.

### Script para criação da tabela 
```
CREATE TABLE dados (
  Produto varchar(200),
  Preco float ,
  Site varchar(20),
  Link varchar(300)
) 
```

### Execução
Comando para executar o Crawler:

```
py crawler.py
```

### Consulta
A consulta pode ser feita tanto por preço quanto por nome do produto

Comando para executar a consulta pelos dados:

```
py consulta.py  Argumento1 Argumento2
```
Argumento1 = Preco ou Produto

Argumento2 = Número float ou string

Exemplo:
```
py consulta.py  Preco 1499.00
```


### Estrutura do projeto

Não foi utililado nenhum Design Pattern específico. O projeto é baseado em POO e utiliza threads para otimizar o processo de captura. Cada thread é responsável por 10.000 request para assim capturar os dados no melhor tempo possível.

Antes do início de construção do crawler foi feito uma análise do offers.csv para a verificação de dados nulos ou duplicados. 
Após a captura também foi feita uma pequena análise dos dados.

O arquivo Análises.ipynb contém tais análises.



## Autor

* **Cláucio Gonçalves Mendes de Carvalho Filho** - (https://github.com/clauciof)


