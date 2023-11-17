from datetime import date
from decimal import Decimal
from http import HTTPStatus
from typing import List

from django.shortcuts import get_object_or_404
from ninja import Router, Schema
from ninja.orm import create_schema

from .models import Material

router = Router()

MaterialSchema = create_schema(Material, fields=(
    'id',
    'n_romaneio',
    'material',
    'descricao',
    'polegada',
    'n_romaneio',
    'm_quantidade',
    'm2',
))

@router.get('material/', response=List[MaterialSchema])
def list_material(request, search=None):
    if search:
        #return Material.objects.filter(n_romaneio__istartswith=search)
        #Material.objects.select_related('n_romaneio').filter(concluido=True, relatorio=None,n_romaneio=search)
        return Material.objects.select_related('n_romaneio').filter(concluido=True, relatorio=None,n_romaneio=search)
    return Material.objects.select_related('n_romaneio').filter(concluido=True, relatorio=None)