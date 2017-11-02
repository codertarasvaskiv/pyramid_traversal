from cornice.resource import resource, view
from couchdb_schematics.document import SchematicsDocument
from pyramid.security import (
    ALL_PERMISSIONS,
    Allow,
    Deny,
    Everyone,
    remember,
    forget
)
from pyramid.httpexceptions import HTTPBadRequest
from pyramid.view import view_config
from .models import Corporation
from .traversal import Root, root_factory
from .validators import validate_corporation_data
from .utils import generate_id


_CORPORATIONS = {1: {'name': 'gawel'}, 2: {'name': 'tarek'}}



@view_config(context=Root, renderer='json')
def view_root(context, request):
    return {'key': 'this is root'}


@resource(name='Corporations', path='/corp', factory=root_factory)
class CorporationResourse(object):

    def __init__(self, request, context):
        print('self init was called')
        self.server = request.registry.couchdb_server
        self.context = context
        self.request = request
        self.db = request.registry.db
        #self.server_id = request.registry.server_id


    # def __getitem__(self, key):
    #     dept = Department()
    #     dept.id = key
    #     return dept

    def __acl__(self):
        return [(Allow, Everyone, 'everything')]

    def collection_get(self):
        print 'collection get'
        return {'corporations': _CORPORATIONS.keys()}

    def get(self):
        print 'simple get'
        return dict(self.context.__dict__['_data'])

    def collection_post(self):
        print('collection post')
        # _CORPORATIONS[len(_CORPORATIONS) + 1] = self.request.json_body
        # return True
        corporation = self.request.validated['corporation']
        corporation.id = generate_id()
        corporation.store(self.request.registry.db)
        return True

    @view(content_type="application/json", validators=(validate_corporation_data,))
    def post(self):
        print(self.request.validated, ' self.request.validated')
        corporation = self.request.validated['corporation']
        corporation.id = generate_id()
        corporation.store(self.request.registry.db)
        return True


    def patch(self):
        print('patch 42')
        self.context.__dict__['_data']['name'] = 'new name'
        print(type(self.context))
        self.context.store(self.db)




@resource(collection_path='/corp/{corp_id}/dep', path='/corp/{corp_id}/dep/{dep_id}', factory=root_factory)
class DepartmentResourse(object):

    def __init__(self, request, context):
        print('self init was called')
        self.context = context
        self.request = request
        self.db = request.registry.db


    # def __getitem__(self, key):
    #     dept = Department()
    #     dept.id = key
    #     return dept

    def __acl__(self):
        return [(Allow, Everyone, 'everything')]

    def collection_get(self):
        print 'collection get'
        return {'corporations': _CORPORATIONS.keys()}

    def get(self):
        print 'simple get'
        return dict(self.context.__dict__['_data'])

    def collection_post(self):
        print('collection post')
        _CORPORATIONS[len(_CORPORATIONS) + 1] = self.request.json_body
        return True

    def patch(self):
        print('patch 42')
        corporation = self.request.context
