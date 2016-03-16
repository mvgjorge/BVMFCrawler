import sys
import requests
from bs4 import BeautifulSoup

DOCUMENTS_URL = 'http://bvmf.bmfbovespa.com.br/Fundos-Listados/FundosListadosDetalhe.aspx?Sigla={}' \
                '&tipoFundo=Imobiliario&aba=subAbaDocumento&idioma=pt-br'

DEMOFINANCEIRAS_URL = 'http://bvmf.bmfbovespa.com.br/Fundos-Listados/FundosListadosDetalhe.aspx?sigla={}' \
                      'b&tipoFundo=Imobiliario&aba=subAbaDemonstracoesFinanceiras&idioma=pt-br'

OUTROSDOCS_URL = 'http://bvmf.bmfbovespa.com.br/Fundos-Listados/FundosListadosDetalhe.aspx?Sigla={}' \
                 '&tipoFundo=Imobiliario&aba=subAbaOutrosDocumentos&idioma=pt-br'


def download_file(url, local_filename):
    print("Fazendo download de {}".format(local_filename))
    path = local_filename.replace('/', ' ') + '.pdf'
    r = requests.get(url, stream=True)
    with open(path, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    return local_filename


def get_documents(url):
    html_page = requests.get(url);
    soup = BeautifulSoup(html_page.content, "html.parser")
    for link in soup.findAll('a'):
        doc = link.get('href')
        if 'FormConsultaPdfDocumentoFundos' in doc:
            download_file(doc, link.string)


def main():
    fundo = sys.argv[1]
    url = DOCUMENTS_URL.format(fundo);
    get_documents(url)
    url = DEMOFINANCEIRAS_URL.format(fundo);
    get_documents(url)
    url = OUTROSDOCS_URL.format(fundo);
    get_documents(url)


if __name__ == '__main__':
    main()
