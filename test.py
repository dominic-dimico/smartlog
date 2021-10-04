#import smartlog
import selector
import pprint




z = selector.DataSelector([
  {'id':1, 'user':'dominic', 'color': 'red'},
  {'id':2, 'user':'spike',   'color': 'blue'},
  {'id':3, 'user':'clare',   'color': 'magenta'},
  {'id':4, 'user':'lucas',   'color': 'green'},
])

cs = z.edit();
print(cs);

#import time
#for i in range(100):
#    log.progress(i, 100);
#    time.sleep(.1);

#s = selector.Selector(
#   {'food':'chocolate', 'color':'red', 'fruit':'strawberry'}
#);
#y = s.edit();
#s.refresh(y);
#y = s.check();
#print(y);
#x = s.radio();
#print(x);

#s = log.selector(
#   ['chocolate', 'vanilla', 'strawberry']
#);
#y = s.edit();
#s.refresh(y);
#y = s.check();
#x = s.radio();



#import re
#timewords = '(now|yesterday|tomorrow|at|noon|midnight|midnight|am|pm|[0-9]|\:|\s)+'
#
#w  = {'when': re.compile(timewords)}
#ps = {
#    'cmd' : re.compile('new|edit|view|list'),
#    'obj' : re.compile('client|session|set'),
#}
#
#args = {
#  'argspec'  : [ {
#    'key'      : 'cmd',
#    'pattern'  : re.compile('new|edit|view|list'),
#    'optional' : False,
#  }, {
#    'key'      : 'obj',
#    'pattern'  : re.compile('client|session|set'),
#    'optional' : False,
#  }, {
#    'key'      : 'user',
#    'pattern'  : re.compile('bowers|dominic|spike'),
#    'optional' : True,
#  }, 
#]};
#
#args = log.gather(args);
#log.print(args);

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
