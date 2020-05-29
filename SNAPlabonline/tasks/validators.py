from django.conf import settings
from django.core.exceptions import ValidationError
import json
from jsonschema import (
    validate, 
    exceptions as jsonschema_exceptions
)




def taskjson_validate(value,
    taskschema= settings.MEDIA_ROOT + '/schema/taskschema.json'):
 
    # FileFields give FieldFile which are alreay like fp
    inst = json.load(value)  

    with open(taskschema) as fp:
        schema = json.load(fp)

    try:
        status = validate(inst, schema)
    except jsonschema_exceptions.ValidationError as e:
        prefix = 'JSON file not valid: '
        raise ValidationError(prefix + e.message,
            params={'value': value})
    return status
