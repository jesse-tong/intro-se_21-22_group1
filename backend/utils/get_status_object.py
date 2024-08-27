from global_vars.constants import status_template
from copy import deepcopy
from flask import jsonify
from dataclasses import asdict, is_dataclass
from sqlalchemy import Row

def get_status_object(success:bool, obj, error: str | None):
    status = status_template
    status['result'] = obj
    status['success']  = success
    status['error'] = error
    return status

def convert_sqlalchemy_row(obj):
    #check if the object is an SQLAlchemy row, if not keep as is, if it's convert to dict
    if type(obj) == Row:
        return dict(obj._mapping)

def get_status_object_json(success:bool, obj, error: str | None):
    if type(obj) == list:
        obj = [asdict(item) if is_dataclass(item) else item for item in obj]
    if is_dataclass(obj):
        obj = asdict(obj)
    status_obj = get_status_object(success, obj, error)
    return jsonify(status_obj)

def convert_to_dict(model_objects):
    if type(model_objects) == list:
        obj = [asdict(item) if is_dataclass(item) else item for item in model_objects]
    if is_dataclass(model_objects):
        obj = asdict(model_objects)
    return obj
    

def convert_list_of_dicts_to_list_of_lists(list_of_dicts):
    res = list(map(lambda x: list(x.values()), list_of_dicts))
    res.insert(0, list(list_of_dicts[0].keys()))
    return res