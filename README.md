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

Aba **Contabilidade detalhada** é basicamente a junção de todos os olerites e cada conta é categorizada
| pagamento | competencia_ini | competencia_fim | cod | demonstrativo | categoria | conta | quantidade | valor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2025-12-12 | 2025-12-01 | 2025-12-31 | 1500 | ADIANTAMENTO QUINZENAL | Bruto | 2820 Adiant Quinzenal |  | R$32,609.42 |
| 2025-12-18 | 2025-12-01 | 2025-12-31 | 1502 | DÉCIMO TERCEIRO | Benefícios | 1330a FGTS |  | R$776.38 |
| 2025-12-18 | 2025-12-01 | 2025-12-31 | 1502 | DÉCIMO TERCEIRO | Bruto | 0512 13º Salário - 2ª Parcela | 1 | R$9,705.19 |
| 2025-12-18 | 2025-12-01 | 2025-12-31 | 1502 | DÉCIMO TERCEIRO | Impostos | 9960 INSS 13Salário |  | -R$767.45 |
| 2025-12-18 | 2025-12-01 | 2025-12-31 | 1502 | DÉCIMO TERCEIRO (outros) |  | 5251 Base IR 13Sal |  | -R$6,879.10 |
| 2025-12-18 | 2025-12-01 | 2025-12-31 | 1502 | DÉCIMO TERCEIRO (outros) |  | 8000 Salario Contribuicao |  | -R$9,705.19 |
| 2025-12-18 | 2025-12-01 | 2025-12-31 | 1502 | DÉCIMO TERCEIRO (outros) |  | 8003 Contribuição - Trib. 13º Salário |  | -R$9,705.19 |
| 2025-12-18 | 2025-12-01 | 2025-12-31 | 1502 | DÉCIMO TERCEIRO (outros) |  | 9961 Base INSS 13Salário |  | -R$9,705.19 |
| 2025-12-18 | 2025-12-01 | 2025-12-31 | 1502 | DÉCIMO TERCEIRO (outros) |  | 1301 Base FGTS RecMes - 13Sal |  | -R$9,705.19 |
| 2025-12-18 | 2025-12-01 | 2025-12-31 | 1502 | DÉCIMO TERCEIRO (outros) |  | 1331 FGTS RecMes - 13Sal |  | -R$776.38 |
| 2025-12-18 | 2025-12-01 | 2025-12-31 | 1502 | DÉCIMO TERCEIRO (outros) |  | 8100 Inss Empregador | 20 | -R$1,941.03 |
| 2025-12-18 | 2025-12-01 | 2025-12-31 | 1502 | DÉCIMO TERCEIRO (outros) |  | 8101 RAT |  | -R$97.04 |
| 2025-12-29 | 2025-12-01 | 2025-12-31 | 1494 | MENSAL | Alocações | 5590 Prev. Privada Básica |  | -R$5,467.87 |
| 2025-12-29 | 2025-12-01 | 2025-12-31 | 1494 | MENSAL | Benefícios | 3179a Vale |  | R$3,425.56 |
| 2025-12-29 | 2025-12-01 | 2025-12-31 | 1494 | MENSAL | Benefícios | 3913a Contrib.Patrocinadora |  | R$10,935.74 |
| 2025-12-29 | 2025-12-01 | 2025-12-31 | 1494 | MENSAL | Benefícios | 1330a FGTS |  | R$6,521.84 |
| 2025-12-29 | 2025-12-01 | 2025-12-31 | 1494 | MENSAL | Bruto | 0010 Salário Base | 140 | R$81,523.51 |
| 2025-12-29 | 2025-12-01 | 2025-12-31 | 1494 | MENSAL | Bruto | 3259 AJUDA DE CUSTO HOME OFFICE |  | R$2,718.11 |
| 2025-12-29 | 2025-12-01 | 2025-12-31 | 1494 | MENSAL | Bruto | 2821 Adiant Quinzenal |  | -R$32,609.42 |
| 2025-12-29 | 2025-12-01 | 2025-12-31 | 1494 | MENSAL | Co-participações | 3179 VA - DESCONTO |  | -R$342.56 |
| 2025-12-29 | 2025-12-01 | 2025-12-31 | 1494 | MENSAL | Co-participações | 5321 Seguro de Vida Desc.Autorizado |  | -R$240.67 |
| 2025-12-29 | 2025-12-01 | 2025-12-31 | 1494 | MENSAL | Impostos | 5500 IR Retido |  | -R$15,225.15 |
| 2025-12-29 | 2025-12-01 | 2025-12-31 | 1494 | MENSAL | Impostos | 5560 INSS |  | -R$4,429.12 |
| 2025-12-29 | 2025-12-01 | 2025-12-31 | 1494 | MENSAL (outros) |  | 5501 Base IR |  | -R$70,744.10 |
| 2025-12-29 | 2025-12-01 | 2025-12-31 | 1494 | MENSAL (outros) |  | 5561 Base INSS |  | -R$37,967.03 |
| 2025-12-29 | 2025-12-01 | 2025-12-31 | 1494 | MENSAL (outros) |  | 8000 Salario Contribuicao |  | -R$81,523.51 |
| 2025-12-29 | 2025-12-01 | 2025-12-31 | 1494 | MENSAL (outros) |  | 8002 Contribuição - Trib. Salário |  | -R$81,523.51 |
| 2025-12-29 | 2025-12-01 | 2025-12-31 | 1494 | MENSAL (outros) |  | 1300 Base FGTS RecMes - Remun |  | -R$81,523.51 |
| 2025-12-29 | 2025-12-01 | 2025-12-31 | 1494 | MENSAL (outros) |  | 1330 FGTS RecMes - Remun |  | -R$6,521.84 |
| 2025-12-29 | 2025-12-01 | 2025-12-31 | 1494 | MENSAL (outros) |  | 3911 Contrib. Básica Participante C2_28 |  | -R$5,467.87 |
| 2025-12-29 | 2025-12-01 | 2025-12-31 | 1494 | MENSAL (outros) |  | 3913 Contrib.Patrocinadora |  | -R$10,935.74 |
| 2025-12-29 | 2025-12-01 | 2025-12-31 | 1494 | MENSAL (outros) |  | 8010 Salário Contribuição INSS Empregado |  | -R$81,523.51 |
| 2025-12-29 | 2025-12-01 | 2025-12-31 | 1494 | MENSAL (outros) |  | 8100 Inss Empregador | 20 | -R$16,304.71 |
| 2025-12-29 | 2025-12-01 | 2025-12-31 | 1494 | MENSAL (outros) |  | 8101 RAT |  | -R$815.25 |
| 2026-01-14 | 2026-01-01 | 2026-01-31 | 1505 | ADIANTAMENTO QUINZENAL | Bruto | 2820 Adiant Quinzenal |  | R$46,584.89 |
| 2026-01-29 | 2026-01-01 | 2026-01-31 | 1501 | MENSAL | Alocações | 5590 Prev. Privada Básica |  | -R$5,467.87 |
| 2026-01-29 | 2026-01-01 | 2026-01-31 | 1501 | MENSAL | Benefícios | 3179a Vale |  | R$4,789.27 |
| 2026-01-29 | 2026-01-01 | 2026-01-31 | 1501 | MENSAL | Benefícios | 3913a Contrib.Patrocinadora |  | R$5,467.87 |
| 2026-01-29 | 2026-01-01 | 2026-01-31 | 1501 | MENSAL | Benefícios | 1330a FGTS |  | R$9,316.93 |
| 2026-01-29 | 2026-01-01 | 2026-01-31 | 1501 | MENSAL | Bruto | 0010 Salário Base | 200 | R$116,462.18 |
| 2026-01-29 | 2026-01-01 | 2026-01-31 | 1501 | MENSAL | Bruto | 3259 AJUDA DE CUSTO HOME OFFICE |  | R$558.52 |
| 2026-01-29 | 2026-01-01 | 2026-01-31 | 1501 | MENSAL | Bruto | 2821 Adiant Quinzenal |  | -R$46,584.89 |
| 2026-01-29 | 2026-01-01 | 2026-01-31 | 1501 | MENSAL | Co-participações | 3179 VA - DESCONTO |  | -R$478.93 |
| 2026-01-29 | 2026-01-01 | 2026-01-31 | 1501 | MENSAL | Co-participações | 5321 Seguro de Vida Desc.Autorizado |  | -R$240.67 |
| 2026-01-29 | 2026-01-01 | 2026-01-31 | 1501 | MENSAL | Impostos | 5500 IR Retido |  | -R$24,786.61 |
| 2026-01-29 | 2026-01-01 | 2026-01-31 | 1501 | MENSAL | Impostos | 5560 INSS |  | -R$4,598.77 |
| 2026-01-29 | 2026-01-01 | 2026-01-31 | 1501 | MENSAL (outros) |  | 5501 Base IR |  | -R$105,513.12 |
| 2026-01-29 | 2026-01-01 | 2026-01-31 | 1501 | MENSAL (outros) |  | 5561 Base INSS |  | -R$39,447.75 |
| 2026-01-29 | 2026-01-01 | 2026-01-31 | 1501 | MENSAL (outros) |  | 8000 Salario Contribuicao |  | -R$116,462.18 |
| 2026-01-29 | 2026-01-01 | 2026-01-31 | 1501 | MENSAL (outros) |  | 8002 Contribuição - Trib. Salário |  | -R$116,462.18 |
| 2026-01-29 | 2026-01-01 | 2026-01-31 | 1501 | MENSAL (outros) |  | 1300 Base FGTS RecMes - Remun |  | -R$116,462.18 |
| 2026-01-29 | 2026-01-01 | 2026-01-31 | 1501 | MENSAL (outros) |  | 1330 FGTS RecMes - Remun |  | -R$9,316.93 |
| 2026-01-29 | 2026-01-01 | 2026-01-31 | 1501 | MENSAL (outros) |  | 3911 Contrib. Básica Participante C2_28 |  | -R$5,467.87 |
| 2026-01-29 | 2026-01-01 | 2026-01-31 | 1501 | MENSAL (outros) |  | 3913 Contrib.Patrocinadora |  | -R$5,467.87 |
| 2026-01-29 | 2026-01-01 | 2026-01-31 | 1501 | MENSAL (outros) |  | 8010 Salário Contribuição INSS Empregado |  | -R$116,462.18 |
| 2026-01-29 | 2026-01-01 | 2026-01-31 | 1501 | MENSAL (outros) |  | 8100 Inss Empregador | 20 | -R$23,292.44 |
| 2026-01-29 | 2026-01-01 | 2026-01-31 | 1501 | MENSAL (outros) |  | 8101 RAT |  | -R$1,164.60 |

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