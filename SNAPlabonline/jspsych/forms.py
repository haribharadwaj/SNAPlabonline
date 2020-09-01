from django.forms import ModelForm
from django.core.exceptions import ValidationError
from .models import Task
import json
from jsonschema import (
    validate, 
    exceptions as jsonschema_exceptions
)

const_stim_schema = """
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
                    "cond": {"type": "integer", "minimum": 1},
                    "showanswerwithfeedback": {"type": "boolean"},
                    "trialfeedback": {"type": "boolean"},
                    "annot": {"type": "object"}
                    },
                "if": {
                "properties": {"plugin": {"const": "hari-audio-button-response"}}
                },
                "then": {
                "required": ["plugin", "prompt", "stimulus", "answer", "cond"]
                },
                "else": {
                "required": ["plugin", "prompt"]
                },
                "additionalProperties": false
                },
            "minItems": 1
            },
        "volume": 
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
                "required": ["plugin", "prompt", "stimulus"]
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
        "randomize", "serveraudio", "trials", "isi", "volume"],
    "additionalProperties": false
}
"""


def conststim_json_validate(value,
    taskschema=const_stim_schema):
 
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



class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'displayname', 'descr', 'task_type', 'trialinfo']

    def clean(self):
        cleaned_data = super().clean()
        task_type = cleaned_data.get('task_type')
        trialinfo = cleaned_data.get('trialinfo')
        if task_type == self.instance.CONST_STIM:
            conststim_json_validate(trialinfo)
        else:
            valerr = ValidationError('Only "Constant Stimulus n-AFC" supported for now',
                code='invalid')
            self.add_error('task_type', valerr)
            self.add_error('trialinfo', valerr)


class TaskUpdateForm(ModelForm):
    class Meta:
        model = Task
        # Different form needed because 'name' is PK and can't be edited.
        fields = ['displayname', 'descr', 'task_type', 'trialinfo']

    def clean(self):
        cleaned_data = super().clean()
        task_type = cleaned_data.get('task_type')
        trialinfo = cleaned_data.get('trialinfo')
        if task_type == self.instance.CONST_STIM:
            conststim_json_validate(trialinfo)
        else:
            valerr = ValidationError('Only "Constant Stimulus n-AFC" supported for now',
                code='invalid')
            self.add_error('task_type', valerr)
            self.add_error('trialinfo', valerr)
