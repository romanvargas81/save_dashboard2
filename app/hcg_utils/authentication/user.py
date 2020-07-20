class User:
    def __init__(self, authenticated=False, roles=None, identifier=None):
        self.authenticated = authenticated
        self.identifier = identifier
        self.first_name = None
        self.last_name = None
        if roles is None:
            self._roles = {}
        else:
            self._roles = roles

    def check(self, resource, permission):
        if self.authenticated is not True:
            return False
        return (resource, permission) in self._roles
