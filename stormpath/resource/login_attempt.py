from base64 import b64encode
from .base import Resource, CollectionResource


class AuthenticationResult(Resource):
    """Handles Base64-encoded login data.

    More info in documentation:
    https://www.stormpath.com/docs/rest/product-guide#AuthenticateAccounts
    """

    writable_attrs = ('type', 'value')

    def get_resource_attributes(self):
        from .account import Account
        return {
            'account': Account
        }

    def __repr__(self):
        return '<%s attributes=%s>' % (self.__class__.__name__,
            str(self._get_property_names()))


class LoginAttemptList(CollectionResource):
    """List of login data.
    """
    resource_class = AuthenticationResult

    def basic_auth(self, login, password):
        value = login + ':' + password
        value = b64encode(value.encode('utf-8')).decode('ascii')
        return self.create({
            'type': 'basic',
            'value': value
        })
