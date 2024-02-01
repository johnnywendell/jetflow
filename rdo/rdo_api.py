from datetime import date
from decimal import Decimal
from http import HTTPStatus
from typing import List
from django.db.models import Q

from django.shortcuts import get_object_or_404
from ninja import Router, Schema, Query
from ninja.orm import create_schema

from .models import ItemBm, RDO, BoletimMedicao, QtdBM,QtdAS
from django.db.models import Sum

router = Router()

ItemSchema = create_schema(ItemBm, fields=(
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
BMSchema = create_schema(BoletimMedicao, depth=1,fields=(
    'bm_n',
    'd_numero',
    'b_numero',
    'valor',
    'd_aprovador',
))
class PlacaSchema(Schema):
    placa: str
    qtd_t: float
    qtd_e: float
    qtd_pranchao: float
    qtd_piso: float


@router.get('placa/', response=List[PlacaSchema])
def list_material(request, search: str = Query(None)):
    queryset = (
        QtdBM.objects.values('placa')
        .annotate(total_qtd_t=Sum('qtd_t'))
        .annotate(total_qtd_e=Sum('qtd_e'))
        .annotate(total_qtd_pranchao=Sum('qtd_pranchao'))
        .annotate(total_qtd_piso=Sum('qtd_piso'))
    )

    if search:
        # Filtra os resultados para a pesquisa fornecida
        queryset = queryset.filter(placa__icontains=search)

    results = []
    for item in queryset:
        results.append(PlacaSchema(
            placa=item['placa'] or "",
            qtd_t=item['total_qtd_t'] or 0.0,
            qtd_e=item['total_qtd_e'] or 0.0,
            qtd_pranchao=item['total_qtd_pranchao'] or 0.0,
            qtd_piso=item['total_qtd_piso'] or 0.0,
        ))

    return results

@router.get('itembm/', response=List[ItemSchema])
def list_material(request, search=None):
    if search:
        return ItemBm.objects.filter(descricao__icontains=search)
    return ItemBm.objects.all()
        #return ItemBm.objects.select_related('contrato').filter(descricao=search)
    #return ItemBm.objects.select_related('contrato').filter()

@router.get('itembm-item/', response=List[ItemSchema])
def list_material(request, search=None):
    if search:
        return ItemBm.objects.filter(item_ref__icontains=search)
    return ItemBm.objects.all()

@router.get('itembm-as/', response=List[ItemSchema])
def list_material(request, search=None, authServPk=None):
    if authServPk:
        return ItemBm.objects.filter(as_itens__a_s=authServPk,descricao__icontains=search)
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

@router.get('boletimmedicao/', response=List[BMSchema])
def list_bm(request, search=None):
    if search:
        return BoletimMedicao.objects.filter(frs=None).filter(Q(b_numero__icontains=search) | Q(d_numero__icontains=search))
    return BoletimMedicao.objects.all()