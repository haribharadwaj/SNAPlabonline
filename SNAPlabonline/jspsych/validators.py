from django.conf import settings
from django.core.exceptions import ValidationError
import json
from jsonschema import (
    validate, 
    exceptions as jsonschema_exceptions
)



taskschema = """
{
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "jsPsych Task schema",
    "description": "This schema attempts to validate the jsPsych task JSONs uploaded by experimenters",
    "type": "object",
    "properties":
        {
        "instructions": {"type": "array", "items": {"type": "string"}},
        "feedback": {"type": "boolean"},
        "holdfeedback": {"type": "boolean"},
        "feedbackdur": {"type": "number"},
        "serveraudio": {"type": "boolean"},
        "randomize": {"type": "boolean"},
        "estimatedduration": {"type": "number"},
        "isi": {"type": "number"},
        "trials": 
            {
            "type": "array", 
            "items":
                {
                "type": "object",
                "properties":
                    {
                    "plugin": {"type": "string",
                        "enum": ["hari-audio-button-response", "html-button-response"]},
                    "prompt": {"type": "string"},
                    "choices":
                        {
                        "type": "array",
                        "items":
                            {
                            "type": "string",
                            "minItems": 1,
                            "uniqueItems": true
                            }
                        },
                    "stimulus": {"type": "string", "pattern": "(wav)$"},
                    "answer": {"type": "integer", "minimum": 1},
                    "annot": {"type": "object"}
                    },
                "if": {
                "properties": {"plugin": {"const": "hari-audio-button-response"}}
                },
                "then": {
                "required": ["plugin", "prompt", "stimulus", "answer"]
                },
                "else": {
                "required": ["plugin", "prompt"]
                },
                "additionalProperties": false
                },
            "minItems": 1
            }
        },
    "required": ["instructions", "feedback", "holdfeedback",
        "randomize", "serveraudio", "trials", "isi"],
    "additionalProperties": false
}
"""


def taskjson_validate(value,
    taskschema=taskschema):
 
    # taskinfo is a TextField inttot which JSON string is pasted
    try:
        inst = json.loads(value)
    except ValueError as ev:
        raise ValidationError('Not a valid JSON string',
            params={'value': value})

    schema = json.loads(taskschema)

    try:
        status = validate(inst, schema)
    except jsonschema_exceptions.ValidationError as e:
        prefix = 'Info not valid: '
        raise ValidationError(prefix + e.message,
            params={'value': value})
    return status
