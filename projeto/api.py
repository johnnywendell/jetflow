from ninja import NinjaAPI

from material.material_api import router as material_router
#from backend.servico.servico_api import router as servico_router

api = NinjaAPI(csrf=True)

api.add_router('/material/', material_router)
#api.add_router('/servico/', servico_router)