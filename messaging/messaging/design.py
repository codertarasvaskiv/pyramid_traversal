from couchdb.design import ViewDefinition

def add_index_options(doc):
    doc['options'] = {'local_seq': True}


def sync_design(db):
    views = [j for i, j in globals().items() if "_view" in i]
    ViewDefinition.sync_many(db, views, callback=add_index_options)


corporation_all_view = ViewDefinition('corporations', 'all', '''function(doc) {
    if(doc.doc_type == 'Corporation') {
        emit(doc._id, {"name": doc.name, "title": doc.title});
    }
}''')
corporation_all_view2 = ViewDefinition('corporations', 'all2', '''function(doc) {
    if(doc.doc_type == 'Corporation2') {
        emit(doc.tenderID, null);
    }
}''')

VIEW_MAP = {
    u'_all_': corporation_all_view
}
