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
| pagamento | competencia_ini | competencia_fim | cod | demonstrativo | categoria | conta | quantidade | valor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2025-12-12 | 2025-12-01 | 2025-12-31 | 1500 | ADIANTAMENTO QUINZENAL | Bruto | 2820 Adiant Quinzenal |  | R$83,555.12 |
| 2025-12-18 | 2025-12-01 | 2025-12-31 | 1502 | DÉCIMO TERCEIRO | Benefícios | 1330a FGTS |  | R$1,989.33 |
| 2025-12-18 | 2025-12-01 | 2025-12-31 | 1502 | DÉCIMO TERCEIRO | Bruto | 0512 13º Salário - 2ª Parcela | 1 | R$24,867.62 |
| 2025-12-18 | 2025-12-01 | 2025-12-31 | 1502 | DÉCIMO TERCEIRO | Impostos | 9960 INSS 13Salário |  | -R$1,966.43 |
| 2025-12-18 | 2025-12-01 | 2025-12-31 | 1502 | DÉCIMO TERCEIRO (outros) |  | 5251 Base IR 13Sal |  | -R$17,626.32 |
| 2025-12-18 | 2025-12-01 | 2025-12-31 | 1502 | DÉCIMO TERCEIRO (outros) |  | 8000 Salario Contribuicao |  | -R$24,867.62 |
| 2025-12-18 | 2025-12-01 | 2025-12-31 | 1502 | DÉCIMO TERCEIRO (outros) |  | 8003 Contribuição - Trib. 13º Salário |  | -R$24,867.62 |
| 2025-12-18 | 2025-12-01 | 2025-12-31 | 1502 | DÉCIMO TERCEIRO (outros) |  | 9961 Base INSS 13Salário |  | -R$24,867.62 |
| 2025-12-18 | 2025-12-01 | 2025-12-31 | 1502 | DÉCIMO TERCEIRO (outros) |  | 1301 Base FGTS RecMes - 13Sal |  | -R$24,867.62 |
| 2025-12-18 | 2025-12-01 | 2025-12-31 | 1502 | DÉCIMO TERCEIRO (outros) |  | 1331 FGTS RecMes - 13Sal |  | -R$1,989.33 |
| 2025-12-18 | 2025-12-01 | 2025-12-31 | 1502 | DÉCIMO TERCEIRO (outros) |  | 8100 Inss Empregador | 20 | -R$4,973.50 |
| 2025-12-18 | 2025-12-01 | 2025-12-31 | 1502 | DÉCIMO TERCEIRO (outros) |  | 8101 RAT |  | -R$248.65 |
| 2025-12-29 | 2025-12-01 | 2025-12-31 | 1494 | MENSAL | Alocações | 5590 Prev. Privada Básica |  | -R$14,010.33 |
| 2025-12-29 | 2025-12-01 | 2025-12-31 | 1494 | MENSAL | Benefícios | 3179a Vale |  | R$8,777.32 |
| 2025-12-29 | 2025-12-01 | 2025-12-31 | 1494 | MENSAL | Benefícios | 3913a Contrib.Patrocinadora |  | R$28,020.66 |
| 2025-12-29 | 2025-12-01 | 2025-12-31 | 1494 | MENSAL | Benefícios | 1330a FGTS |  | R$16,710.91 |
| 2025-12-29 | 2025-12-01 | 2025-12-31 | 1494 | MENSAL | Bruto | 0010 Salário Base | 140 | R$208,887.69 |
| 2025-12-29 | 2025-12-01 | 2025-12-31 | 1494 | MENSAL | Bruto | 3259 AJUDA DE CUSTO HOME OFFICE |  | R$6,964.62 |
| 2025-12-29 | 2025-12-01 | 2025-12-31 | 1494 | MENSAL | Bruto | 2821 Adiant Quinzenal |  | -R$83,555.12 |
| 2025-12-29 | 2025-12-01 | 2025-12-31 | 1494 | MENSAL | Co-participações | 3179 VA - DESCONTO |  | -R$877.73 |
| 2025-12-29 | 2025-12-01 | 2025-12-31 | 1494 | MENSAL | Co-participações | 5321 Seguro de Vida Desc.Autorizado |  | -R$616.68 |
| 2025-12-29 | 2025-12-01 | 2025-12-31 | 1494 | MENSAL | Impostos | 5500 IR Retido |  | -R$39,011.39 |
| 2025-12-29 | 2025-12-01 | 2025-12-31 | 1494 | MENSAL | Impostos | 5560 INSS |  | -R$11,348.75 |
| 2025-12-29 | 2025-12-01 | 2025-12-31 | 1494 | MENSAL (outros) |  | 5501 Base IR |  | -R$181,267.62 |
| 2025-12-29 | 2025-12-01 | 2025-12-31 | 1494 | MENSAL (outros) |  | 5561 Base INSS |  | -R$97,282.93 |
| 2025-12-29 | 2025-12-01 | 2025-12-31 | 1494 | MENSAL (outros) |  | 8000 Salario Contribuicao |  | -R$208,887.69 |
| 2025-12-29 | 2025-12-01 | 2025-12-31 | 1494 | MENSAL (outros) |  | 8002 Contribuição - Trib. Salário |  | -R$208,887.69 |
| 2025-12-29 | 2025-12-01 | 2025-12-31 | 1494 | MENSAL (outros) |  | 1300 Base FGTS RecMes - Remun |  | -R$208,887.69 |
| 2025-12-29 | 2025-12-01 | 2025-12-31 | 1494 | MENSAL (outros) |  | 1330 FGTS RecMes - Remun |  | -R$16,710.91 |
| 2025-12-29 | 2025-12-01 | 2025-12-31 | 1494 | MENSAL (outros) |  | 3911 Contrib. Básica Participante C2_28 |  | -R$14,010.33 |
| 2025-12-29 | 2025-12-01 | 2025-12-31 | 1494 | MENSAL (outros) |  | 3913 Contrib.Patrocinadora |  | -R$28,020.66 |
| 2025-12-29 | 2025-12-01 | 2025-12-31 | 1494 | MENSAL (outros) |  | 8010 Salário Contribuição INSS Empregado |  | -R$208,887.69 |
| 2025-12-29 | 2025-12-01 | 2025-12-31 | 1494 | MENSAL (outros) |  | 8100 Inss Empregador | 20 | -R$41,777.56 |
| 2025-12-29 | 2025-12-01 | 2025-12-31 | 1494 | MENSAL (outros) |  | 8101 RAT |  | -R$2,088.91 |
| 2026-01-14 | 2026-01-01 | 2026-01-31 | 1505 | ADIANTAMENTO QUINZENAL | Bruto | 2820 Adiant Quinzenal |  | R$119,364.46 |
| 2026-01-29 | 2026-01-01 | 2026-01-31 | 1501 | MENSAL | Alocações | 5590 Prev. Privada Básica |  | -R$14,010.33 |
| 2026-01-29 | 2026-01-01 | 2026-01-31 | 1501 | MENSAL | Benefícios | 3179a Vale |  | R$12,271.56 |
| 2026-01-29 | 2026-01-01 | 2026-01-31 | 1501 | MENSAL | Benefícios | 3913a Contrib.Patrocinadora |  | R$14,010.33 |
| 2026-01-29 | 2026-01-01 | 2026-01-31 | 1501 | MENSAL | Benefícios | 1330a FGTS |  | R$23,872.77 |
| 2026-01-29 | 2026-01-01 | 2026-01-31 | 1501 | MENSAL | Bruto | 0010 Salário Base | 200 | R$298,411.03 |
| 2026-01-29 | 2026-01-01 | 2026-01-31 | 1501 | MENSAL | Bruto | 3259 AJUDA DE CUSTO HOME OFFICE |  | R$1,431.09 |
| 2026-01-29 | 2026-01-01 | 2026-01-31 | 1501 | MENSAL | Bruto | 2821 Adiant Quinzenal |  | -R$119,364.46 |
| 2026-01-29 | 2026-01-01 | 2026-01-31 | 1501 | MENSAL | Co-participações | 3179 VA - DESCONTO |  | -R$1,227.16 |
| 2026-01-29 | 2026-01-01 | 2026-01-31 | 1501 | MENSAL | Co-participações | 5321 Seguro de Vida Desc.Autorizado |  | -R$616.68 |
| 2026-01-29 | 2026-01-01 | 2026-01-31 | 1501 | MENSAL | Impostos | 5500 IR Retido |  | -R$63,510.74 |
| 2026-01-29 | 2026-01-01 | 2026-01-31 | 1501 | MENSAL | Impostos | 5560 INSS |  | -R$11,783.44 |
| 2026-01-29 | 2026-01-01 | 2026-01-31 | 1501 | MENSAL (outros) |  | 5501 Base IR |  | -R$270,356.27 |
| 2026-01-29 | 2026-01-01 | 2026-01-31 | 1501 | MENSAL (outros) |  | 5561 Base INSS |  | -R$101,076.98 |
| 2026-01-29 | 2026-01-01 | 2026-01-31 | 1501 | MENSAL (outros) |  | 8000 Salario Contribuicao |  | -R$298,411.03 |
| 2026-01-29 | 2026-01-01 | 2026-01-31 | 1501 | MENSAL (outros) |  | 8002 Contribuição - Trib. Salário |  | -R$298,411.03 |
| 2026-01-29 | 2026-01-01 | 2026-01-31 | 1501 | MENSAL (outros) |  | 1300 Base FGTS RecMes - Remun |  | -R$298,411.03 |
| 2026-01-29 | 2026-01-01 | 2026-01-31 | 1501 | MENSAL (outros) |  | 1330 FGTS RecMes - Remun |  | -R$23,872.77 |
| 2026-01-29 | 2026-01-01 | 2026-01-31 | 1501 | MENSAL (outros) |  | 3911 Contrib. Básica Participante C2_28 |  | -R$14,010.33 |
| 2026-01-29 | 2026-01-01 | 2026-01-31 | 1501 | MENSAL (outros) |  | 3913 Contrib.Patrocinadora |  | -R$14,010.33 |
| 2026-01-29 | 2026-01-01 | 2026-01-31 | 1501 | MENSAL (outros) |  | 8010 Salário Contribuição INSS Empregado |  | -R$298,411.03 |
| 2026-01-29 | 2026-01-01 | 2026-01-31 | 1501 | MENSAL (outros) |  | 8100 Inss Empregador | 20 | -R$59,682.23 |
| 2026-01-29 | 2026-01-01 | 2026-01-31 | 1501 | MENSAL (outros) |  | 8101 RAT |  | -R$2,984.05 |

