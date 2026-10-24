FROM fedora

ENV ADP_USER \
    ADP_PASSWORD \
    ADP_SINCE \
    HEADLESS \
    PDF \
    PICKLE \
    DEBUG


RUN    dnf -y --setopt=tsflags=nodocs --setopt=install_weak_deps=False upgrade \
    && dnf -y --setopt=tsflags=nodocs --setopt=install_weak_deps=False install \
            selenium-manager \
            chromium \
            chromium-headless \
            chromedriver \
            python-unversioned-command \
            python3-pandas \
            python3-beautifulsoup4 \
            python3-selenium \
            python3-dotenv \
            python3-dotenv+cli
    && dnf clean all \
    && useradd -m extractor

USER extractor
WORKDIR /home/extractor

ADD adpscrape.py

CMD ["python","adpscrape.py"]