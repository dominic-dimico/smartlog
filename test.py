import smartlog
import pprint
import re

log = smartlog.Smartlog();

timewords = '(now|yesterday|tomorrow|at|noon|midnight|midnight|am|pm|[0-9]|\:|\s)+'

w  = {'when': re.compile(timewords)}
ps = {
    'cmd' : re.compile('new|edit|view|list'),
    'obj' : re.compile('client|session|set'),
}

args = {
  'argspec'  : [ {
    'key'      : 'cmd',
    'pattern'  : re.compile('new|edit|view|list'),
    'optional' : False,
  }, {
    'key'      : 'obj',
    'pattern'  : re.compile('client|session|set'),
    'optional' : False,
  }, {
    'key'      : 'user',
    'pattern'  : re.compile('bowers|dominic|spike'),
    'optional' : True,
  }, 
]};

args = log.gather(args);
log.print(args);

#args = {
#  'y': 3,
#  'z': "0",
#}
#
#try: 
#    args = log.argcheck(args, {
#      'x' : {
#          'log'      : 'x coordinate',
#          'required' :  True,
#          'default'  :  1,
#          'type'     :  int,
#      }, 'y' : {
#          'log'      : 'y coordinate',
#          'required' :  True,
#          'default'  :  0,
#          'actions'  :  ['default', 'backup', 'delete'],
#      }, 'z' : {
#          'log'      : 'z coordinate',
#          'required' :  False,
#          'default'  :  0,
#          'type'     :  int,
#      },
#    });
#
#except smartlog.ArgumentError as e: 
#       pass;
#       #print(e.message);
#
#else: log.logok("Success!"); 
#
#finally: pprint.pprint(args);
