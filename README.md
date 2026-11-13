# Extrator de olerites do site ADP Brasil

Este programa acessa https://expert.hcm.adp.com/adpweb e extrai todos os seus olerites.
Grava-os em planilha Excel, PDFs e arquivo pickle com dados puros e processados para contabilidade, análise e visualização.

Usa o Chromium com Selenium.

Uso na linha de comando:

```shell
usage: adpscrape.py [-h] [--adp-user ADP_USER] [--adp-password ADP_PASSWORD] [--start-year START_YEAR]
                    [--headless | --no-headless] [--pdf | --no-pdf] [--pickle | --no-pickle] [--output OUTPUT]
                    [-d | --debug | --no-debug]

options:
  -h, --help                     show this help message and exit
  --adp-user ADP_USER            ADP username (default: $ADP_USER environment variable)
  --adp-password ADP_PASSWORD    ADP password (default: $ADP_PASSWORD environment variable)
  --start-year START_YEAR        Começa a extração a partir deste ano (default: $ADP_SINCE ou ano passado)
  --headless, --no-headless      Executa o navegador (Chromium) sem janela nehuma (só que não funciona) (use --no-headless para
                                 ver o navegador trabalhando; default $HEADLESS ou falso)
  --excel, --no-excel            Salva planilha Excel com diversas visões (default: $EXCEL ou salva sim)
  --pdf, --no-pdf                Salva PDFs dos demonstrativos (use --no-pdf para não salvar; default: $PDF ou salva sim)
  --pickle, --no-pickle          Salva arquivo Pickle com tudo o que foi extraido e dados processados (default: $PICKLE ou
                                 salva sim)
  --output OUTPUT                Pasta para escrever resultados (default: $OUTPUT ou pasta atual)
  -d, --debug, --no-debug        Debug mode
```

Todos esses parâmetros podem também ser passados no arquivo `.env`. Veja exemplo em [.env.example](.env.example).

