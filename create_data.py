import csv
import io
from datetime import datetime

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from romaneio.models import Romaneio
from material.models import Material

def save_data(data):
    '''
    Salva os dados no banco.
    '''
    aux = []
    for item in data:

        funcionario = item.get('funcionario')
        entrada = item.get('entrada')
        nf = str(item.get('nf'))
        romaneio = str(item.get('romaneio'))
        documento = str(item.get('documento'))
        obs = str(item.get('obs'))
        area = item.get('area')
        solicitante = item.get('solicitante')
        #importado = True if item.get('importado') == 'True' else False
        obj = Romaneio(
            funcionario=funcionario,
            entrada=entrada,
            nf=nf,
            romaneio=romaneio,
            documento=documento,
            obs=obs,
            area=area,
            solicitante=solicitante,
        )
        aux.append(obj)
    Romaneio.objects.bulk_create(aux)


def import_csv(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        # Lendo arquivo InMemoryUploadedFile
        file = myfile.read().decode('utf-8')
        reader = csv.DictReader(io.StringIO(file))
        # Gerando uma list comprehension
        data = [line for line in reader]
        save_data(data)
        return HttpResponseRedirect(reverse('romaneio:romaneio_list'))

    template_name = 'produto_import.html'
    return render(request, template_name)