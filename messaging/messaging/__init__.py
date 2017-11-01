"""Main entry point
"""
from couchdb import Server as CouchdbServer
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.config import Configurator

from .security import groupfinder

from .models import Corporation
from .utils import extract_corporation, corporation_from_data
from .traversal import root_factory

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)

    # security policies
    authn_policy = AuthTktAuthenticationPolicy(
        settings['messaging.secret'], callback=groupfinder, hashalg='sha512'
    )
    authz_policy = ACLAuthorizationPolicy()
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)

    config.set_root_factory(root_factory)

    config.add_request_method(extract_corporation, 'corporation', reify=True)
    config.add_request_method(corporation_from_data)
    config.registry.model = Corporation



    #  database settings
    server = CouchdbServer(settings['couchdb.uri'])
    config.registry.couchdb_server = server
    if settings['couchdb.db'] not in server:
        server.create(settings['couchdb.db'])
    config.registry.db = server[settings['couchdb.db']]


    config.include('cornice')
    config.include('pyramid_jinja2')
    config.include('.routes')


    config.add_static_view('static', 'static', cache_max_age=3600)

    config.scan()
    # config.add_view('messaging.traversal.root_factory', renderer='json')
    # config.add_view('messaging.views.my_view', renderer='json')
    #config.add_view('messaging.views.my_view', renderer='json')
    # config.add_route('home', '/')
    # config.scan()
    return config.make_wsgi_app()



#
# def main(global_config, **settings):
#     config = Configurator(settings=settings, root_factory=get_root)
#     config.registry.db = Server(uri=settings['couchdb.db'])
#
#
#     config.add_view(hello_world_of_resources, context=Root)
#
#     def add_couchdb(request):
#         db = config.registry.db.get_or_create_db(settings['couchdb.db'])
#         return db
#
#     config.add_request_method(add_couchdb, 'db', reify=True)
#     config.include("cornice")
#     config.scan("messaging.views")
#     return config.make_wsgi_app()
#


# from pyramid.config import Configurator
# from couchdbkit import *
#
#
# def main(global_config, **settings):
#     config = Configurator(settings=settings)
#
#     config.registry.db = Server(uri=settings['couchdb.db'])
#
#     def add_couchdb(request):
#         db = config.registry.db.get_or_create_db(settings['couchdb.db'])
#         return db
#
#     config.add_request_method(add_couchdb, 'db', reify=True)
#
#     config.include("cornice")
#     config.scan("messaging.views")
#     return config.make_wsgi_app()

