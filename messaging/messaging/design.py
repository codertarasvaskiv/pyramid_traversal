from couchdb.design import ViewDefinition

def add_index_options(doc):
    doc['options'] = {'local_seq': True}


def sync_design(db):
    views = [j for i, j in globals().items() if "_view" in i]
    ViewDefinition.sync_many(db, views, callback=add_index_options)

FIELDS = [
    '_id',
    'name',
    #'title'
]

corporation_all_view = ViewDefinition('corporations', 'all', '''function(doc) {
    if(doc.doc_type == 'Corporation') {
        var fields=%s, data={};
        for (var i in fields) {
            if (doc[fields[i]]) {
                data[fields[i]] = doc[fields[i]]
            }
        }
        emit(doc._id, data);
    }
}''' % FIELDS )
corporation_all_view2 = ViewDefinition('corporations', 'all2', '''function(doc) {
    if(doc.doc_type == 'Corporation2') {
        emit(doc.tenderID, null);
    }
}''')

VIEW_MAP = {
    u'_all_': corporation_all_view
}
