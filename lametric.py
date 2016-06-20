# PythonAPI LaMetric REST data access
# coding=utf-8

import json
import urllib2
import ssl

# Common definitions

#_BASE_URL       = "https://developer.lametric.com/"
_BASE_URL       = "https://10.0.1.100:4343/"
_PUSH_URL       = _BASE_URL + "api/v1/dev/widget/update/com.lametric."

class Setup(object):

    def __init__(self):
        self.data = {}
        self.data['frames'] = []
        self.index = 0

    def addTextFrame(self, icon, text):
        frame = {}
        frame['index'] = self.index
        frame['icon']  = icon
        frame['text']  = text
        self.data['frames'].append(frame)
        self.index += 1

    def addGoalFrame(self, icon, start, current, end, unit):
        frame = {}
        frame['index'] = self.index
        frame['icon']  = icon
        frame['goalData'] = {}
        frame['goalData']['start'] = start
        frame['goalData']['current'] = current 
        frame['goalData']['end'] = end
        frame['goalData']['unit'] = unit
        self.data['frames'].append(frame)
        self.index += 1

    def addSparklineFrame(self, data):
        frame = {}
        frame['index'] = self.index
        frame['chartData'] = data
        self.data['frames'].append(frame)
        self.index += 1
    
    def push(self, app_id, access_token):
        #ctx = ssl.create_default_context()
        #ctx.check_hostname = False
        #ctx.verify_mode = ssl.CERT_NONE
        #opener = urllib2.build_opener(urllib2.HTTPSHandler(context=ctx));
        opener = urllib2.build_opener();
        headers = { 'Accept': 'application/json', 'Cache-Control': 'no-cache', 'X-Access-Token': access_token };
        request = urllib2.Request(_PUSH_URL + app_id, json.dumps(self.data,ensure_ascii=False), headers);

        print json.dumps(self.data,ensure_ascii=False)

        try:
            response = opener.open(request);
        except urllib2.HTTPError as e:
            print('The server couldn\'t fulfill the request.')
            print('Error code: ', e.code)
            print e.read()
        except urllib2.URLError as e:
            print('Failed to reach a server.')
            print('Reason: ', e.reason)
            print e.read()
        #else:
            # everything is fine

