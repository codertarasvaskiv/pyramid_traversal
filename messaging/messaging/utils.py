import os
from cornice.util import json_error
from couchdb.http import ResourceConflict
from datetime import datetime
from iso8601 import parse_date, ParseError
from jsonpatch import make_patch, apply_patch as _apply_patch
from pyramid.exceptions import URLDecodeError
from pyramid.compat import decode_path_info
from pytz import timezone
from schematics.exceptions import ConversionError, ModelValidationError
from schematics.types import BaseType
from uuid import uuid4
from webob.multidict import NestedMultiDict

TZ = timezone(os.environ['TZ'] if 'TZ' in os.environ else 'Europe/Kiev')


def apply_patch(request, data=None, save=True, src=None):
    import pdb;pdb.set_trace()
    data = request.validated['data'] if data is None else data
    patch = data and apply_data_patch(src or request.context.serialize(), data)
    if patch:
        request.context.import_data(patch)
        if save:
            return save_corporation(request)

def apply_data_patch(item, changes):
    patch_changes = []
    prepare_patch(patch_changes, item, changes)
    if not patch_changes:
        return {}
    return _apply_patch(item, patch_changes)

def prepare_patch(changes, orig, patch, basepath=''):
    if isinstance(patch, dict):
        for i in patch:
            if i in orig:
                prepare_patch(changes, orig[i], patch[i], '{}/{}'.format(basepath, i))
            else:
                changes.append({'op': 'add', 'path': '{}/{}'.format(basepath, i), 'value': patch[i]})
    elif isinstance(patch, list):
        if len(patch) < len(orig):
            for i in reversed(range(len(patch), len(orig))):
                changes.append({'op': 'remove', 'path': '{}/{}'.format(basepath, i)})
        for i, j in enumerate(patch):
            if len(orig) > i:
                prepare_patch(changes, orig[i], patch[i], '{}/{}'.format(basepath, i))
            else:
                changes.append({'op': 'add', 'path': '{}/{}'.format(basepath, i), 'value': j})
    else:
        for x in make_patch(orig, patch).patch:
            x['path'] = '{}{}'.format(basepath, x['path'])
            changes.append(x)




def corporation_from_data(request, data, raise_error=True, create=True):
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

def request_params(request):
    try:
        params = NestedMultiDict(request.GET, request.POST)
    except UnicodeDecodeError:
        request.errors.add('body', 'data', 'could not decode params')
        request.errors.status = 422
        raise json_error(request.errors)
    except Exception, e:
        request.errors.add('body', str(e.__class__.__name__), str(e))
        request.errors.status = 422
        raise json_error(request.errors)
    return params

def save_corporation(request):
    corp = request.validated['corporation']

    patch = make_patch(corp.serialize("plain"), request.validated['corp_src']).patch
    import pdb;pdb.set_trace()
    if patch:
        now = get_now()

        corp.revisions.append(type(corp).revisions.model_class({
            'author': request.authenticated_userid,
            'changes': patch,
            'rev': corp.rev
        }))
        # old_dateModified = corp.dateModified
        # if getattr(corp, 'modified', True):
        #     corp.dateModified = now
        try:
            corp.store(request.registry.db)
        except ModelValidationError, e:
            for i in e.message:
                request.errors.add('body', i, e.message[i])
            request.errors.status = 422
        except ResourceConflict, e:  # pragma: no cover
            request.errors.add('body', 'data', str(e))
            request.errors.status = 409
        except Exception, e:  # pragma: no cover
            request.errors.add('body', 'data', str(e))
        else:
            # here is logger thing
            return True


def get_now():
    return datetime.now(TZ)

class IsoDateTimeType(BaseType):
    MESSAGES = {
        'parse': u'Could not parse {0}. Should be ISO8601.',
    }

    def to_native(self, value, context=None):
        if isinstance(value, datetime):
            return value
        try:
            date = parse_date(value, None)
            if not date.tzinfo:
                date = TZ.localize(date)
            return date
        except ParseError:
            raise ConversionError(self.messages['parse'].format(value))
        except OverflowError as e:
            raise ConversionError(e.message)

    def to_primitive(self, value, context=None):
        return value.isoformat()
