from cornice.resource import resource, view
from couchdb_schematics.document import SchematicsDocument
from functools import partial
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
from .design import VIEW_MAP
from .models import Corporation
from .traversal import Root, root_factory
from .validators import validate_corporation_data
from .utils import generate_id




@view_config(context=Root, renderer='json')
def view_root(context, request):
    return {'key': 'this is root'}



class MainResource(object):
    def __init__(self, request, context):
        self.server = request.registry.couchdb_server
        self.context = context
        self.request = request
        self.db = request.registry.db


@resource(name='Corporations', path='/corp', factory=root_factory)
class CorporationsResourse(MainResource):

    def __init__(self, request, context):
        super(CorporationsResourse, self).__init__(request, context)
        self.__acl__ = [(Allow, 'editor', 'view')]
        self.VIEW_MAP = VIEW_MAP

    def __acl__(self):
        return [
            (Allow, 'editor', 'view'),
            (Allow, 'g:admin', 'view'),
        ]

    @view(content_type="application/json")
    def get(self):
        view_map = self.VIEW_MAP
        list_view = view_map[u'_all_']
        view = partial(list_view, self.db)
        view()
        results = [
            {'id': i.id, 'name': i.value['name'], 'title': i.value['title']}  for i in view()
        ]
        data = {
            'data': results
        }
        return data


    @view(content_type="application/json", permission='create', validators=(validate_corporation_data,))
    def post(self):
        corporation = self.request.validated['corporation']
        corporation.id = generate_id()
        corporation.store(self.request.registry.db)
        return {
            'data': corporation.serialize()
        }


    def patch(self):
        print('patch 42')
        self.context.__dict__['_data']['name'] = 'new name'
        print(type(self.context))
        self.context.store(self.db)


@resource(name='Corporation', path='/corp/{corp_id}', factory=root_factory)
class CorporationResourse(MainResource):

    def __init__(self, request, context):
        super(CorporationResourse, self).__init__(request, context)

    def __acl__(self):
        return [(Deny, Everyone, 'view')]

    def get(self):
        #import pdb;pdb.set_trace()
        return {
            "data": self.context.serialize()
        }

    @view(content_type="application/json", validators=(validate_corporation_data,))
    def post(self):
        corporation = self.request.validated['corporation']
        corporation.id = generate_id()
        corporation.store(self.request.registry.db)
        return {
            'data': corporation.serialize()
        }

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
