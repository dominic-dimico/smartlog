from   blessings import Terminal
import sys
import inspect
import os
import traceback
import pprint
import pandas;
import traceback;
import numpy;
import getch;
format_ = format
 



pandas.set_option('mode.chained_assignment', None)

class QuietException(Exception):
      pass


class AlertException(Exception):
      def __init__(self, message):
          self.message = message;

class FailException(Exception):

      def caller(self, fr):
          name   = fr.f_code.co_name;
          back   = fr.f_back.f_locals;
          local  = fr.f_locals;
          globl  = fr.f_globals;
          for get in (
                 lambda:globl[name],
                 lambda:getattr(local['self'], name),
                 lambda:getattr(local['cls'], name),
                 lambda:back[name], # nested
                 lambda:back['func'],  # decorators
                 lambda:back['meth'],
                 lambda:back['f'],
          ):
              try:    func = get()
              except: pass
              else:   
                 if func.__code__ == co: 
                    return func;
          return None;

      def __init__(self, log):
          log.fail();
          import inspect
          traceback.print_exc();
          try:
             import sys
             frame  = sys._getframe(1)
             local  = frame.f_locals;
             func   = self.caller(frame);
          except: print("couldn't obtain caller");
          from ptpython.ipython import embed; embed(local=locals())

class WarnException(Exception):
      def __init__(self, message):
          self.message = message;


