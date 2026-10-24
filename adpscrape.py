#!/usr/bin/env python

import datetime
import time
import os
import io
import types
import argparse
import pathlib
import base64
import pickle
import urllib
import dotenv
import bs4
import pandas

# Selenium Manager é necessário para baixar automaticamente o driver para
# Firefox. No caso de Chromium, ele não é necessário porque o Fedora já
# disponibiliza o pacote chromedriver, sempre compatível com o Chromium da
# distribuição. Só que o Chromium apresentou problemas e parei de usá-lo.
os.environ["SE_MANAGER_PATH"] = "/usr/bin/selenium-manager"

import selenium
import selenium.webdriver
import selenium.webdriver.support.expected_conditions
import selenium.webdriver.support.ui


debug = False


def get_browser_firefox():
    # Firefox apresentou problemas no login e não tem certas funções que usamos
    # para extrair PDF e HTTP com referer. Não use Firefox para esta aplicação.
    options = selenium.webdriver.firefox.options.Options()

    # options.add_argument("--headless")

    # Esta instrumentação de geolocalização não funciona
    options.set_preference("geo.enabled", True)
    options.set_preference("geo.provider.use_corelocation", True)
    options.set_preference("geo.prompt.testing", True)
    options.set_preference("geo.prompt.testing.allow", True)
    # options.set_preference("geo.wifi.uri", 'data:application/json , { "status": "OK", "accuracy ": 100.0, "location": { "lat": 18.975080, "lng": 72.825838, "latitude": 18.975080, "longitude": 72.825838, "accuracy": 100.0 } }')

    driver = selenium.webdriver.Firefox(options=options)

    return driver


def get_browser_chrome(headless=False):
    # --- Configure Chromium ---
    service = selenium.webdriver.chrome.service.Service("/usr/bin/chromedriver")

    options = selenium.webdriver.chrome.options.Options()
    options.binary_location = "/usr/bin/chromium-browser"

    if headless:
        options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")

    # options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # --- Selenium Manager auto-downloads driver ---
    driver = selenium.webdriver.Chrome(options=options, service=service)

    return driver


def adp_url():
    return os.getenv('ADP_URL','https://expert.hcm.adp.com/adpweb')



def adp_login(driver,usuario,senha):
    # Open the website
    driver.get(adp_url())

    # Quanto tempo esperar pelos elementos desejados da página.
    # Se os botões e campos desejados não aparecerem nesse período de tempo,
    # os métodos find_element() a seguir vão falhar e gerar uma excessão.
    driver.implicitly_wait(10)

    # Preenche os campos de usuáro e senha para se logar
    username = (
        driver
        .find_element(
            selenium.webdriver.common.by.By.CSS_SELECTOR,
            "#login-form_username"
        )
    )
    username.send_keys(usuario)
    username.send_keys(selenium.webdriver.common.keys.Keys.ENTER)

    driver.implicitly_wait(3)

    if debug:
        driver.save_screenshot("selenium-login.png")

    password = (
        driver
        .find_element(
            selenium.webdriver.common.by.By.CSS_SELECTOR,
            "#login-form_password"
        )
    )

    for c in senha:
        password.send_keys(c)

    time.sleep(3)

    password.send_keys(selenium.webdriver.common.keys.Keys.ENTER)

    if debug:
        driver.save_screenshot("selenium-login2.png")

    # Opção 1: Press ENTER to login
    # selenium.webdriver.common.action_chains.ActionChains(driver).send_keys(selenium.webdriver.common.keys.Keys.ENTER).perform()

    # Opção 2: 3 tabs para posicinar foco no botão Entrar
    # selenium.webdriver.common.action_chains.ActionChains(driver).send_keys(selenium.webdriver.common.keys.Keys.TAB).perform()
    # selenium.webdriver.common.action_chains.ActionChains(driver).send_keys(selenium.webdriver.common.keys.Keys.TAB).perform()
    # selenium.webdriver.common.action_chains.ActionChains(driver).send_keys(selenium.webdriver.common.keys.Keys.TAB).perform()
    # selenium.webdriver.common.action_chains.ActionChains(driver).send_keys(selenium.webdriver.common.keys.Keys.ENTER).perform()

    # Opção 2: Click no botão "Entrar"
    # (
    #     driver
    #     .find_element(
    #         selenium.webdriver.common.by.By.CSS_SELECTOR,
    #         "sdf-button#signBtn"
    #     )
    #     .click()
    # )



