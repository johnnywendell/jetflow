from datetime import date
from decimal import Decimal
from http import HTTPStatus
from typing import List

from django.shortcuts import get_object_or_404
from ninja import Router, Schema
from ninja.orm import create_schema

from .models import ItemBm

router = Router()

MaterialSchema = create_schema(ItemBm, fields=(
    'id',
    'contrato',
    'item_ref',
    'disciplina',
    'descricao',
    'und',
    'preco_item',

))

@router.get('itembm/', response=List[MaterialSchema])
def list_material(request, search=None):
    if search:
        return ItemBm.objects.filter(descricao__istartswith=search)
    return ItemBm.objects.all()
        #return ItemBm.objects.select_related('contrato').filter(descricao=search)
    #return ItemBm.objects.select_related('contrato').filter()