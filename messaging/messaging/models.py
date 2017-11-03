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
            'create': blacklist('id', 'doc_type'),
            'view': blacklist('doc_type', '_rev', '_id'),
        }

    departments = ListType(ModelType(Department), default=list())
    name = StringType()
    title = StringType()
    _id = StringType()
    _rev = StringType()
    doc_type = StringType()

    # def __init__(self, request, context=None):
    #     self.request = request

    # @serializable(serialized_name='id')
    # def doc_id(self):
    #     """A property that is serialized by schematics exports."""
    #     return self._id


    def __acl__(self):
        return [(Allow, Everyone, 'everything')]


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

