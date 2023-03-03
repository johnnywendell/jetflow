from rolepermissions.roles import AbstractUserRole

class Inspetor(AbstractUserRole):
    available_permissions = {'ass_inspetor':True}

class Coordenador(AbstractUserRole):
    available_permissions = {'ass_coordenador':True}

class Fiscal(AbstractUserRole):
    available_permissions = {'ass_fiscal':True}
