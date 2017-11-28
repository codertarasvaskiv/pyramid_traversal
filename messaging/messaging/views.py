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
from .validators import validate_create_corporation_data, validate_patch_corporation_data
from .utils import apply_patch, generate_id, save_corporation


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

    @view(content_type="application/json", permission='view_list')
    def get(self):
        view_map = self.VIEW_MAP
        list_view = view_map[u'_all_']
        view = partial(list_view, self.db)

        results = [
            i['value'] for i in view()
        ]
        data = {
            'data': results
        }
        return data

    @view(content_type="application/json", permission='create', validators=(validate_create_corporation_data,))
    def post(self):
        corporation = self.request.validated['corporation']
        corporation.id = generate_id()
        corporation.store(self.request.registry.db)
        return {
            'data': {'owner_token': corporation.owner_token}
        }


@resource(name='Corporation', path='/corp/{corp_id}', factory=root_factory)
class CorporationResourse(MainResource):
    def __init__(self, request, context):
        super(CorporationResourse, self).__init__(request, context)

    # def __acl__(self):
    #     return [(Deny, Everyone, 'view')]
    @view(content_type="application/json", permission='view_one')
    def get(self):
        return {
            "data": self.context.serialize('view_one')
        }

    @view(content_type="application/json", permission='edit', validators=(validate_patch_corporation_data,))
    def patch(self):
        corp = self.context

        apply_patch(self.request, save=False, src=self.request.validated['corp_src'])

        save_corporation(self.request)

        return {
            'data': 'success update'
        }


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