def adp_go_demonstrativos(driver):
    if debug:
        driver.save_screenshot("selenium-links.png")

    # Espera o frame correto ficar disponível
    (
    	selenium.webdriver.support.ui.WebDriverWait(driver, 10).until(
            selenium.webdriver.support
            .expected_conditions
            .frame_to_be_available_and_switch_to_it(
                (selenium.webdriver.common.by.By.CSS_SELECTOR,"frame")
            )
        )
    )

    # Acha o link que leva aos demonstrativos
    demonstrativos=(
        driver
        .find_element(
            selenium.webdriver.common.by.By.CSS_SELECTOR,
            "sfc-shell#shell"
        )
        .find_element(
            selenium.webdriver.common.by.By.CSS_SELECTOR,
            "waypoint-home"
        )
        .shadow_root
        .find_element(
            selenium.webdriver.common.by.By.CSS_SELECTOR,
            "sdf-box.lg-w-full"
        )
        .find_element(
            selenium.webdriver.common.by.By.CSS_SELECTOR,
            "waypoint-expert-box#waypoint-cmp"
        )
        .shadow_root
        .find_element(
            selenium.webdriver.common.by.By.CSS_SELECTOR,
            "sdf-link"
        )
    )

    # Click and wait for new page to be loaded before returning
    demonstrativos.click()



def adp_iterate_demonstrativos(driver,start_year):
    demonstrativos=list()

    driver.switch_to.default_content()

    # Espera o frame correto estar disponível e entra nele
    (
    	selenium.webdriver.support.ui.WebDriverWait(driver, 15)
        .until(
            selenium.webdriver.support
            .expected_conditions
            .frame_to_be_available_and_switch_to_it(
                (selenium.webdriver.common.by.By.CSS_SELECTOR,"frame")
            )
        )
    )

    if debug:
        driver.save_screenshot("selenium-demonstrativos.png")

    # Continua a saga até o frame correto
    container=(
        driver
        .find_element(
            selenium.webdriver.common.by.By.CSS_SELECTOR,
            "sfc-shell#shell"
        )
        .find_element(
            selenium.webdriver.common.by.By.CSS_SELECTOR,
            "waypoint-bmprog"
        )
        .shadow_root
        .find_element(
            selenium.webdriver.common.by.By.CSS_SELECTOR,
            "iframe#BMPROG"
        )
    )

    (
    	selenium.webdriver.support.ui.WebDriverWait(driver, 15).until(
            selenium.webdriver.support
            .expected_conditions
            .frame_to_be_available_and_switch_to_it(container)
        )
    )

    tab_navigator = driver.current_window_handle

    current = datetime.date.today()

    # Manipula os seletores de ano e mês para extrair metadados dos demonstrativos
    for year in range(current.year, start_year - 1, -1):
        # Seta o ano
        selenium.webdriver.support.ui.Select(
            driver
            .find_element(
                selenium.webdriver.common.by.By.CSS_SELECTOR,
                "select#vt_ano"
            )
        ).select_by_value(str(year))

        for month in range(current.month if current.year == year else 12, 0, -1):
            # Seta o mês
            selenium.webdriver.support.ui.Select(
                driver
                .find_element(
                    selenium.webdriver.common.by.By.CSS_SELECTOR,
                    "select#vt_mes"
                )
            ).select_by_value(f"{month:02d}")

            driver.implicitly_wait(2)

            # Pega as linhas certas da tabela
            rows = driver.find_elements(selenium.webdriver.common.by.By.CSS_SELECTOR, "table:nth-of-type(3) tr")

            if not len(rows)>=3:
                continue

            # Só continua se há demonstrativos nesse mês
            for i in range(3,len(rows)+1):
                cols = driver.find_elements(
                    selenium.webdriver.common.by.By.CSS_SELECTOR,
                    f"table:nth-of-type(3) tr:nth-of-type({i}) td"
                )

                if len(cols)!=4:
                    continue

                # Só continua se há o número certo de colunas
                # Coleta URL e metadados de todos os demonstrativos do mês
                # selecionado e guarda na lista de demonstrativos.
                demonstrativos.append(types.SimpleNamespace(
                    url          = urllib.parse.urljoin(
                        driver.current_url,
                        (
                            cols[0].find_element(
                                selenium.webdriver.common.by.By.CSS_SELECTOR,
                                "a"
                            ).get_attribute("href")
                        )
                    ),
                    codigo       = int(cols[0].text.strip()),
                    tipo         = cols[1].text.strip(),
                    competencia  = [
                        datetime.datetime.strptime(t, '%d/%m/%Y').date()
                        for t in cols[2].text.strip().split(' a ')
                    ],
                    pagamento    = datetime.datetime.strptime(cols[3].text.strip(), '%d/%m/%Y').date(),
                ))

    # Com os metadados de cada demonstrativo disponíveis, vamos extrair cada
    # demonstrativo em sí, acessando sua URL específica
    header_referer = dict(headers=dict(Referer=adp_url()))
    for demonstrativo in demonstrativos:
        # ADP se protege e exige requisição HTTP com referer, então mandamos o referer
        driver.execute_cdp_cmd("Network.enable", {})
        driver.execute_cdp_cmd("Network.setExtraHTTPHeaders", header_referer)
        driver.get(demonstrativo.url)

        driver.implicitly_wait(2)

        # Apaga um objeto visual interativo de sumarização, inútil para nossos PDFs
        try:
            driver.execute_script(
                "arguments[0].remove();",
                (
                    driver
                    .find_element(
                        selenium.webdriver.common.by.By.CSS_SELECTOR,
                        "div.total-layer"
                    )
                )
            )
        except selenium.common.exceptions.NoSuchElementException:
            pass

        # Extrai versão PDF da página
        demonstrativo.pdf = base64.b64decode(
            driver.execute_cdp_cmd(
                "Page.printToPDF",
                dict(
                    printBackground = False,
                    landscape = False,
                )
            )['data']
        )

        # Encontra as tabelas
        demonstrativo.tables = (
            driver
            .find_element(
                selenium.webdriver.common.by.By.TAG_NAME,
                "form"
            )
            .find_elements(
                selenium.webdriver.common.by.By.XPATH,
                "./table"
            )
        )

        # Converte objetos Selenium das tabelas encontradas em objetos
        # BeautifulSoup, e assim nos desprendemos do browser.
        demonstrativo.tables = [
            bs4.BeautifulSoup(t.get_attribute("outerHTML"), "html.parser")
            for t in demonstrativo.tables
        ]

        # As tabelas extraidas:
        # {
        #     0: 'inutil',
        #     1: 'dados da empresa',
        #     2: 'dados do funcionário',
        #     3: 'banco e sumário',
        #     4: 'vazio',
        #     5: {
        #         2: 'dados',
        #         4: 'dados outros'
        #     },
        #     6: 'sumarização',
        #     7: 'vazio',
        #     8: 'vazio',
        #     9: 'vazio'
        # }

    # Não precisamos mais do browser
    driver.quit()

    # Retorna uma lista de dicts de demonstrativos extraidos
    # dict(url, codigo, tipo, competencia, pagamento, pdf, tables)
    return demonstrativos



