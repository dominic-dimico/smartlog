from   blessings import Terminal
import sys
import os
import traceback
import pprint
import pandas;
import numpy;
import getch;
format_ = format
 


def curpos():

    import re, termios, tty
    buf = ""
    stdin = sys.stdin.fileno()
    tattr = termios.tcgetattr(stdin)

    try:
        tty.setcbreak(stdin, termios.TCSANOW)
        sys.stdout.write("\x1b[6n")
        sys.stdout.flush()

        while True:
            buf += sys.stdin.read(1)
            if buf[-1] == "R":
                break

    finally:
        termios.tcsetattr(stdin, termios.TCSANOW, tattr)

    # reading the actual values, but what if a keystroke appears while reading
    # from stdin? As dirty work around, getpos() returns if this fails: None
    try:
        matches = re.match(r"^\x1b\[(\d*);(\d*)R", buf)
        groups = matches.groups()
    except AttributeError:
        return None

    return (int(groups[0]), int(groups[1]))


pandas.set_option('mode.chained_assignment', None)

class QuietException(Exception):
      pass


class AlertException(Exception):
      def __init__(self, message):
          self.message = message;


class WarnException(Exception):
      def __init__(self, message):
          self.message = message;


class ArgumentError(Exception):

      def introspect(self):
          message = "";
          alert   = "";
          self.errors = 0;
          self.alerts = [];
          for key in self.default.keys():
            if isinstance(self.default[key], dict):
              if 'error' in self.default[key]:
                 message      += '\nError: '     + key + ' '   + self.default[key]['error'];
                 alert        +=                   key + ' '   + self.default[key]['error'];
                 if 'log'     in self.default[key]:
                     message  += '\n  name:    ' + key + ' - ' + self.default[key]['log'];
                 if 'default' in self.default[key]:
                     message  += '\n  default: '               + str(self.default[key]['default']);
                 if 'type'    in self.default[key]:
                     message  += '\n  type:    '               + str(self.default[key]['type'])
                 if 'actions' in self.default[key]:
                     message  += '\n  actions: ' + ",".join(     self.default[key]['actions'])
                 self.errors  = self.errors + 1;
                 self.alerts += [alert];
          self.message = message;
          return message;

      def __init__(self, default):
          self.default = default; 
          self.introspect();



