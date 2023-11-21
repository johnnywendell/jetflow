# utils.py

import csv
from datetime import datetime
import os

def converter_afd_para_csv(arquivos_afd, saida_csv):
    with open(saida_csv, 'w', newline='') as arquivo_csv:
        escritor_csv = csv.writer(arquivo_csv)

        # Escreve o cabeçalho do CSV
        escritor_csv.writerow(['Arquivo', 'NSR', 'Tipo de Registro', 'Data', 'Hora', 'PIS'])

        # Itera sobre os arquivos AFD
        for arquivo_afd in arquivos_afd:
            nome_arquivo = os.path.splitext(os.path.basename(arquivo_afd))[0]
            with open(arquivo_afd, 'r') as arquivo_afd_leitura:
                linhas_afd = arquivo_afd_leitura.readlines()

                # Itera sobre as linhas do AFD e converte para CSV
                for linha in linhas_afd:
                    if len(linha) == 35:
                        nsr = linha[0:9].strip()
                        tipo_registro = linha[9]
                        data_str = linha[10:18]
                        hora_minuto_str = linha[18:22]
                        pis = linha[22:34]

                        try:
                            data = datetime.strptime(data_str, '%d%m%Y').strftime('%Y-%m-%d')
                        except ValueError:
                            data = None

                        hora_minuto = hora_minuto_str[:2] + ':' + hora_minuto_str[2:]

                        # Escreve a linha no arquivo CSV com o nome do arquivo
                        escritor_csv.writerow([nome_arquivo, nsr, tipo_registro, data, hora_minuto, pis])
                    else:
                        # Imprime '**' se o tamanho da linha for diferente de 34
                        print(f"** Linha pulada no arquivo {nome_arquivo} - Tamanho incorreto:", len(linha), " - Conteúdo:", linha.strip())
