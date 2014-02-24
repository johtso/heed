import collections
from functools import partial
import os

import arrow
from flask import Flask, abort, request
import pymongo

from . import schemas
from .utils import jsonify

app = Flask(__name__)

MONGO_URI = os.getenv('MONGO_URI')
db = pymongo.MongoClient(MONGO_URI).get_default_database()


def remove_key(key, obj):
    if key in obj:
        del obj[key]
    return obj

remove_id = partial(remove_key, '_id')


@app.route('/')
def index():
    return 'hello!'


@app.route('/switches', methods=['GET'])
@app.route('/switches/<switch_id>', methods=['GET'])
def show_switches(switch_id=None):
    if switch_id:
        switches = db.switches.find_one({'name': switch_id})
        if not switches:
            abort(404)
        else:
            switches = remove_id(switches)
    else:
        switches = map(remove_id, db.switches.find())
    return jsonify(switches)


@app.route('/checkin/<switch_id>', methods=['POST', 'PUT'])
def checkin(switch_id):
    data = {'name': switch_id, 'last_checkin': arrow.utcnow().datetime}
    db.switches.update({'name': switch_id}, data, upsert=True)
    return jsonify(data)


@app.route('/status', methods=['POST'])
def status():
    data = request.get_json(silent=True)
    switch_checks = schemas.switches.validate(data)

    if not switch_checks:
        return 'No switches specified', 404

    switches = db.switches.find({
        'name': {'$in': switch_checks.keys()}
    })
    last_checkin_by_name = {switch['name']: switch['last_checkin']
                            for switch in switches}

    now = arrow.utcnow()
    status_counter = collections.Counter()
    for name, interval in switch_checks.iteritems():
        last_checkin = last_checkin_by_name.get(name)
        if last_checkin:
            status_okay = (last_checkin
                           and (now - arrow.get(last_checkin)) < interval)
            status_counter.update([status_okay])
        else:
            status_counter.update([False])

    okay, bad = status_counter[True], status_counter[False]

    if bad:
        return '{} of {} switches triggered'.format(bad, len(switch_checks)), 404
    else:
        return 'All {} switches okay.'.format(len(switch_checks))