# TODO: enable pipes
class Smartlog():


    t       = None;
    outfile = None;
    infile  = None;
    quiet   = False;


    def __init__(self, args={
          'outfile'  : "/dev/stdout",
          'infile'   : "/dev/stdin",
          'pipefile' : "~/config/smartlog/fifo",
        }):
        self.files = args;
        self.load();



    # Continue printint to stdout
    def load(self):
        try:    self.infile  = sys.stdin;
        except: print("Could not set stdin");
        try:    self.outfile = open(self.files['outfile'], "a");
        except: self.outfile = sys.stdout; #print("File Exception");
        else:   self.t = Terminal(stream=self.outfile, force_styling=True);


    # Create a pipe
    def pipe(self):
        try:    os.mkfifo(self.files['pipefile']);
        except: print("Pipe creation failed!");
        else:   self.outfile = open('~/.smartlog.fifo', 'w');


    # Write to outfile if quiet is not set
    def write(self, msg):
        if not self.quiet:
           self.outfile.write(msg);

    # Print an alert message.
    def previous_line(self):
        self.write("\033[F");


    # Print an alert message.
    def reprint(self, msg):
        self.write("\r\033[K"+msg);
        self.outfile.flush();


    def incolor(self, color, msg):
      if   color == "red":    msg = self.t.red(msg)
      elif color == "yellow": msg = self.t.bold_yellow(msg)
      elif color == "green":  msg = self.t.green(msg)
      elif color == "blue":   msg = self.t.blue(msg)
      elif color == "purple": msg = self.t.magenta(msg)
      elif color == "black":  msg = self.t.dim_white(msg)
      elif color == "white":  msg = msg;
      return msg


    # Print an alert message.
    def alert(self, msg):
        self.write(self.t.red("*")), 
        self.write(self.t.bold(" Alert:")),
        self.write(" %s!" % msg),
        self.rok()


    # Print an alert message.
    def yesno(self, msg):
        self.write(self.t.magenta("*")), 
        self.write(self.t.bold(" %s? (y/n): " % msg)),
        self.outfile.flush();
        ret = self.infile.readline();
        if ret.rstrip().lstrip() == 'y':
           return True;
        else: return False;


    # Print a WARN message.
    def warn(self, msg):
        self.write(self.t.yellow("*")), 
        self.write(self.t.bold(" Warning:")),
        self.write(" %s." % msg),
        self.warnok()


    def optip(self, msg):
        """
        Give a tip that says:
        
        "You can set it with the %s flag."
        """
        self.write(self.t.blue("*")), 
        self.write(" You can set it with the %s flag." % msg),
        self.infook()


    # Print an INFO message.
    def tip(self, msg):
        self.write(self.t.blue("*")), 
        self.write(" %s." % msg),
        self.infook()


    # Print an INFO message.
    def info(self, msg):
        self.write(self.t.blue("*")), 
        self.write(" %s" % msg),
        self.infook()


    # Print an log message, but no OK or FAIL box.
    def log(self, msg):
        self.write(self.t.green("*")), 
        self.write(" %s... " % msg),


    # Print an log message, but no OK or FAIL box.
    def logn(self, msg):
        self.log(msg);
        self.write("\n");


    # Print an log message, with OK.
    def logok(self, msg):
        self.log(msg);
        self.ok();


    # Print an OK box.
    def ok(self, msg=""):
        self.write(msg);
        with self.t.location(x=self.t.width-10):
          self.write("[  "),
          self.write(self.t.green("OK")),
          self.write("  ]"),
        self.write("\n")
        #self.write(str(self.t.width)+"\n")


    # Print a FAIL box.
    def fail(self, msg=""):
        self.write(msg);
        with self.t.location(x=self.t.width-10):
          self.write("[ "),
          self.write(self.t.red("FAIL")),
          self.write(" ]"),
        self.write("\n")


    # Print a yellow OK box.
    def yok(self, msg=""):
        self.write(msg);
        with self.t.location(x=self.t.width-10):
          self.write("[  "),
          self.write(self.t.yellow("OK")),
          self.write("  ]"),
        self.write("\n")


    # Print a red OK box.
    def rok(self, msg=""):
        self.write(msg);
        with self.t.location(x=self.t.width-10):
          self.write("[  "),
          self.write(self.t.red("OK")),
          self.write("  ]"),
        self.write("\n")


    # Print a WARN box.
    def warnok(self, msg=""):
        self.write(msg);
        with self.t.location(x=self.t.width-10):
          self.write("[ "),
          self.write(self.t.yellow("WARN")),
          self.write(" ]"),
        self.write("\n")


    # Print an INFO box.
    def infook(self, msg=""):
        self.write(msg);
        with self.t.location(x=self.t.width-10):
          self.write("[ "),
          self.write(self.t.blue("INFO")),
          self.write(" ]"),
        self.write("\n")


    # Determine if program exists.
    def which(self, program):
        str = ' '.join(["Checking location of",program])
        self.log(str)
        def is_exe(self, fpath):
            return os.path.isfile(fpath) and os.access(fpath, os.X_OK)
        fpath, fname = os.path.split(program)
        if fpath:
            if is_exe(program):
                self.ok()
                return program
        else:
            for path in os.environ["PATH"].split(os.pathsep):
                path = path.strip('"')
                exe_file = os.path.join(path, program)
                if is_exe(exe_file):
                    self.ok()
                    return exe_file
        self.fail()
        return None

    def progress(self, i, n, status=" OK "):
        m = self.t.width - 20;
        p = int((i/n) * 100);
        neqs   = int(float(i/n)*m);
        eqs    = "=" * int(neqs);
        spaces = ' ' * int(m-neqs);
        if (i % 2 == 0): ok=self.t.green(status);
        else:            ok=self.t.green_bold(status);
        self.reprint("[ %s>%s%3s%% ] [ %s ]" % (eqs, spaces, p, ok))

    # Check if directory exists.
    def checkdir(self, name):
        str = ' '.join(["Checking if directory",name,"exists"])
        self.log(str)
        if os.path.isdir(name):
            self.ok()
            return True
        else:
            self.fail()
            return False


    # Check if file exists.
    def checkfile(self, name):
        str = ' '.join(["Checking if file",name,"exists"])
        self.log(str)
        if os.path.isfile(name):
            self.ok()
            return True
        else:
            self.fail()
            return False


    # Check if environment variable is set
    def checkenvvar(self, name):
        val = os.getkey(name)
        str = ' '.join(["Checking if variable",name,"is set"])
        self.log(str)
        if val:
            self.ok()
        else:
            self.fail()


    def funcheck(self, args, preproc, function, postproc):
        args = self.argcheck(args, preproc);
        args = function(args);
        args = self.argcheck(args, postproc);
        return args;


    def copyback(self, args, keys, function):
        return self.funcheck(
             args,
            {'backup' : keys},
             function,
            {'restore' : keys}
        );



    # Check given dictionary against default
    # TODO: this is more than a validator at this point...
    def argcheck(self, user, default):


        def add_error(default, key, error):
            if 'error' not in default[key]: 
                              default[key]['error']  =        error;
            else:             default[key]['error'] += '; ' + error;
            return            default;


        from copy import copy
        def backup(user, key, ext='.1'):
            if ext != '.1':
               user[key+ext] = copy(user[key]);
               return user;
            index = 1;
            backup_key = key + ext;
            while backup_key in user:
                  backup_key = key + "." + str(index);
                  index      = index + 1;
            user[backup_key] = copy(user[key]);
            return user;


        def restore(user, key, ext='.1'):
            if ext != '.1':
                user[key] = user[key+ext];
                user.pop(backup_key)
                return user;
            index = 1;
            next_backup_key = key + ext;
            last_backup_key = key;
            while next_backup_key in user:
                  index           = index + 1;
                  last_backup_key = next_backup_key;
                  next_backup_key = key + "." + str(index);
            if last_backup_key in user and last_backup_key != key:
                user[key] = copy(user[last_backup_key]);
                user.pop(last_backup_key)
            else: return None;
            return user;
    

        def default_actions(user, default, key):

            if 'actions' not in default[key]:
               default[key]['actions'] = [];

            actions = [
               'log',
               'restore', 'backup',  
               'default', 'overwrite', 
               'clear',   'delete', 
               'gather',  
               'type',    
               'require', 
            ];

            for action in actions:
                if (((action in default and key in default[action])
                  or (action in default[key])) 
                 and (action not in default[key]['actions'])):
                         default[key]['actions'] += [action];

            if 'all' in default:
               default[key]['actions'] = default['all'] + default[key]['actions'];

            return (user, default);


        def do_gather(self, user, default, key):
            t = str;
            if 'gather' not in default[key]:
                  default[key]['gather'] ='maybe';
            if    default[key]['gather']=="never": return (user, default);
            elif (default[key]['gather']=="always" or
                 (default[key]['gather']=="maybe"  and 
                   key not in user 
                 )):
                 if 'type' in default[key]:
                     t = default[key]['type'];
                 args = self.gather({
                           'method': 'linear',
                           'keys'  : [key],
                           'data'  : {},
                           'types' : {key:str(t)},
                 });
                 try:    user[key] = (t)(args['data'][key]);
                 except: user[key] = '';
            return (user, default)


        def do_actions(self, user, default, key):
            (user, default) = default_actions(user, default, key);
            for action in default[key]['actions']:
                if action == "require":
                   self.log("Requiring %s" % (key));
                   if key not in user:
                        self.fail("not found");
                        default = add_error(default, key, "required");
                        break;
                   else: self.ok();
                elif action == "gather":
                     (user, default) = do_gather(self, user, default, key);
                elif action == "overwrite":
                         self.log("Overwriting %s" % (key));
                         user[key] = default[key]['overwrite'];
                         self.ok();
                elif action == "default":
                     if key not in user: 
                         self.log("Defaulting %s" % (key));
                         if 'default' in default[key]:
                            user[key] = default[key]['default'];
                            self.ok(str(default[key]['default']));
                         else: self.fail("no default field supplied");
                elif action == "restore":
                        self.log("Restoring %s" % (key));
                        if 'restore' in default[key]:
                              restored = restore(user, key, default[key]['restore']);
                        else: restored = restore(user, key);
                        if not restored: self.fail("no backup");
                        else: 
                          user = restored;
                          self.ok(str(user[key]));
                elif action == "clear":
                        self.log("Clearing %s" % (key));
                        if isinstance(user[key], str):
                           user[key] = '';
                        elif isinstance(user[key], dict):
                           user[key] = {}; 
                        elif isinstance(user[key], list):
                           user[key] = []; 
                        elif isinstance(user[key], tuple):
                           user[key] = tuple(); 
                        elif isinstance(user[key], int):
                           user[key] = 0; 
                        elif isinstance(user[key], float):
                           user[key] = 0.0; 
                        else: 
                           user[key] = None;
                        self.ok();
                elif action == "delete":
                     self.log("Deleting %s" % (key));
                     if key in user: 
                        user.pop(key);
                        self.ok();
                     else: self.fail("no key to delete")
                elif action == "log":
                     if 'log' in default[key]:
                        self.info(key+": "+default[key]['log']);
                elif action == "backup":
                     self.log("Backing up %s" % (key));
                     if key in user: 
                        if 'backup' in default[key]:
                              user = backup(user, key, default[key]['backup']);
                        else: user = backup(user, key);
                        self.ok();
                     else: self.fail();
                elif action == "type":
                     self.log("Type-checking %s" % (key));
                     if 'type' in default[key]: 
                         if key in user:
                            if not isinstance(user[key], default[key]['type']):
                               try:   
                                   user[key] = (default[key]['type'])(user[key]);
                                   self.ok("converted");
                               except Exception: 
                                   default = add_error(default, key, "type");
                                   self.fail("exception occured");
                                   break;
                            else: self.ok("ok");
                         else: self.fail('key not found');
                     else: self.fail('type not set');
            return (user, default);


        def extract_keys(self, user, default):
            keys = list(default.keys());
            morekeys = [];
            for key in keys:
                if isinstance(default[key], list):
                   for akey in default[key]:
                       if akey not in morekeys:
                          morekeys += [akey];
            for key in morekeys:
                if key not in default:
                   default[key] = {};
            return (user, default);


        def process(self, user, default):
            keys = list(default.keys());
            for key in keys:
                if isinstance(default[key], dict):
                   (user, default) = do_actions(self, user, default, key);
            return (user, default);


        def check_errors(self, user, default):
            ae = ArgumentError(default);
            for i in range(ae.errors):
                self.alert(ae.alerts[i]);
            return ae;


        if not isinstance(user, dict):
           raise ArgumentError({'args':{'error':'type'}});

        if not isinstance(default, dict):
           raise ArgumentError({'default':{'error':'type'}});


        quiet = self.quiet;
        self.quiet = True;
        if 'quiet' in default and not default['quiet']:
           self.quiet = False;

        (user, default) = extract_keys(self, user, default);
        (user, default) =      process(self, user, default);
        ae              = check_errors(self, user, default);

        self.quiet = False;
        if ae.errors>0: 
           raise ae;

        return user;

               


    def exlog(self, callback, args, opts={}):
        opts = self.argcheck(opts, {
           'log'  : {'default': callback.__name__},
           'ok'   : {'default': 'ok'   },
           'fail' : {'default': 'fail' },
        });
        ret = False;
        try:
           self.logn(opts['log']);
           if args: ret = callback(args);
           else:    ret = callback(args);
        except  WarnException as e: self.warn(e.message);
        except AlertException as e: self.alert(opts['fail']);
        except OverFlowError  as e: pass;
        except      Exception as e: 
                    if args: self.print(args);
                    traceback.print_exc();
                    import code; code.interact(local=locals());  
        except QuietException as e: pass; #self.ok();
        finally:                    return ret;



    # Print a prompt message.
    def prompt(self, args={
      'message' : ''
    }):

        import toolbelt;
        if 'message' in args: 
              message = args['message'];
        else: message = args;
        p = self.t.magenta("*") + self.t.bold(" %s: " % message);

        response = '';

        # Fix response not sticking
        if 'type' in args and args['type'] == 'text':
           text = '';
           if 'datum' in args:
              if args['datum']: text = args['datum'];
           response = toolbelt.editors.vim(text);
        elif 'auto' in args:
           args['auto'].prompt = p;
           if 'datum' in args and args['datum']:
              args['auto'].input = args['datum'];
           response = args['auto'].run();
        else: 
           self.quiet=False;
           self.write(p);
           self.outfile.flush();
           response = self.infile.readline();

        response = response.rstrip().lstrip();
        if response == '':
           args['response'] = '';
           if 'datum' in args: args.pop('datum');
           return args;

        if 'type' in args:
           if args['type'] == 'datetime':
              response = toolbelt.quickdate.quickdate(response);
           elif args['type'] == 'float':
              response = float(response);
           elif args['type'] == 'int':
              response = int(response);
              
        args['response'] = response;
        if 'datum' in args: args.pop('datum');
        return args;




    class Selector():


        def __init__(self, log, ls):
              self.log = log;
              self.t = log.t;
              self.refresh(ls);
              

        def refresh(self, ls):
            import toolbelt;
            self.ls = ls;
            self.n = len(ls);
            self.c = toolbelt.coordinates.Cursor();
            self.c.ymax = self.n-1;
            self.c.ywrap = True;
            if isinstance(ls, dict):
               self.ks = list(ls.keys()); ks = self.ks;
               self.km = max([len(x) for x in ks]) if ks else 0;
               self.m = max([len(str(ls[x])) for x in ls]) if ls else 0;
            self.m = max([len(str(x)) for x in ls]) if ls else 0;
            self.z = None;


        def kspace(self, s):
            return s + ' ' * (self.km - len(s));
        def space(self, s):
            return s + ' ' * (self.m - len(str(s)));


        def draw(self, sels=[]):
            t = self.t; ls = self.ls;
            n = self.n; c = self.c;
            for i in range(len(ls)):
                if isinstance(ls, dict): 
                      s = self.kspace(self.ks[i]) + ": " + self.space(str(ls[self.ks[i]]));
                else: s = self.space(ls[i]);
                with t.location(0, t.height-n+i-1):
                     if i == c.y:    self.log.write("   > "+t.black_on_yellow(s));
                     elif i in sels: self.log.write("   > "+t.yellow(s));
                     else:           self.log.write("   > "+t.white(s));
                     self.log.outfile.flush();


        def radio(self):
            ls = self.ls; c = self.c; t = self.t; 
            n = self.n; z = None;
            self.log.write("Select one:\n"+"\n"*n);
            while not z:
                self.draw();
                (_, z) = c.kb.wait();
            (x, y) = z;
            return y;


        def check(self):
            c = self.c; t = self.t; n = self.n;
            z = self.z; k = '';  sels = [];
            self.log.write("Select any (q to quit): \n"+"\n"*n);
            while True:
                self.draw(sels);
                (k, z) = c.kb.wait();
                if k=='q': break;
                if k=='\n':
                   sels += [c.y];
            return sels;


        def editx(self):
            ls = self.ls; c = self.c; t = self.t; 
            n = self.n; 
            with t.location(0, t.height-n+c.y-1):
                 self.log.write("   > ");
                 if isinstance(ls, dict):
                    self.log.write(self.space(self.ks[c.y])+": ");
                 self.log.outfile.flush();
            with t.location(0, t.height-n+c.y-1):
                 inp = input();
            with t.location(0, t.height-n+c.y-1):
                 self.log.write("   > ");
                 self.log.write(self.space(self.ks[c.y])+": ");
                 self.log.write(' '*len(str(ls[self.ks[c.y]])));
            return inp;


        def edit(self):
            c = self.c; t = self.t; n = self.n;
            ls = self.ls; z = self.z; k = ''; 
            eds = [];
            self.log.write("q to quit: \n"+"\n"*n);
            while True:
                self.draw(eds);
                (k, z) = c.kb.wait();
                if   k=='q': break;
                elif k=='\n': 
                     inp = self.editx();
                     if isinstance(ls, dict):
                           ls[self.ks[c.y]] = inp;
                     else: ls[c.y] = inp;
                     eds += [c.y];
            return self.ls;
            

    class DataSelector():

          def __init__(self, log, ds):
              import toolbelt;
              self.log = log;
              self.t   = log.t;
              self.n   = len(ds);
              self.c   = toolbelt.coordinates.Cursor();
              self.z   = None;
              self.ds  = ds;
              if ds: 
                    d = ds[0]
                    self.ks  = list(d.keys());
              else: self.ks = [];
              self.c.xmax = self.n-1;
              self.c.ymax = len(d.keys())-1;
              self.ms  = [];
              self.eds = [];


          def space(self, s):
              if len(s)>10: s = s[:10];
              return s + ' ' * (12 - len(s) if len(s)<10 else 2);


          def drawkeys(self):
              ds = self.ds; c = self.c; n = self.n;
              t  = self.t; 
              j = 0;
              d = ds[0];
              for k in d:
                  with t.location((j*12), t.height-n-3):
                       self.log.write(t.yellow(self.space(k)));
                  j += 1;

          def color(self, i):
              if 'color' in self.ks:
                 return self.ds[i]['color']
              else: return "white";

          def draw(self):
              ds = self.ds; c = self.c; n = self.n;
              t  = self.t; 
              self.drawkeys();
              (x, y) = curpos();
              for i in range(n):
                  j = 0;
                  colorful = self.color(i);
                  for k in self.ds[i]:
                      with t.location((j*12), t.height-n-2+i):
                          if (i + j) % 2 == 0:     s  = "{t.%s" % colorful
                          else:                    s  = "{t.%s" % colorful
                          if (c.x, c.y) == (i, j): s += "_reverse";
                          else:
                              if (i, j) in self.eds:
                                 if colorful != black:
                                       s += "_on_yellow";
                                 else: s += "_italic";
                          s += "}";
                          s += self.space(str(self.ds[i][k]))+"{t.normal}";
                          self.log.write(s.format(t=t));
                          j += 1;
              self.log.outfile.flush();


          def check(self):
              c = self.c; t = self.t; n = self.n;
              z = self.z; k = ''; eds = [];
              self.log.write("Select any: \n"+"\n"*n);
              while True:
                    self.draw();
                    (k, z) = c.kb.wait();
                    if k=='q': break;
                    if k=='\n':
                       self.eds += [(c.x, c.y)];
              return self.eds;


          def editx(self):
              c  = self.c; t = self.t;
              with self.t.location(0, self.t.height-2):
                   self.log.write(" > ");
                   self.log.outfile.flush();
                   v = input();
              k = self.ks[c.y];
              with self.t.location(0, self.t.height-2):
                   self.log.write(" > "+' '*len(v));
              self.ds[c.x][k] = v;
              self.eds += (c.x, c.y);
              


          def edit(self):
              c  = self.c; t = self.t; n = self.n;
              z  = self.z; k = ''; eds = [];
              ds = self.ds;
              self.log.write("Select any: \n"+"\n"*n+"\n\n");
              while True:
                    self.draw();
                    (k, z) = c.kb.wait();
                    if k=='q': break;
                    if k=='\n':
                       self.editx();
              return self.ds;



    def selector(self, ls):
        return self.Selector(self, ls);

    def xselector(self, ds):
        return self.DataSelector(self, ds);


    # Gather data into a dict, line by line,
    # with prompts
    def gather(self, args):

        args = self.argcheck(args, {
           'argspec' : {'default': {}, 'type':pandas.DataFrame},
           'keys'    : {'default': [], 'type':list},
           'xs'      : {'default': [], 'type':list},
           'data'    : {'default': {}, 'type':dict},
           'types'   : {'default': {}, 'type':dict},
        });

        args['maxlength'] = max([len(key) for key in args['keys']]) if args['keys'] else 0;
        args["keyindex"]  = 0;

        if 'data' not in args['argspec']:
           args['argspec']['data'] = numpy.nan;
        if 'span' not in args['argspec']:
           args['argspec']['span'] = numpy.nan;
           args['argspec'] = args['argspec'].astype({'span':object})


        # Format the info and prompt messages
        def format(args):
            args['spaces']  = ' ' * (args['maxlength'] - len(args['keys'][args['keyindex']]));
            args['message'] = "%s%s  " % (args['keys'][args['keyindex']], args['spaces'])
            if args['keys'][args['keyindex']] in args['data'].keys():
               args['datum'] = args['data'][args['keys'][args['keyindex']]];
               args['info'] = "%s%s  : %s" % (
                       args['keys'][args['keyindex']], 
                       args['spaces'],
                       args['data'][args['keys'][args['keyindex']]]
                   )
            return args;


        # Gather everything from xs
        def gatherxs(args):
            i = args["keyindex"];
            j = 0;
            while j < len(args['xs']):
                if j+i >= len(args['keys']):
                   #self.warn("More inputs than keys");
                   args["xs"] = args["xs"][j:];
                   args["keyindex"] = j+i;
                   return args;
                args['data'][args['keys'][j+i]] = args['xs'][j+i];
                j += 1;
            args["xs"] = args["xs"][j:];
            args["keyindex"] = j+i;
            return args;


        # Gather words
        def gatherwords(args):
            args = format(args);
            if 'types' in args:
               args['type'] = args['types'][args['keys'][args['keyindex']]]
            args = self.prompt(args);
            args["xs"] = args["response"].split(" ");
            args = gatherxs(args);
            return args;


        # Gather a line
        def gatherline(args):
            args = format(args);
            if 'types' in args:
               if args['keys'][args['keyindex']] in args['types']:
                  args['type'] = args['types'][args['keys'][args['keyindex']]]
            if args["keys"][args["keyindex"]] in args['data'].keys():
               self.info(args['info']);
               if 'overwrite' in args and not args['overwrite']:
                  args["keyindex"] += 1;
                  return args;
            args = self.prompt(args);
            if args["response"] != '':
               args["data"][args["keys"][args["keyindex"]]] = args["response"];
            return args;
            

        def trimstring(string, spans):
            spans = list(set(spans));
            spans.sort(key=lambda x: x[1], reverse=True);
            for x in range(len(spans)):
                (b, e) = spans[x]
                string = string.replace(string[b:e], "").strip();
            return string;



        def gatherpatkey(args, x):
            import toolbelt;
            df    = args['argspec'];
            spec  = df.loc[x,];
            key   = spec['key']
            p     = spec['pattern'];
            q     = spec['exclude'];

            string = str(args['response']);
            if not pandas.isnull(spec['exclude']):
                ns = q.finditer(string);
                spans = []
                for n in ns:
                    spans += [n.span(0)];
                string = trimstring(string, spans);
            m = p.search(string);
            if not m: return args;
            args['data'][key]  = m.group(0);
            df.loc[x,'data']   = m.group(0);
            df.at[x,'span']    = m.span(0);
            if key not in args['keys']: 
                  args['keys'] += [key];
            if (('types' in args and key in args['types'] and args['types'][key] == "datetime")
                  or ('type' in spec and spec['type']=="datetime")):
                  args['data'][key] = toolbelt.quickdate.quickdate(args['data'][key]);
                  df.loc[x,'data']  = toolbelt.quickdate.quickdate(df.loc[x,'data']);
            return args;


        def updatekeysleft(args):
            args['keysleft'] = [];
            for key in args['patkeys']:
                if key not in args['excluded']:
                   args['keysleft'].append(key);
            return args;


        def gatherpats(args):
            """ Gather data based on regex argspec
                First gather from xs, then from stdin
            """
            df = args['argspec'];
            args = self.argcheck(args, {
                'excluded' : {'overwrite': []},
                'response' : {'overwrite': " ".join(args['xs'])},
                'patkeys'  : {'overwrite': df['key'].to_list()},
                'keysleft' : {'overwrite': df['key'].to_list()},
                'optkeys'  : {'overwrite': df[df['optional']==False]['key'].to_list()},
            });
            for x in range(len(df)):
                args = gatherpatkey(args, x);
            reqs = df[(df['optional']==False) & (df['data'].isna())];
            while len(reqs)>0:
                  key  = reqs.iloc[0]['key'];
                  args['keyindex'] = args['keys'].index(key);
                  args = format(args);
                  args = self.prompt(args);
                  for x in range(len(df)):
                      args = gatherpatkey(args, x);
                  reqs = df[(df['optional']==False) & (df['data'].isna())];
            spans = [];
            for x in range(len(df)):
                if not pandas.isnull(df.loc[x,'span']):
                   spans += [df.loc[x,'span']];
            args['response'] = trimstring(args['response'], spans)
            if args['response'] != '':
                  args['xs'] = args['response'].split(" ");
            else: args['xs'] = [];
            return args;



        # If we have keys that aren't defined in the argspec,
        # we can gather them here
        def gatherleftovers(args):
            args['keysleft'] = list(
                set(args['keys']) - set(args['excluded'])
            );
            if args['keysleft']:
               args['keyindex'] = args['keys'].index(args['keysleft'][0]);
               args['data'][args['keys'][args['keyindex']]] = args['response'];
            for key in args['keysleft']:
                args['keyindex'] = args['keys'].index(key);
                args = gatherline(args);
            return args;


        def combinekeys(args):
            df = args['argspec'];
            args['keys'] += [k for k     in list(df['key'].unique())
                                if k not in   args['keys']];
            return args;


        # If we have argspec, first gather from argspec 
        if ('argspec' in args and 'method' not in args or 
            'method' in args and args['method'] != "linear"):
           #args['argspec']['data'] = numpy.nan;
           args = combinekeys(args);
           args = gatherpats(args);
           return self.argcheck(args, {
                'excluded' : {'delete': True},
                'keysleft' : {'delete': True},
                'patkeys'  : {'delete': True},
                'optkeys'  : {'delete': True},
                'maxlength': {'delete': True},
                'message'  : {'delete': True},
                'spaces'   : {'delete': True},
           });


        # Gather xs
        args = gatherxs(args);

        # Gather words
        if 'words' in args and args['words']:
           while args["keyindex"] < len(args["keys"]):
                 args = gatherwords(args);

        # Gather lines
        else: 
          while args["keyindex"] < len(args["keys"]):
                args = gatherline(args);
                args["keyindex"] += 1;

        return args;


    def logdata(self, args):
        """ Pretty-print a dictionary
        """
        if 'data' not in args:
           return;
        d = args['data'];
        if len(d) == 0: return;
        l = max([len(k) for k in d]);
        i = 0
        for k in d:
            dk = d[k];
            if 'types' in args and k in args['types'] and args['types'][k] == "text":
                dk = self.firstline({ 'message' : d[k], });
            i = i + 1;
            sp = ' ' * (l - len(k));
            self.info("  %s%s : %s" % (k, sp, dk));
        return args;


    def firstline(self, args):
        """ Extract the first line from message.
              *message* - str message to extract line from
        """
        if 'message' in args:
           if isinstance(args['message'], str):
              splits = args['message'].split('\n');
              if len(splits) > 0:
                 args['message'] = splits[0];
        return args['message'];


    # args = {
    #  'linelen' : 'length of line'
    #  'message'     : 'message to print
    #}
    def wrap(self, args):
        if 'message' in args:
           if args['message']:
              msglen  = len(args['message'])
              linelen = args['linelen']
              if msglen < linelen: return args['message'];
              args['message'] = args['message'].replace('\n', ' ');
              nolines = int(msglen/args['linelen']);
              msg = '\n';
              #args['message'];
              for i in range(0, nolines):
                  msg += args['message'][i*linelen:(i+1)*linelen] + '\n';
              return msg + args['message'][(i+1)*linelen:];
        return '';
        
        

    def print(self, args):
        pprint.pprint(args);


    # Print a table
    # tabspec
    # {
    #  'width' : 10,
    #  'color' : blue,
    # }
    def tabulate(self, keys, data, opts={
        'colwidth' : 12,
        'colspace' : 1,
    }):
        colwidth=opts['colwidth'];
        colspace=opts['colspace'];
        textwidth = colwidth - colspace;
        for key in keys:
            numspaces = colspace if textwidth < len(key) else colwidth-len(key)
            spaces    = ' ' * numspaces;
            self.write(self.t.yellow("%s%s" % (key[:textwidth], spaces)));
        self.write("\n");
        for row in data:
            if 'color' in row: color = row['color'];
            else:              color = 'white';
            for key in keys:
                element   = str(row[key]);
                numspaces = colspace if textwidth < len(element) else colwidth-len(element)
                spaces    =  ' ' * numspaces;
                msg = "%s%s" % (element[:textwidth], spaces);
                self.write(self.incolor(color,msg));
            self.write("\n");



    def print_element(self, spec):
        data = str(spec['data']);
        spaces = ' ' * (spec['width'] if spec['width'] < len(data) else spec['width']-len(data));
        self.write(incolor(spec['color'], "%s%s" % (data[:spec['width']], spaces)));


    def xtabulate(self, df):
        for y in df.columns:
            d = df.at['keys', y];
            print_element(d);
        self.write("\n");
        for y in df.columns:
           for x in range(len(df)):
               d = df.at[x, y];
               print_element(d);
           self.write("\n");

