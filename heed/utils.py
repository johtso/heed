from datetime import datetime
import json

import arrow
from flask import Response


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return arrow.get(obj).timestamp

        return json.JSONEncoder.default(self, obj)


def jsonify(*args, **kwargs):
    return Response(
        json.dumps(*args, cls=CustomJSONEncoder, **kwargs),
        mimetype='application/json'
    )
