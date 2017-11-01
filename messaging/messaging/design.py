from couchdb.design import ViewDefinition



corporation_all_view = ViewDefinition('tenders', 'all', '''function(doc) {
    if(doc.doc_type == 'Tender') {
        emit(doc.tenderID, null);
    }
}''')