from pyramid.security import (
    ALL_PERMISSIONS,
    Allow,
    Deny,
    Everyone,
    remember,
    forget
)


class Root(object):
    __parent__ = __name__ = None
    __acl__ = [
        (Deny, Everyone, 'edit'),
        #(Allow, 'group:editors', 'edit'),
    ]

    def __init__(self, request):
        self.request = request
        self.db = request.registry.db

    def __json__(self, request):
        return {'key': 'this is root'}

def root_factory(request):
    print("inside root_factory")
    request.validated['corp_src'] = {}
    root = Root(request)
    if not request.matchdict or not request.matchdict.get('corp_id'):
        return root
    request.validated['id'] = request.matchdict['corp_id']
    corporation = request.corporation
    print('traversal.py 33')
    corporation.__parent__ = root
    request.validated['corporation'] = request.validated['db_doc'] = corporation
    print('exit root_factory')
    return corporation