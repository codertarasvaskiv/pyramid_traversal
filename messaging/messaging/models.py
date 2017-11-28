from pyramid.security import (
    ALL_PERMISSIONS,
    Allow,
    Deny,
    Everyone,
)
from couchdb_schematics.document import SchematicsDocument
from schematics.models import Model as SchematicsModel
from schematics.transforms import blacklist, convert, export_loop
from schematics.types import BaseType, StringType
from schematics.types.compound import DictType, ListType, ModelType
from schematics.types.serializable import serializable

from .utils import get_now, IsoDateTimeType


schematics_embedded_role = SchematicsDocument.Options.roles['embedded'] + blacklist("__parent__")





class Model(SchematicsModel):
    class Options(object):
        """Export options for Document."""
        serialize_when_none = False

    def to_patch(self, role=None):
        """
        Return data as it would be validated. No filtering of output unless
        role is defined.
        """
        field_converter = lambda field, value: field.to_primitive(value)
        data = export_loop(self.__class__, self, field_converter, role=role, raise_error_on_role=True, print_none=True)
        return data


class Revision(Model):
    author = StringType()
    date = IsoDateTimeType(default=get_now)
    changes = ListType(DictType(BaseType), default=list())
    rev = StringType()


class Department(Model):

    depName = StringType()
    depTitle = StringType()

    def __acl__(self):
        return [(Allow, Everyone, 'everything')]

class Corporation(SchematicsDocument, Model):

    class Options:
        roles = {
            'plain': (blacklist('_attachments', 'revisions', 'dateModified') + schematics_embedded_role),
            'create': blacklist('_id', '_rev', 'doc_type'),
            'view_one': (blacklist('_rev', '_id', 'doc_id', 'doc_type', 'revisions') + SchematicsDocument.Options.roles['embedded'] + blacklist("__parent__")),
            'public': blacklist('_id', '_rev', 'doc_type'),
            'edit': blacklist('owner_token')
        }

    departments = ListType(ModelType(Department), default=list(), required=False)
    name = StringType()
    title = StringType()

    dateModified = IsoDateTimeType()
    revisions = ListType(ModelType(Revision), default=list())
    owner_token = StringType()
    _id = StringType()
    _rev = StringType()
    doc_type = StringType()

    def __acl__(self):
        acl = []
        acl.extend([
            # allow/deny     group                permission
            (Allow, 'editors', 'edit'),
            (Allow, '{}'.format(self.owner_token), 'edit'),
            (Allow, '{}'.format(self.owner_token), 'view_one')
        ])
        return acl

    def __local_roles__(self):
        roles = dict([('{}'.format(self.owner_token), 'edit')])
        return roles

    # sometimes we need role before we go to view
    # example validator. Patch validator makes some stuff.
    # thats why we need authenticated role function and ger_role function
    def get_role(self):
        root = self.__parent__
        request = root.request
        if request.authenticated_role == 'edit':
            role = 'edit'
        elif request.authenticated_role == 'create':
            role = 'create'
        elif request.authenticated_role == 'admin':
            role = 'admin'
        else:
            role = 'view_list'
        return role


    def import_data(self, raw_data, **kw):
        """
        Converts and imports the raw data into the instance of the model
        according to the fields in the model.
        :param raw_data:
            The data to be imported.
        """
        data = self.convert(raw_data, **kw)
        del_keys = [k for k in data.keys() if
                    data[k] == self.__class__.fields[k].default or data[k] == getattr(self, k)]
        for k in del_keys:
            del data[k]
        self._data.update(data)
        return self






class Employee(object):
    pass

