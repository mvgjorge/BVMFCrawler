import string
import sys
import requests
import os
import unicodedata
from bs4 import BeautifulSoup

DOCUMENTS_URL = 'http://bvmf.bmfbovespa.com.br/Fundos-Listados/FundosListadosDetalhe.aspx?Sigla={}' \
                '&tipoFundo=Imobiliario&aba=subAbaDocumento&idioma=pt-br'

DEMOFINANCEIRAS_URL = 'http://bvmf.bmfbovespa.com.br/Fundos-Listados/FundosListadosDetalhe.aspx?sigla={}' \
                      'b&tipoFundo=Imobiliario&aba=subAbaDemonstracoesFinanceiras&idioma=pt-br'

OUTROSDOCS_URL = 'http://bvmf.bmfbovespa.com.br/Fundos-Listados/FundosListadosDetalhe.aspx?Sigla={}' \
                 '&tipoFundo=Imobiliario&aba=subAbaOutrosDocumentos&idioma=pt-br'


validFilenameChars = "-_.() %s%s" % (string.ascii_letters, string.digits)


def remove_disallowed_filename_chars(filename):
    return "".join([x if x.isalnum() else "_" for x in filename])


# given a PDF url, download the document to the folder specifiec
def download_file(url, local_filename, folder):
    encoded_file = remove_disallowed_filename_chars(local_filename);
    path = os.path.join(folder, encoded_file + '.pdf')
    if os.path.isfile(path):
        return
    print("Fazendo download de {}".format(encoded_file))
    r = requests.get(url, stream=True)
    with open(path, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    return local_filename


# connect to BVMF pages and get all downloads links
def get_documents(url, folder):
    html_page = requests.get(url)
    soup = BeautifulSoup(html_page.content, "html.parser")
    for link in soup.findAll('a'):
        doc = link.get('href')
        if 'FormConsultaPdfDocumentoFundos' in doc:
            download_file(doc, link.string, folder)


# creates all folders that will store the documents
def create_folders(rootfolder):
    fullpath = os.path.join(rootfolder, "DOCUMENTS")
    if not os.path.exists(fullpath):
        os.makedirs(fullpath)
    fullpath = os.path.join(rootfolder, "DEMOFINANCEIRAS")
    if not os.path.exists(fullpath):
        os.makedirs(fullpath)
    fullpath = os.path.join(rootfolder, "OUTROSDOCS")
    if not os.path.exists(fullpath):
        os.makedirs(fullpath)


def main():
    fundo = sys.argv[1]
    rootfolder = sys.argv[2]
    create_folders(rootfolder)
    url = DOCUMENTS_URL.format(fundo)
    get_documents(url, os.path.join(rootfolder, "DOCUMENTS"))
    url = DEMOFINANCEIRAS_URL.format(fundo)
    get_documents(url, os.path.join(rootfolder, "DEMOFINANCEIRAS"))
    url = OUTROSDOCS_URL.format(fundo)
    get_documents(url, os.path.join(rootfolder, "OUTROSDOCS"))


if __name__ == '__main__':
    main()
