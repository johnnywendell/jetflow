from datetime import date
from decimal import Decimal
from http import HTTPStatus
from typing import List
from django.db.models import Q

from django.shortcuts import get_object_or_404
from ninja import Router, Schema
from ninja.orm import create_schema

from .models import ItemBm, RDO

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
RdoSchema = create_schema(RDO, depth=1,fields=(
    'rdo',
    'unidade',
    'solicitante',
    'projeto_cod',
    'escopo',
))

@router.get('itembm/', response=List[MaterialSchema])
def list_material(request, search=None):
    if search:
        return ItemBm.objects.filter(descricao__icontains=search)
    return ItemBm.objects.all()
        #return ItemBm.objects.select_related('contrato').filter(descricao=search)
    #return ItemBm.objects.select_related('contrato').filter()
@router.get('itembm-item/', response=List[MaterialSchema])
def list_material(request, search=None):
    if search:
        return ItemBm.objects.filter(item_ref__icontains=search)
    return ItemBm.objects.all()

@router.get('rdo-solicitante/', response=List[RdoSchema])
def list_material(request, search=None):
    if search:
        return RDO.objects.filter(bm=None,aprovado=True,solicitante__solicitante__icontains=search)
    return RDO.objects.all(bm=None,aprovado=True,)

@router.get('rdo-unidade/', response=List[RdoSchema])
def list_material(request, search=None):
    if search:
        return RDO.objects.filter(bm=None,aprovado=True,unidade__area__icontains=search)
    return RDO.objects.all(bm=None,aprovado=True,)

@router.get('rdo-projeto/', response=List[RdoSchema])
def list_material(request, search=None):
    if search:
        return RDO.objects.filter(bm=None,aprovado=True,projeto_cod__projeto_nome__icontains=search)
    return RDO.objects.all(bm=None,aprovado=True,)

@router.get('rdo-escopo/', response=List[RdoSchema])
def list_material(request, search=None):
    if search:
        return RDO.objects.filter(bm=None,aprovado=True,escopo__icontains=search)
    return RDO.objects.all(bm=None,aprovado=True,)