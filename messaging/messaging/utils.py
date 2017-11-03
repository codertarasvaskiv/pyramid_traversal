from pyramid.exceptions import URLDecodeError
from pyramid.compat import decode_path_info
from uuid import uuid4



def corporation_from_data(request, data, raise_error=True, create=True):
    print('utils 7 def corporation_from_data ')
    model = request.registry.model
    if model is None and raise_error:
        request.errors.add('data', 'procurementMethodType', 'Not implemented')
        request.errors.status = 415
        raise "errors"
    if model is not None and create:
        model = model(data)
    return model

def extract_corporation_adapter(request, corporation_id):
    db = request.registry.db
    doc = db.get(corporation_id)
    if doc is not None and doc.get('doc_type') == 'corporation':
        request.errors.add('url', 'corporation_id', 'Archived')
        request.errors.status = 410
        raise "error"
    elif doc is None or doc.get('doc_type') != 'Corporation':
        request.errors.add('url', 'corporation_id', 'Not Found')
        request.errors.status = 404
        raise "error"

    return request.corporation_from_data(doc)



def extract_corporation(request):
    try:
        # empty if mounted under a path in mod_wsgi, for example
        path = decode_path_info(request.environ['PATH_INFO'] or '/')
    except KeyError:
        path = '/'
    except UnicodeDecodeError as e:
        raise URLDecodeError(e.encoding, e.object, e.start, e.end, e.reason)

    corporation_id = ""
    # extract tender id
    parts = path.split('/')
    if len(parts) < 3 or parts[1] != 'corp':
        return

    corporation_id = parts[2]
    return extract_corporation_adapter(request, corporation_id)


def generate_id():
    return uuid4().hex