from cornice.util import json_error
from .utils import generate_id


def validate_create_corporation_data(request, **kwargs):

    data = validate_json_data(request) # check if "data" is json type

    model = request.corporation_from_data(data, create=False)

    data = validate_data(request, model, data=data)

def validate_patch_corporation_data(request, **kwargs):

    data = validate_json_data(request)

    # additional logic with patch. In objects logic.


    #                                                 partial=True
    return validate_data(request, type(request.corporation), True, data)


def validate_data(request, model, partial=False, data=None):

    try:
        if partial and isinstance(request.context, model):
            initial_data = request.context.serialize()
            m = model(initial_data)
            m.__parent__ = request.context.__parent__
            m.validate()
            role = request.context.get_role()
            method = m.to_patch
        else:
            m = model(data)
            m.__parent__ = request.context
            m.owner_token = generate_id()
            m.validate()
            method = m.serialize
            role = 'create'
    except KeyError as e:
        request.errors.status = 422
    else:
        if hasattr(type(m), '_options') and role not in type(m)._options.roles:
            request.errors.add('url', 'role', 'Forbidden')
            request.errors.status = 403
        else:
            data = method(role)
            request.validated['data'] = data
            if not partial:
                m = model(data)
                m.__parent__ = request.context
                request.validated[model.__name__.lower()] = m
    return data



# here just validation if request.json_body is json type. Return json without "data" prefix.
# if there is error then return it with serialization
def validate_json_data(request):
    try:
        json = request.json_body
    except ValueError, e:
        request.errors.add('body', 'data', e.message)
        request.errors.status = 422
        raise json_error(request.errors)
    if not isinstance(json, dict) or 'data' not in json or not isinstance(json.get('data'), dict):
        request.errors.add('body', 'data', "Data not available")
        request.errors.status = 422
        raise json_error(request.errors)
    request.validated['json_data'] = json['data']
    return json['data']
