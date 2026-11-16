# RentSmart — Sistema de Orçamento de Locação (R.M Imóveis)

Aplicação em Python desenvolvida com **Programação Orientada a Objetos (POO)** para automatizar o cálculo de orçamentos de locação da **R.M Imóveis**, separando o valor do aluguel mensal da taxa contratual e gerando uma projeção de pagamentos para 12 meses em formato CSV.

## Estrutura do Projeto

- `imoveis.py`: Define a classe base abstrata `Imovel` e as subclasses `Apartamento`, `Casa` e `Estudio`, aplicando herança, encapsulamento e polimorfismo.
- `orcamento.py`: Define a classe `OrcamentoLocacao`, responsável por calcular a taxa contratual parcelada, montar o resumo detalhado do orçamento e exportar o arquivo CSV de 12 meses.
- `main.py`: Ponto de entrada da aplicação em linha de comando (CLI), com validação completa das entradas do usuário.
- `orcamento_rentsmart.csv`: Arquivo gerado automaticamente ao final da execução com a projeção dos 12 meses do contrato.

## Regras de Negócio Implementadas

| Categoria | Aluguel-Base (1 quarto) | 2º Quarto | Estacionamento / Garagem | Desconto |
| :--- | :---: | :---: | :---: | :---: |
| **Apartamento** | R$ 700,00 | + R$ 200,00 | + R$ 300,00 (1 vaga) | 5% se não possuir crianças (após adicionais) |
| **Casa** | R$ 900,00 | + R$ 250,00 | + R$ 300,00 (1 vaga) | — |
| **Estúdio** | R$ 1.200,00 | — | R$ 250,00 (pacote 2 vagas) + R$ 60,00/vaga extra | — |

- **Taxa contratual**: R$ 2.000,00 fixos, parceláveis em **1x até 5x**, exibidos separadamente do aluguel mensal.

## Pré-requisitos e Execução

O projeto utiliza apenas a **biblioteca padrão do Python 3** (não requer instalação de pacotes externos).

1. Clone ou baixe os arquivos do repositório.
2. No terminal, acesse a pasta do projeto.
3. Execute o comando:

```bash
python3 main.py
```

4. Siga as instruções no terminal para informar o tipo de imóvel, características e parcelamento da taxa contratual.
5. Ao final, o resumo será exibido na tela e o arquivo `orcamento_rentsmart.csv` será salvo na mesma pasta.
