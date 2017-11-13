from pyramid.security import (
    ALL_PERMISSIONS,
    Allow,
    Deny,
    Everyone,
)
from couchdb_schematics.document import SchematicsDocument
from schematics.models import Model as SchematicsModel
from schematics.transforms import blacklist, convert
from schematics.types import StringType
from schematics.types.compound import ListType, ModelType
from schematics.types.serializable import serializable



class Department(SchematicsModel):

    name = StringType()
    title = StringType()

    def __acl__(self):
        return [(Allow, Everyone, 'everything')]

class Corporation(SchematicsDocument, SchematicsModel):

    class Options:
        roles = {
            'create': (blacklist('id', 'doc_type')),
            'view': (blacklist('doc_type', '_rev', '_id') + SchematicsDocument.Options.roles['embedded'] + blacklist("__parent__")),
            'public': blacklist('_id', '_rev', 'doc_type')
        }

    departments = ListType(ModelType(Department), default=list())
    name = StringType()
    title = StringType()
    _id = StringType()
    _rev = StringType()
    doc_type = StringType()

    # def __acl__(self):
    #     return [(Allow, 'editor', 'view')]


    def import_data(self, raw_data, **kw):
        """
        Converts and imports the raw data into the instance of the model
        according to the fields in the model.
        :param raw_data:
            The data to be imported.
        """
        print("import data is called")
        data = raw_data
        del_keys = ['_id', '_rev', 'doc_type']
        for k in del_keys:
            del data[k]

        self._data.update(data)
        return self






class Employee(object):
    pass