def contabil(demonstrativos):
    """
    Converte para formato contábil as tabelas BeautifulSoup extraídas de ADP.
    Cada dict da lista demonstrativos passará a conter a chave `contabil` com um
    pandas.DataFrame muito útil.
    """
    for d in demonstrativos:
        if not len(d.tables)>5:
            continue

        d.contabil = (
            # Importa tabela principal e já marca-a com seu tipo
            pandas.read_html(
                io=io.StringIO(str(d.tables[5].find_all('table')[2])),
                decimal=',',
                thousands='.'
            )[0]
            .assign(
                demonstrativo=d.tipo,
            )

            # Concatena com sub-tabela "OUTROS"
            .pipe(
                lambda table: (
                    pandas.concat(
                        [
                            table,
                            pandas.read_html(
                                io=io.StringIO(str(d.tables[5].find_all('table')[4])),
                                decimal=',',
                                thousands='.'
                            )[0]
                            .assign(
                                demonstrativo=d.tipo + " (outros)",
                            )
                        ]
                    )
                    .reset_index(drop=True)
                    if len(d.tables[5].find_all('table')[4].find_all('tr'))>0
                    else table
                )
            )

            # Elimina colunas puramente visuais, com '|'
            .drop(columns=[1,3,5,7])

            # Dá nome oficial às colunas
            .rename(
                columns={
                    0: 'conta',
                    2: 'quantidade',
                    4: 'entrada',
                    6: 'saida'
                }
            )

            .assign(
                # Adiciona colunas de categorização do informe
                cod=d.codigo,
                competencia_ini=d.competencia[0],
                competencia_fim=d.competencia[1],
                pagamento=d.pagamento,
                demonstrativo=lambda table: table.demonstrativo.astype('category'),
                conta=lambda table: table.conta.astype('category'),

                # Converte valores em dados contábeis
                valor=lambda table: table.entrada.combine_first(table.saida * -1)
            )

            # Retorna somente colunas relevantes e na ordem certa
            ["pagamento competencia_ini competencia_fim cod demonstrativo conta quantidade valor".split()]
        )

    return demonstrativos



