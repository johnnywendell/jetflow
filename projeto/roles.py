from rolepermissions.roles import AbstractUserRole

class Inspetor(AbstractUserRole):
    available_permissions = {'ass_inspetor':True}

class Coordenador(AbstractUserRole):
    available_permissions = {'ass_coordenador':True}

class Fiscal(AbstractUserRole):
    available_permissions = {'ass_fiscal':True}

class Medidor(AbstractUserRole):
    available_permissions = {'ass_medidor':True}

class Planejador(AbstractUserRole):
    available_permissions = {'ass_planejador':True}

class Gerencia(AbstractUserRole):
    available_permissions = {'all_permissions':True}