Aba **Sumário por demonstrativo** tem valores sumarizados por categorias e por demonstrativo encontrado

| pagamento | Bruto Total | Bruto | Horas extras | Benefícios | Alocações | Co-participações | Impostos | Depósito Bancário | Ganho Real |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 2025-12-12 | $83,555.12 | $83,555.12 | $0.00 | $0.00 | $0.00 | $0.00 | $0.00 | $83,555.12 | $83,555.12 |
| 2025-12-18 | $26,856.94 | $24,867.62 | $0.00 | $1,989.33 | $0.00 | $0.00 | -$1,966.43 | $22,901.18 | $24,890.51 |
| 2025-12-29 | $199,816.39 | $132,297.18 | $0.00 | $53,508.88 | -$14,010.33 | -$1,494.41 | -$50,360.14 | $66,432.30 | $147,961.84 |
| 2026-01-14 | $119,364.46 | $119,364.46 | $0.00 | $0.00 | $0.00 | $0.00 | $0.00 | $119,364.46 | $119,364.46 |
| 2026-01-29 | $244,642.64 | $180,477.66 | $0.00 | $50,154.66 | -$14,010.33 | -$1,843.83 | -$75,294.18 | $89,329.31 | $167,504.63 |

Aba **Sumário mensal** é como a anterior, mas dá melhor noção de renda mensal total

| pagamento | Bruto Total | Bruto | Horas extras | Benefícios | Alocações | Co-participações | Impostos | Depósito Bancário | Ganho Real |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 2025-12-31 | $310,228.46 | $240,719.92 | $0.00 | $55,498.21 | -$14,010.33 | -$1,494.41 | -$52,326.57 | $172,888.61 | $256,407.48 |
| 2026-01-31 | $364,007.10 | $299,842.12 | $0.00 | $50,154.66 | -$14,010.33 | -$1,843.83 | -$75,294.18 | $208,693.77 | $286,869.09 |

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