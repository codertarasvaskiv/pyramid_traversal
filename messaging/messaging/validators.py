
def validate_corporation_data(request, **kwargs):
    try:
        json = request.json_body

        if not isinstance(json, dict) or 'data' not in json or not isinstance(json.get('data'), dict):
            request.errors.add('body', 'data', "Data not available")
            request.errors.status = 422
        else:
            request.validated['json_data'] = json['data']
            data = json['data']

            model = request.corporation_from_data(data, create=False)
            data = validate_data(request, model, data=data)
    except ValueError, e:
        request.errors.add('body', 'data', 'no json body was provided')
        request.errors.status = 422


def validate_data(request, model, partial=False, data=None):
    print('validating data')
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
            m.validate()
            method = m.serialize
            role = 'create'
    except Exception as e:
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