class Smartlog():


    t       = None;
    outfile = None;
    infile  = None;
    quiet   = False;


    def __init__(self, args={
          'outfile'   : "/dev/stdout",
          'infile'    : "/dev/stdin",
          'pipefile'  : "~/config/smartlog/fifo",
          'name'      : '',
          'printname' : False,
        }):
        for key in args:
            if 'file' not in key:
               setattr(self, key, args[key]);
        self._load();


    def _load(self):
        """ Load args"""
        try:     self.infile  = open(self.args['infile'], 'r');
        except:  self.infile  = sys.stdin;
        try:     self.outfile = open(self.args['outfile'], "a");
        except:  self.outfile = sys.stdout;
        finally: self.t = Terminal(stream=self.outfile, force_styling=True);


    def _pipe(self):
        """ Create a pipe"""
        try:    os.mkfifo(self.args['pipefile']);
        except: traceback.print_exc();
        else:   self.outfile = open('~/.smartlog.fifo', 'w');


    def write(self, msg):
        """Write to outfile"""
        if not self.quiet:
           self.outfile.write(msg);
           self.outfile.flush();


    def previous_line(self):
        """Move cursor to previous line"""
        self.write("\033[F");


    def reprint(self, msg):
        """Re-print a line, e.g. for progress bar"""
        self.write("\r\033[K"+msg);
        self.outfile.flush();


    def incolor(self, color, msg):
      """ Print *msg* in *color*, return *msg*"""
      if   color == "red":    msg = self.t.red(msg)
      elif color == "yellow": msg = self.t.bold_yellow(msg)
      elif color == "green":  msg = self.t.green(msg)
      elif color == "blue":   msg = self.t.blue(msg)
      elif color == "purple": msg = self.t.magenta(msg)
      elif color == "black":  msg = self.t.dim_white(msg)
      elif color == "white":  msg = msg;
      return msg

    def oncolor(self, color, msg):
      """ Print *msg* in *color*, return *msg*"""
      if   color == "red":    msg = self.t.on_red(msg)
      elif color == "yellow": msg = self.t.on_yellow(msg)
      elif color == "green":  msg = self.t.on_green(msg)
      elif color == "blue":   msg = self.t.on_blue(msg)
      elif color == "purple": msg = self.t.on_magenta(msg)
      elif color == "black":  msg = self.t.on_black(msg)
      elif color == "white":  msg = self.t.on_white(msg);
      return msg

    def colored(self, in_color, on_color, msg):
      """ Print *msg* in *color*, return *msg*"""
      return self.incolor(
         in_color,
         self.oncolor(on_color, msg)
      );


    def asterisk(self, color):
        """ Print asterisk in *color*, and name if set"""
        self.write(self.incolor(color, "* ")), 
        if self.printname:
           self.write( self.incolor(color, "[") 
                     + self.incolor('white', self.name)
                     + self.incolor(color, "]")
                     + self.incolor('white', ": ")
           );


    def alert(self, msg):
        """ Print alert *msg*"""
        self.asterisk('red');
        self.write(self.t.bold(" Alert:")),
        self.write(" %s!" % msg),
        self.rok()


    # Print an alert message.
    def yesno(self, msg):
        """ Present prompt asking yes or no"""
        self.asterisk('purple');
        self.write(self.t.bold(" %s? (y/n): " % msg)),
        self.outfile.flush();
        ret = self.infile.readline();
        if ret.rstrip().lstrip() == 'y':
           return True;
        else: return False;


    # Print a WARN message.
    def warn(self, msg):
        """ Display warn *msg* """
        self.asterisk('yellow');
        self.write(self.t.bold(" Warning:")),
        self.write(" %s." % msg),
        self.warnok()


    def optip(self, msg):
        """ Give a tip that says: "You can set it with the %s flag." """
        self.asterisk('blue');
        self.write(" You can set it with the %s flag." % msg),
        self.infook()


    def tip(self, msg):
        """ Display info *msg* """
        self.asterisk('blue');
        self.write(" %s." % msg),
        self.infook()


    def info(self, msg):
        """ Display info *msg* """
        self.asterisk('blue');
        self.write(" %s" % msg),
        self.infook()


    def log(self, msg):
        """ Display log *msg* """
        self.asterisk('green');
        self.write(" %s... " % msg),


    def logn(self, msg):
        """ Display log *msg*, no ellipse """
        self.log(msg);
        self.write("\n");


    def logok(self, msg):
        """ Display log *msg*, with the OK flag """
        self.log(msg);
        self.ok();


    def ok(self, msg=""):
        self.write(msg);
        with self.t.location(x=self.t.width-10):
          self.write("[  "),
          self.write(self.t.green("OK")),
          self.write("  ]"),
        self.write("\n")
        #self.write(str(self.t.width)+"\n")


    def fail(self, msg=""):
        """ Print a FAIL box """
        self.write(msg);
        with self.t.location(x=self.t.width-10):
          self.write("[ "),
          self.write(self.t.red("FAIL")),
          self.write(" ]"),
        self.write("\n")


    def yok(self, msg=""):
        """ Print a yellow OK box """
        self.write(msg);
        with self.t.location(x=self.t.width-10):
          self.write("[  "),
          self.write(self.t.yellow("OK")),
          self.write("  ]"),
        self.write("\n")


    def rok(self, msg=""):
        """ Print a red OK box """
        self.write(msg);
        with self.t.location(x=self.t.width-10):
          self.write("[  "),
          self.write(self.t.red("OK")),
          self.write("  ]"),
        self.write("\n")


    def warnok(self, msg=""):
        """ Print a WARN box """
        self.write(msg);
        with self.t.location(x=self.t.width-10):
          self.write("[ "),
          self.write(self.t.yellow("WARN")),
          self.write(" ]"),
        self.write("\n")


    def infook(self, msg=""):
        """ Print an INFO box """
        self.write(msg);
        with self.t.location(x=self.t.width-10):
          self.write("[ "),
          self.write(self.t.blue("INFO")),
          self.write(" ]"),
        self.write("\n")


    def which(self, program):
        """ Determine if program exists """
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
        """ Show progress bar """
        m = self.t.width - 20;
        p = int((i/n) * 100);
        neqs   = int(float(i/n)*m);
        eqs    = "=" * int(neqs);
        spaces = ' ' * int(m-neqs);
        if (i % 2 == 0): ok=self.t.green(status);
        else:            ok=self.t.green_bold(status);
        self.reprint("[ %s>%s%3s%% ] [ %s ]" % (eqs, spaces, p, ok))

    def checkdir(self, name):
        """ Check if directory *name* exists """
        str = ' '.join(["Checking if directory",name,"exists"])
        self.log(str)
        if os.path.isdir(name):
            self.ok()
            return True
        else:
            self.fail()
            return False


    def checkfile(self, name):
        """ Check if file *name* exists """
        str = ' '.join(["Checking if file",name,"exists"])
        self.log(str)
        if os.path.isfile(name):
            self.ok()
            return True
        else:
            self.fail()
            return False


    def checkenvvar(self, name):
        """ Check if environment variable *name* is set """
        val = os.getkey(name)
        str = ' '.join(["Checking if variable",name,"is set"])
        self.log(str)
        if val:
            self.ok()
        else:
            self.fail()


    #######################################
    #! Compatibility with toolbelt argcheck
    #######################################
    def argcheck(self, user, default):               
        from toolbelt import argcheck;
        return argcheck.argcheck(user, default, log=self);


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
           else:    ret = callback();
        except  WarnException as e: self.warn(e.message);
        except AlertException as e: self.alert(opts['fail']);
        except OverFlowError  as e: pass;
        except      Exception as e: 
                    if args: self.print(args);
                    traceback.print_exc();
                    import code; code.interact(local=locals());  
        except QuietException as e: pass; #self.ok();
        finally:                    return ret;



    def prompt(self, args={
        """ Print a prompt message."""
      'message' : ''
    }):

        from toolbelt import editors;
        from toolbelt import quickdate;
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
           response = editors.vim(text);
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
              response = quickdate.quickdate(response);
           elif args['type'] == 'float':
              response = float(response);
           elif args['type'] == 'int':
              response = int(response);
              
        args['response'] = response;
        if 'datum' in args: args.pop('datum');
        return args;





    def selector(self, ls):
        from smartlog import selector 
        return selector.Selector(self, ls);


    def xselector(self, ds):
        from smartlog import selector 
        return selector.DataSelector(self, ds);


    def gather(self, args):
        from smartlog import gather
        return gather.gather(args, log=self);


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


    ############################################################
    #! TODO: somehow want to merge draw() from selector and this
    ############################################################
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
        colors = ['red', 'blue', 'yellow', 'green', 'purple']
        for row in data:
            if 'color' in row: color = row['color'];
            elif 'tags' in row and row['tags']:
                 cs = [c for c in colors if c in row['tags']];
                 if cs: color = cs[0];
                 else:  color = 'black';
            else: color = 'black';
            for key in keys:
                element   = str(row[key]);
                numspaces = colspace if textwidth < len(element) else colwidth-len(element)
                spaces    =  ' ' * numspaces;
                msg = "%s%s" % (element[:textwidth], spaces);
                self.write(self.oncolor(color,msg));
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

