from django.urls import path
from qualidade import views as v
from django.contrib.auth.decorators import login_required
from usuarios.decorators import manager_required
from django.contrib.auth.decorators import login_required
from rolepermissions.decorators import has_role_decorator

app_name ='qualidade'

urlpatterns =[
    path('qualidade/', manager_required(v.RelatoriosList.as_view()), name='relatorios_list'),
    path('qualidade/edit/<int:pk>/', v.relatorios_edit, name='relatorios_update'),
    path('qualidade/edit/etapa/<int:pk>/', manager_required(v.EtapaUpdate.as_view()), name='etapas_update'),
    path('qualidade/<int:pk>/', v.relatorios_detail, name='relatorios_detail'),
    path('qualidade/add/', v.relatorios_add, name='relatorios_add'),
    path('photo/create/', v.photo_create, name='photo_create'),
    path('pdf/<int:pk>/', v.render_pdf_view, name='render_pdf_view'),
    path('photo/delete/<int:pk>', v.delete_photo, name='photo_delete'),
    path('ass/insp/<int:pk>', v.assign_insp, name='ass_insp'),
    path('ass/coord/<int:pk>', v.assign_coord, name='ass_coord'),
    path('ass/fiscal/<int:pk>', v.assign_fiscal, name='ass_fiscal'),

    path('qualidade/check/', login_required(v.Checklist_list.as_view()), name='check_list'),
    path('qualidade/checklist/<int:pk>', v.checklist_detail, name='checklist_detail'),
    path('qualidade/add/check', v.checklist_add, name='checklist_add'),
    path('qualidade/edit/check2/<int:pk>', v.checklist_edit, name='checklist_edit'),
    path('qualidade/edit/<int:pk>/check', has_role_decorator('inspetor')(v.ChecklistUpdate.as_view()), name='checklist_update'),
    path('qualidade/edit/etapa/<int:pk>/check', has_role_decorator('inspetor')(v.EtapacheckUpdate.as_view()), name='etapascheck_update'),
    path('photocheck/create/', v.photo_create_check, name='photo_create_check'),
    path('pdfcheck/<int:pk>/', v.render_pdf_view_check, name='render_pdf_view_check'),
    path('photocheck/delete/<int:pk>', v.delete_photo_check, name='delete_photo_check'),
    path('pdfchecksimple/<int:pk>/', v.render_pdf_view_check_simple, name='render_pdf_view_check_simple'),

    path('check/delete/<int:pk>', v.delete_checklist, name='checklist_delete'),
]
