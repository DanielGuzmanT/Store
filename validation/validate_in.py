from os import path
from jsonschema import validate, ValidationError
from flask import request, jsonify
from functools import wraps
import yaml

with open(path.join(path.dirname(__file__), 'schema.yml')) as f:
    schema = yaml.safe_load(f)


# REAL VALIDATION
def validate_json(schema_one):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # [INIT WRAPPER]
            json = request.get_json(force=True)

            try:
                validate(json, schema_one)
                return func(*args, **kwargs)  # executing principal function

            except ValidationError as error:
                # json send format guide: https://github.com/omniti-labs/jsend
                return jsonify(status="error", message=error.message)

            # [END WRAPPER]
        return wrapper
    return decorator
