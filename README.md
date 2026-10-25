# Extrator de olerites do side ADP Brasil

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

Os dados na planilha Excel foram tratados e sumarizados (em algumas abas) de modo que
sirvam para dar uma melhor noção de renda mensal integral, inlcuindo benefícios
tangíveis e não-tangíveis, como vale, carro, previdência privada etc.

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