from rolepermissions.roles import AbstractUserRole

class Inspetor(AbstractUserRole):
    available_permissions = {'ass_inspetor':True}

class Coordenador(AbstractUserRole):
    available_permissions = {'ass_coordenador':True}

class Fiscal(AbstractUserRole):
    available_permissions = {'ass_fiscal':True}

class Medidor(AbstractUserRole):
    available_permissions = {'ass_medidor':True}

class Encarregado(AbstractUserRole):
    available_permissions = {'ass_encarregado':True}

class Planejador(AbstractUserRole):
    available_permissions = {'ass_planejador':True}

class Gerencia(AbstractUserRole):
    available_permissions = {'all_permissions':True}

#################  view roles

class Rdo(AbstractUserRole):
    available_permissions = {'ass_rdo':True}

class Rdodetail(AbstractUserRole):
    available_permissions = {'ass_rdodetail':True}

class Bms(AbstractUserRole):
    available_permissions = {'ass_bms':True}