Eu uso este programa todo mês para pegar meus olerites, acompanhar minha renda e integrar os dados extraídos no
meu [Investorzilla](https://github.com/avibrazil/investorzilla).

## O que ele exporta

Este programa cria os seguintes arquivos:

- Planilha Excel com algumas visões detalhadas e sumarizadas de todos os meses
- Arquivos PDF, um para cada demonstrativo encontrado (mensal, adiantamento, 13o.)
- Arquivo Pickle com todos os dados originais extraídos e algumas sumarizações

Os dados na planilha Excel foram categorizados e sumarizados (em algumas abas) de modo que
sirvam para dar uma melhor noção de renda mensal integral e líquida, inlcuindo:

- **Benefícios** tangíveis e não-tangíveis, como vale, carro, aportes patrocinados de previdência privada etc.
- **Bruto**, que é basicamente o salário nominal
- **Bruto Total**, o salário nominal mais benefícios
- **Horas extras**
- **Alocações**, valores subtraidos do bruto e que vão para outras contas, como previdência privada
- **Co-participações**, valores subtraídos do bruto para uso de plano de saúde, parcela do vale alimentação etc
- **Impostos**, valores subtraidos para impostos
- **Depósitos bancários**, o que é realmente depositado no banco do funcionário
- **Ganho real**, o bruto total menos impostos e co-participações

### Conteúdo da planilha excel

Aba **Contabilidade detalhada** é basicamente a junção de todos os olerites e cada conta é **categorizada**
| pagamento   | competencia_ini   | competencia_fim   |   cod | demonstrativo            | categoria        | conta                                    |   quantidade |       valor |
|:------------|:------------------|:------------------|------:|:-------------------------|:-----------------|:-----------------------------------------|-------------:|------------:|
| 2025-12-12  | 2025-12-01        | 2025-12-31        |  1500 | ADIANTAMENTO QUINZENAL   | Bruto            | 2820 Adiant Quinzenal                    |              |   45312.1   |
| 2025-12-18  | 2025-12-01        | 2025-12-31        |  1502 | DÉCIMO TERCEIRO          | Benefícios       | 1330a FGTS                               |              |    1078.82  |
| 2025-12-18  | 2025-12-01        | 2025-12-31        |  1502 | DÉCIMO TERCEIRO          | Bruto            | 0512 13º Salário - 2ª Parcela            |         1    |   13485.8   |
| 2025-12-18  | 2025-12-01        | 2025-12-31        |  1502 | DÉCIMO TERCEIRO          | Impostos         | 9960 INSS 13Salário                      |              |   -1066.4   |
| 2025-12-18  | 2025-12-01        | 2025-12-31        |  1502 | DÉCIMO TERCEIRO (outros) |                  | 5251 Base IR 13Sal                       |              |   -9558.79  |
| 2025-12-18  | 2025-12-01        | 2025-12-31        |  1502 | DÉCIMO TERCEIRO (outros) |                  | 8000 Salario Contribuicao                |              |  -13485.8   |
| 2025-12-18  | 2025-12-01        | 2025-12-31        |  1502 | DÉCIMO TERCEIRO (outros) |                  | 8003 Contribuição - Trib. 13º Salário    |              |  -13485.8   |
| 2025-12-18  | 2025-12-01        | 2025-12-31        |  1502 | DÉCIMO TERCEIRO (outros) |                  | 9961 Base INSS 13Salário                 |              |  -13485.8   |
| 2025-12-18  | 2025-12-01        | 2025-12-31        |  1502 | DÉCIMO TERCEIRO (outros) |                  | 1301 Base FGTS RecMes - 13Sal            |              |  -13485.8   |
| 2025-12-18  | 2025-12-01        | 2025-12-31        |  1502 | DÉCIMO TERCEIRO (outros) |                  | 1331 FGTS RecMes - 13Sal                 |              |   -1078.82  |
| 2025-12-18  | 2025-12-01        | 2025-12-31        |  1502 | DÉCIMO TERCEIRO (outros) |                  | 8100 Inss Empregador                     |        20    |   -2697.14  |
| 2025-12-29  | 2025-12-01        | 2025-12-31        |  1494 | MENSAL                   | Alocações        | 5590 Prev. Privada Básica                |              |   -7597.83  |
| 2025-12-29  | 2025-12-01        | 2025-12-31        |  1494 | MENSAL                   | Benefícios       | 3913a Contrib.Patrocinadora              |              |   15195.7   |
| 2025-12-29  | 2025-12-01        | 2025-12-31        |  1494 | MENSAL                   | Benefícios       | 1330a FGTS                               |              |    9062.36  |
| 2025-12-29  | 2025-12-01        | 2025-12-31        |  1494 | MENSAL                   | Bruto            | 0010 Salário Base                        |       140    |  113280     |
| 2025-12-29  | 2025-12-01        | 2025-12-31        |  1494 | MENSAL                   | Bruto            | 2821 Adiant Quinzenal                    |              |  -45312.1   |
| 2025-12-29  | 2025-12-01        | 2025-12-31        |  1494 | MENSAL                   | Impostos         | 5500 IR Retido                           |              |  -21156     |
| 2025-12-29  | 2025-12-01        | 2025-12-31        |  1494 | MENSAL                   | Impostos         | 5560 INSS                                |              |   -6154.45  |
| 2025-12-29  | 2025-12-01        | 2025-12-31        |  1494 | MENSAL (outros)        |                  | 5501 Base IR                             |              |  -98301.8   |
| 2025-12-29  | 2025-12-01        | 2025-12-31        |  1494 | MENSAL (outros)        |                  | 5561 Base INSS                           |              |  -52756.7   |
| 2025-12-29  | 2025-12-01        | 2025-12-31        |  1494 | MENSAL (outros)        |                  | 8000 Salario Contribuicao                |              | -113280     |
| 2025-12-29  | 2025-12-01        | 2025-12-31        |  1494 | MENSAL (outros)        |                  | 8002 Contribuição - Trib. Salário        |              | -113280     |
| 2025-12-29  | 2025-12-01        | 2025-12-31        |  1494 | MENSAL (outros)        |                  | 1300 Base FGTS RecMes - Remun            |              | -113280     |
| 2025-12-29  | 2025-12-01        | 2025-12-31        |  1494 | MENSAL (outros)        |                  | 1330 FGTS RecMes - Remun                 |              |   -9062.36  |
| 2025-12-29  | 2025-12-01        | 2025-12-31        |  1494 | MENSAL (outros)        |                  | 3911 Contrib. Básica Participante C2_28  |              |   -7597.83  |
| 2025-12-29  | 2025-12-01        | 2025-12-31        |  1494 | MENSAL (outros)        |                  | 3913 Contrib.Patrocinadora               |              |  -15195.7   |
| 2025-12-29  | 2025-12-01        | 2025-12-31        |  1494 | MENSAL (outros)        |                  | 8010 Salário Contribuição INSS Empregado |              | -113280     |
| 2025-12-29  | 2025-12-01        | 2025-12-31        |  1494 | MENSAL (outros)        |                  | 8100 Inss Empregador                     |        20    |  -22656.1   |
| 2026-01-14  | 2026-01-01        | 2026-01-31        |  1505 | ADIANTAMENTO QUINZENAL | Bruto            | 2820 Adiant Quinzenal                    |              |   64731.6   |
| 2026-01-29  | 2026-01-01        | 2026-01-31        |  1501 | MENSAL                 | Alocações        | 5590 Prev. Privada Básica                |              |   -7597.83  |
| 2026-01-29  | 2026-01-01        | 2026-01-31        |  1501 | MENSAL                 | Benefícios       | 3913a Contrib.Patrocinadora              |              |    7597.83  |
| 2026-01-29  | 2026-01-01        | 2026-01-31        |  1501 | MENSAL                 | Benefícios       | 1330a FGTS                               |              |   12946.3   |
| 2026-01-29  | 2026-01-01        | 2026-01-31        |  1501 | MENSAL                 | Bruto            | 0010 Salário Base                        |       200    |  161829     |
| 2026-01-29  | 2026-01-01        | 2026-01-31        |  1501 | MENSAL                 | Bruto            | 2821 Adiant Quinzenal                    |              |  -64731.6   |
| 2026-01-29  | 2026-01-01        | 2026-01-31        |  1501 | MENSAL                 | Impostos         | 5500 IR Retido                           |              |  -34442     |
| 2026-01-29  | 2026-01-01        | 2026-01-31        |  1501 | MENSAL                 | Impostos         | 5560 INSS                                |              |   -6390.18  |
| 2026-01-29  | 2026-01-01        | 2026-01-31        |  1501 | MENSAL (outros)        |                  | 5501 Base IR                             |              | -146615     |
| 2026-01-29  | 2026-01-01        | 2026-01-31        |  1501 | MENSAL (outros)        |                  | 5561 Base INSS                           |              |  -54814.3   |
| 2026-01-29  | 2026-01-01        | 2026-01-31        |  1501 | MENSAL (outros)        |                  | 8000 Salario Contribuicao                |              | -161829     |
| 2026-01-29  | 2026-01-01        | 2026-01-31        |  1501 | MENSAL (outros)        |                  | 8002 Contribuição - Trib. Salário        |              | -161829     |
| 2026-01-29  | 2026-01-01        | 2026-01-31        |  1501 | MENSAL (outros)        |                  | 1300 Base FGTS RecMes - Remun            |              | -161829     |
| 2026-01-29  | 2026-01-01        | 2026-01-31        |  1501 | MENSAL (outros)        |                  | 1330 FGTS RecMes - Remun                 |              |  -12946.3   |
| 2026-01-29  | 2026-01-01        | 2026-01-31        |  1501 | MENSAL (outros)        |                  | 3911 Contrib. Básica Participante C2_28  |              |   -7597.83  |
| 2026-01-29  | 2026-01-01        | 2026-01-31        |  1501 | MENSAL (outros)        |                  | 3913 Contrib.Patrocinadora               |              |   -7597.83  |
| 2026-01-29  | 2026-01-01        | 2026-01-31        |  1501 | MENSAL (outros)        |                  | 8010 Salário Contribuição INSS Empregado |              | -161829     |
| 2026-01-29  | 2026-01-01        | 2026-01-31        |  1501 | MENSAL (outros)        |                  | 8100 Inss Empregador                     |        20    |  -32365.8   |


Aba **Sumário por demonstrativo** tem valores sumarizados por categorias e por demonstrativo encontrado


| pagamento  | Demonstrativo          | Bruto Total   | Bruto         | Horas extras   | Benefícios   | Alocações    | Co-participações   | Impostos      | Depósito Bancário   | Ganho Real    |
|:-----------|:-----------------------|--------------:|--------------:|---------------:|-------------:|-------------:|-------------------:|--------------:|--------------------:|--------------:|
| 2025-12-12 | ADIANTAMENTO QUINZENAL | R$ 45,312.12  | R$ 45,312.12  | R$ 0.00        | R$ 0.00      | R$ 0.00      | R$ 0.00            | R$ 0.00       | R$ 45,312.12        | R$ 45,312.12  |
| 2025-12-18 | DÉCIMO TERCEIRO        | R$ 14,564.58  | R$ 13,485.76  | R$ 0.00        | R$ 1,078.82  | R$ 0.00      | R$ 0.00            | R$ -1,066.40  | R$ 12,419.36        | R$ 13,498.18  |
| 2025-12-29 | MENSAL                 | R$ 108,360.86 | R$ 71,745.05  | R$ 0.00        | R$ 29,017.98 | R$ -7,597.83 | R$ -810.42         | R$ -27,310.41 | R$ 36,026.38        | R$ 80,240.03  |
| 2026-01-14 | ADIANTAMENTO QUINZENAL | R$ 64,731.61  | R$ 64,731.61  | R$ 0.00        | R$ 0.00      | R$ 0.00      | R$ 0.00            | R$ 0.00       | R$ 64,731.61        | R$ 64,731.61  |
| 2026-01-29 | MENSAL                 | R$ 132,670.24 | R$ 97,873.43  | R$ 0.00        | R$ 27,198.98 | R$ -7,597.83 | R$ -999.92         | R$ -40,832.20 | R$ 48,443.48        | R$ 90,838.12  |


Aba **Sumário mensal** é como a anterior, mas dá melhor noção de renda mensal total

| pagamento  | Bruto Total   | Bruto         | Horas extras   | Benefícios   | Alocações    | Co-participações   | Impostos      | Depósito Bancário   | Ganho Real    |
|:-----------|--------------:|--------------:|---------------:|-------------:|-------------:|-------------------:|--------------:|--------------------:|--------------:|
| 2025-12-31 | R$ 168,237.57 | R$ 130,542.93 | R$ 0.00        | R$ 30,096.80 | R$ -7,597.83 | R$ -810.42         | R$ -28,376.81 | R$ 93,757.87        | R$ 139,050.33 |
| 2026-01-31 | R$ 197,401.84 | R$ 162,605.03 | R$ 0.00        | R$ 27,198.98 | R$ -7,597.83 | R$ -999.92         | R$ -40,832.20 | R$ 113,175.09       | R$ 155,569.73 |

## Rode via container

Incluí um `Containerfile` que prepara uma instalação bem integrada.

O objetivo era rodar o browser em modo _headless_, ou seja, sem precisar abrir uma janela visual.
Mas o site ADP dá problemas assim, já logo no login.

Então você precisa de um servidor X11 para que a janela do Chromium apareça e rode a extração.
Isso é moleza no Linux. Mas se o container estiver rodando em Windows, você precisa do [VcXsrv](https://sourceforge.net/projects/vcxsrv/).
Se o container rodar em macOS, tenha o [XQuartz](https://www.xquartz.org/) rodando.

## Rode sem container

Eu rodo isso diretamente no meu servidor Fedora Linux com pacotes similares aos do `Containerfile`.

Não testei, mas este programa deve rodar bem em Windows e macOS se você tiver Python 3, todos os modulos instalados (veja o `Containerfile`), o browser Chrome e o driver para controlá-lo (que, se não me engano, o Selenium baixa automaticamente).

Eu tentei primeiramente usar o Firefox, mas tive problemas de compatibilidade em modo driver com o ADP.

## Rode num notebook

Veja o notebook [exemplo de uso.ipynb](exemplo%20de%20uso.ipynb) para mais detalhes.
Os pré-requisitos são os mesmos citados acima. Muitas das operações que escrevi no
notebook já estão incluidas nas operações que o programa principal faz, nas funções `contabilidade_total()` e `sumario()`.