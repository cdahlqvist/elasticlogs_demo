#!/usr/bin/python

import json
import sys
import re
from dateutil.parser import parse
import datetime, time

sessions = {}
counter = 0

for line in sys.stdin:
    try:
        obj = json.loads(line)
        user_hash = obj['user_hash']

        obj['epoch'] = time.mktime(parse(obj['timestamp'], fuzzy=True).timetuple())
    
        if user_hash not in sessions:
            sessions[user_hash] = {'start_epoch':0,'start_ts':'','end_epoch':0,'end_ts':'','duration':0,'requests':{'total_count':0,'total_volume':0}}
            sessions[user_hash]['clientip'] = obj['clientip']
            sessions[user_hash]['agent'] = obj['agent']
            sessions[user_hash]['user_hash'] = user_hash

        if sessions[user_hash]['start_epoch'] == 0:
            sessions[user_hash]['start_epoch'] = obj['epoch']
            sessions[user_hash]['start_ts'] = obj['timestamp']
            sessions[user_hash]['end_epoch'] = obj['epoch']
            sessions[user_hash]['end_ts'] = obj['timestamp']
        else:
            if sessions[user_hash]['end_epoch'] < obj['epoch']:
                sessions[user_hash]['end_epoch'] = obj['epoch']
                sessions[user_hash]['end_ts'] = obj['timestamp']
                sessions[user_hash]['duration'] = int(obj['epoch'] - sessions[user_hash]['start_epoch'])
            elif sessions[user_hash]['start_epoch'] > obj['epoch']:
                sessions[user_hash]['start_epoch'] = obj['epoch']
                sessions[user_hash]['start_ts'] = obj['timestamp']
                sessions[user_hash]['duration'] = int(sessions[user_hash]['end_epoch'] - obj['epoch'])
                sessions[user_hash]['duration_days'] = sessions[user_hash]['duration'] / 86400
        
        sessions[user_hash]['requests']['total_count'] += 1
    
        if obj['bytes']:
            sessions[user_hash]['requests']['total_volume'] += obj['bytes']
            sessions[user_hash]['requests'][request_type]['volume'] += obj['bytes']

    except ValueError:
        pass

for uh, data in sessions.iteritems():
    del data['start_epoch']
    del data['end_epoch']

    print json.dumps(data)

