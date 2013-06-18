import json
import requests
from . import Resource, ResourceList, API_URL
from .directory import Directory
from stormpath.error import Error as StormpathError

class Account(Resource):
    path = 'accounts'
    fields = ['username', 'email', 'password', 'givenName',
            'middleName', 'surname', 'status',]

    def __str__(self):
        return self.username

    @staticmethod
    def prepare_data(data):
        clean_data = {}
        for k,v in data.items():
            if k == 'given_name':
                clean_data['givenName'] = v
            elif k == 'middle_name':
                clean_data['middleName'] = v
            else:
                clean_data[k] = v

        return clean_data

    @property
    def directory(self):
        self.read()
        url = self._data['directory']['href']
        directory = Directory(session=self._session, url=url)
        directory.read()
        return directory

    def add_group(self, group):
        from .group_membership import GroupMembership
        gm = GroupMembership(session=self._session, account=self, group=group)
        gm.save()
        return gm

    @property
    def groups(self):
        from .group import Group, GroupResourceList
        url = self._data['groups']['href']
        return GroupResourceList(url=url, session=self._session,\
                resource=Group, directory=self.directory)

    @property
    def group_memberships(self):
        from .group_membership import GroupMembership, GroupMembershipResourceList
        url = '%s/groupMemberships' % self.url
        return GroupMembershipResourceList(url=url, session=self._session,\
                resource=GroupMembership)

class AccountResourceList(ResourceList):
    def __init__(self, *args, **kwargs):
        if 'directory' in kwargs.keys():
            self._directory = kwargs.pop('directory')

        if 'group' in kwargs.keys():
            self._group = kwargs.pop('group')

        super(AccountResourceList, self).__init__(*args, **kwargs)

    def create(self, *args, **kwargs):
        if self._directory:
            # handle creation in directory
            url = '%sdirectories/%s/accounts' % (API_URL, self._directory.uid)

            if len(args) == 1:
                data = args[0]
            else:
                data = kwargs.get('data') or kwargs
            data = self._resource_class.prepare_data(data)

            resp = self._session.post(url, data=json.dumps(data))
            if resp.status_code not in (200, 201):
                raise StormpathError(error=resp.json())

            account = Account(session=self._session, data=resp.json())
            return account
        else:
            raise NotImplementedError
