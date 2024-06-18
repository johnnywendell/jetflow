import os

#python manage.py dumpdata romaneio.area --indent 4 > fixture/area.json
#python manage.py loaddata fixture/area.json --app romaneio.area

def dump_model():
    os.system("python manage.py dumpdata romaneio.area --indent 4 > fixture/area.json")

def dump_data():
    os.system("python manage.py dumpdata romaneio.area --indent 4 > fixture/area.json")
    os.system("python manage.py dumpdata romaneio.solicitante --indent 4 > fixture/solicitante.json")
    os.system("python manage.py dumpdata romaneio.romaneio --indent 4 > fixture/romaneio.json")
    os.system("python manage.py dumpdata material.material --indent 4 > fixture/material.json")
    os.system("python manage.py dumpdata material.tintafundo --indent 4 > fixture/tintafundo.json")
    os.system("python manage.py dumpdata material.tintaintermediaria --indent 4 > fixture/tintaintermediaria.json")
    os.system("python manage.py dumpdata material.tintaacabamento --indent 4 > fixture/tintaacabamento.json")
    os.system("python manage.py dumpdata material.tratamento --indent 4 > fixture/tratamento.json")
    os.system("python manage.py dumpdata qualidade.relatorioinspecao --indent 4 > fixture/relatorioinspecao.json")
    os.system("python manage.py dumpdata qualidade.etapapintura --indent 4 > fixture/etapapintura.json")
    os.system("python manage.py dumpdata qualidade.photo --indent 4 > fixture/photo.json")
    os.system("python manage.py dumpdata qualidade.assinatura --indent 4 > fixture/assinatura.json")
    os.system("python manage.py dumpdata auth.user --indent 4 > fixture/user.json")

def load_data():
    os.system("python manage.py loaddata fixture/user.json --app auth.user")
    os.system("python manage.py loaddata fixture/area.json --app romaneio.area")
    os.system("python manage.py loaddata fixture/solicitante.json --app romaneio.solicitante")
    os.system("python manage.py loaddata fixture/romaneio.json --app romaneio.romaneio")
    os.system("python manage.py loaddata fixture/tintafundo.json --app material.tintafundo")
    os.system("python manage.py loaddata fixture/tintaintermediaria.json --app material.tintaintermediaria")
    os.system("python manage.py loaddata fixture/tintaacabamento.json --app material.tintaacabamento")
    os.system("python manage.py loaddata fixture/tratamento.json --app material.tratamento")
    os.system("python manage.py loaddata fixture/material.json --app material.material ")
    os.system("python manage.py loaddata fixture/relatorioinspecao.json --app qualidade.relatorioinspecao")
    os.system("python manage.py loaddata fixture/etapapintura.json --app qualidade.etapapintura")
    #os.system("python manage.py loaddata fixture/photo.json --app qualidade.photo")
    #os.system("python manage.py loaddata fixture/assinatura.json --app qualidade.assinatura")

if __name__ == "__main__":
    dump_data()
    #load_data()


