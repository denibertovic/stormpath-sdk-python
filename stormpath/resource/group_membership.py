import json
import requests
from .base import Resource, ResourceList, API_URL
from .group import Group
from .account import Account

class GroupMembership(Resource):
    # FIXME: special case, resolve related_fields handling
    path = 'groupMemberships'
    fields = []
    related_fields = ['account', 'group']

    def __init__(self, *args, **kwargs):
        super(GroupMembership, self).__init__(*args, **kwargs)

    @property
    def account(self):
        return self._related_data.get('account')

    @property
    def group(self):
        return self._related_data.get('group')

    def save(self):
        # FIXME: resolve handling of account/group after save in _data
        # FIXME: resolve loading from url and object
        url = '%s%s' % (API_URL, self.path)
        account_url = group_url = None

        data = {
            "account" : {"href": self.account.url},
            "group" : {"href": self.group.url},
        }

        resp = self._session.post(url, data=json.dumps(data))
        if resp.status_code not in (200, 201):
            raise Exception(resp.json())

        self._data = resp.json()
        self.url = self._data['href']

class GroupMembershipResourceList(ResourceList):
    pass
