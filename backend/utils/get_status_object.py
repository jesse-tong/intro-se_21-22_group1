from global_vars.constants import status_template
from copy import deepcopy
from flask import jsonify
from dataclasses import asdict, is_dataclass

def get_status_object(success:bool, obj, error: str | None):
    status = status_template
    status['result'] = obj
    status['success']  = success
    status['error'] = error
    return status

def get_status_object_json(success:bool, obj, error: str | None):
    if type(obj) == list:
        obj = [asdict(item) if is_dataclass(item) else item for item in obj]
    if is_dataclass(obj):
        obj = asdict(obj)
    status_obj = get_status_object(success, obj, error)
    return jsonify(status_obj)