def contabilidade_total(demonstrativos):
    # Tabela cotábil completa
    return (
        pandas.concat(
            [
                d.contabil
                for d in demonstrativos
                if hasattr(d,'contabil')
            ]
        )
        .reset_index(drop=True)
        .assign(
            conta=lambda table: table.conta.astype('category'),
            demonstrativo=lambda table: table.demonstrativo.astype('category'),
        )
    )



def save_pickle(demonstrativos, folder=pathlib.Path()):
    with (folder / 'demonstrativos.pkl').open('wb') as f:
        pickle.dump(demonstrativos, f)



def save_pdf(demonstrativos, folder=pathlib.Path()):
    for d in demonstrativos:
        with (folder / f"{d.pagamento:%Y.%m.%d} {d.tipo}.pdf").open('wb') as f:
            f.write(d.pdf)



def cli_args():
    true_set=("1", "true", "yes")
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--adp-user",
        default=os.getenv("ADP_USER"),
        help="ADP username (default: $ADP_USER environment variable)",
    )
    parser.add_argument(
        "--adp-password",
        default=os.getenv("ADP_PASSWORD"),
        help="ADP password (default: $ADP_PASSWORD environment variable)",
    )
    parser.add_argument(
        "--start-year",
        type=int,
        default=os.getenv("ADP_SINCE"),
        help="Começa a extração a partir deste ano (default: $ADP_SINCE ou ano passado)",
    )
    parser.add_argument(
        "--headless",
        action=argparse.BooleanOptionalAction,
        default=os.getenv("HEADLESS", "false").lower() in true_set,
        help="Executa o navegador (Chromium) sem janela nehuma (só que não funciona) (use --no-headless para ver o navegador trabalhando; default $HEADLESS ou falso)",
    )
    parser.add_argument(
        "--pdf",
        action=argparse.BooleanOptionalAction,
        default=os.getenv("PDF", "true").lower() in true_set,
        help="Salva PDFs dos demonstrativos (use --no-pdf para não salvar; default: $PDF ou salva sim)",
    )
    parser.add_argument(
        "--pickle",
        action=argparse.BooleanOptionalAction,
        default=os.getenv("PICKLE", "true").lower() in true_set,
        help="Salva arquivo Pickle com tudo o que foi extraido e dados processados (default: $PICKLE ou salva sim)",
    )
    parser.add_argument(
        "--output",
        type=pathlib.Path,
        default=os.getenv("OUTPUT", "./"),
        help="Pasta para escrever resultados (default: $OUTPUT ou pasta atual)",
    )
    parser.add_argument(
        "-d", "--debug",
        action=argparse.BooleanOptionalAction,
        default=os.getenv("DEBUG", "false").lower() in true_set,
        help="Debug mode",
    )

    args,_ = parser.parse_known_args()

    if not args.adp_user:
        parser.error("--adp-user ou $ADP_USER é mandatório")
    if not args.adp_password:
        parser.error("--adp-password ou $ADP_PASSWORD é mandatório")
    if not args.start_year:
        args.start_year=datetime.date.today().year - 1

    args.output.mkdir(parents=True, exist_ok=True)

    return args



def main():
    global debug

    dotenv.load_dotenv()

    args=cli_args()

    debug=args.debug

    driver=get_browser_chrome(args.headless)
    adp_login(driver,usuario=args.adp_user,senha=args.adp_password)
    adp_go_demonstrativos(driver)

    demonstrativos=adp_iterate_demonstrativos(driver,args.start_year)

    demonstrativos=contabil(demonstrativos)

    if args.pickle:
        save_pickle(demonstrativos, folder=args.output)

    if args.pdf:
        save_pdf(demonstrativos, folder=args.output)

    return demonstrativos



if __name__ == "__main__":
    main()