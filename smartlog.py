from   blessings import Terminal
import sys
import os
import traceback
import pprint


class QuietException(Exception):
      pass

class AlertException(Exception):
      def __init__(self, message):
          self.message = message;


# TODO: enable pipes
class Smartlog():

    t       = None;
    outfile = None;
    infile  = None;


    def __init__(self, args={
        'outfile' : "/dev/stdout",
        'infile'  : "/dev/stdin",
    }):
        try: self.outfile = open(args['outfile'], "a");
        except: print("File Exception");
        self.t = Terminal(stream=self.outfile, force_styling=True);
        try: self.infile = open(args['infile'], "r");
        except: print("File Exception");


    # Be silent
    def quiet(self):
        self.outfile = open('/dev/null', "a");


    # Continue printint to stdout
    def resume(self):
        self.outfile = open('/dev/stdout', "a");
        self.t = Terminal(stream=self.outfile, force_styling=True);


    # Print an alert message.
    def reprint(self, msg):
        self.outfile.write("\r\033[K"+msg);


    # Print an alert message.
    def alert(self, msg):
        self.outfile.write(self.t.red("*")), 
        self.outfile.write(self.t.bold(" Alert:")),
        self.outfile.write(" %s!" % msg),
        self.rok()


    # Print an alert message.
    def yesno(self, msg):
        self.outfile.write(self.t.magenta("*")), 
        self.outfile.write(self.t.bold(" %s? (y/n): " % msg)),
        self.outfile.flush();
        ret = sys.stdin.readline();
        if ret.rstrip().lstrip() == 'y':
           return True;
        else: return False;


    # Print a WARN message.
    def warn(self, msg):
        self.outfile.write(self.t.yellow("*")), 
        self.outfile.write(self.t.bold(" Warning:")),
        self.outfile.write(" %s." % msg),
        self.warnok()


    def optip(self, msg):
        """
        Give a tip that says:
        
        "You can set it with the %s flag."
        """
        self.outfile.write(self.t.blue("*")), 
        self.outfile.write(" You can set it with the %s flag." % msg),
        self.infook()


    # Print an INFO message.
    def tip(self, msg):
        self.outfile.write(self.t.blue("*")), 
        self.outfile.write(" %s." % msg),
        self.infook()


    # Print an INFO message.
    def info(self, msg):
        self.outfile.write(self.t.blue("*")), 
        self.outfile.write(" %s" % msg),
        self.infook()


    # Print an log message, but no OK or FAIL box.
    def log(self, msg):
        self.outfile.write(self.t.green("*")), 
        self.outfile.write(" %s..." % msg),


    # Print an log message, but no OK or FAIL box.
    def logn(self, msg):
        self.log(msg);
        self.outfile.write("\n");


    # Print an log message, with OK.
    def logok(self, msg):
        self.log(msg);
        self.ok();


    # Print an log message, with no OK and newline.
    def lognok(self, msg):
        self.log(msg);
        self.outfile.write("\n");


    # Print an OK box.
    def ok(self):
        with self.t.location(x=self.t.width-10):
          self.outfile.write("[  "),
          self.outfile.write(self.t.green("OK")),
          self.outfile.write("  ]"),
        self.outfile.write("\n")
        #self.outfile.write(str(self.t.width)+"\n")


    # Print a FAIL box.
    def fail(self):
        with self.t.location(x=self.t.width-10):
          self.outfile.write("[ "),
          self.outfile.write(self.t.red("FAIL")),
          self.outfile.write(" ]"),
        self.outfile.write("\n")


    # Print a yellow OK box.
    def yok(self):
        with self.t.location(x=self.t.width-10):
          self.outfile.write("[  "),
          self.outfile.write(self.t.yellow("OK")),
          self.outfile.write("  ]"),
        self.outfile.write("\n")


    # Print a red OK box.
    def rok(self):
        with self.t.location(x=self.t.width-10):
          self.outfile.write("[  "),
          self.outfile.write(self.t.red("OK")),
          self.outfile.write("  ]"),
        self.outfile.write("\n")


    # Print a WARN box.
    def warnok(self):
        with self.t.location(x=self.t.width-10):
          self.outfile.write("[ "),
          self.outfile.write(self.t.yellow("WARN")),
          self.outfile.write(" ]"),
        self.outfile.write("\n")


    # Print an INFO box.
    def infook(self):
        with self.t.location(x=self.t.width-10):
          self.outfile.write("[ "),
          self.outfile.write(self.t.blue("INFO")),
          self.outfile.write(" ]"),
        self.outfile.write("\n")


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


    # opts is a dict loaded with info:
    #      'log'  : 'what the function is doing',
    #      'ok'   : 'success message',
    #      'fail' : 'failure message'
    def exlog(self, callback, args=None, opts={}):
        if 'log' in opts.keys():
           self.logn(opts['log']);
        ret = False;
        try:
           if args:
              ret = callback(args);
           else: ret = callback();
           if 'ok' in opts.keys():
              self.info(opts['ok']);
        except QuietException as e:
           pass;
        except AlertException as e:
           self.alert(e.message);
        except Exception as e:
           exc_type, exc_obj, exc_tb = sys.exc_info()
           fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
           traceback.print_exc();
        return ret;


    # Print a prompt message.
    def prompt(self, args={
      'message' : ''
    }):

        import toolbelt
        if 'message' in args: 
              message = args['message'];
        else: message = args;
        p = self.t.magenta("*") + self.t.bold(" %s: " % message);

        # Fix response not sticking
        if 'type' in args and args['type'] == 'text':
           response = toolbelt.editors.vim();
        elif 'auto' in args:
           args['auto'].prompt = p;
           response = args['auto'].run();
        else: 
           self.outfile.write(p);
           self.outfile.flush();
           response = self.infile.readline();

        response = response.rstrip().lstrip();
        if response == '':
           args['response'] = '';
           return args;

        if 'type' in args:
           if args['type'] == 'datetime':
              q = toolbelt.quickdate.QuickDate(response);
              response = q.lex;
           elif args['type'] == 'float':
              response = float(response);
           elif args['type'] == 'int':
              response = int(response);
              
        args['response'] = response;
        return args;


    # Gather data into a dict, line by line,
    # with prompts
    def gather(self, args = {
       'keys'       : [], 
       'data'       : {}, 
       'types'      : {}, 
       'xs'         : None, 
       'overwrite'  : True,
       'auto'       : None
    }):


        args['keys']      = list(args['keys']);
        args['maxlength'] = max([len(key) for key in args['keys']]);
        args["keyindex"]  = 0;


        if not 'data' in args:
           args['data'] = {};

        if not 'xs' in args:
           args['xs'] = [];


        # Format the info and prompt messages
        def format(args):
            args['spaces']  = ' ' * (args['maxlength'] - len(args['keys'][args['keyindex']]));
            args['message'] = "%s%s  " % (args['keys'][args['keyindex']], args['spaces'])
            if args['keys'][args['keyindex']] in args['data'].keys():
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
               args['type'] = args['types'][args['keys'][args['keyindex']]]
            if args["keys"][args["keyindex"]] in args['data'].keys():
               self.info(args['info']);
               if 'overwrite' in args and not args['overwrite']:
                  args["keyindex"] += 1;
                  return args;
            args = self.prompt(args);
            if args["response"] != '':
               args["data"][args["keys"][args["keyindex"]]] = args["response"];
            args["keyindex"] += 1;
            return args;
            

        # Gather xs
        args = gatherxs(args);

        # Gather words
        if 'words' in args and args['words']:
           while args["keyindex"] < len(args["keys"]):
                 args = gatherwords(args);

        # Gather lines
        else: 
          while args["keyindex"] < len(args["keys"]):
                #self.print(args);
                args = gatherline(args);

        #print(args);
        return args;


    # Pretty-print a dictionary
    def logdata(self, args):
        if 'data' not in args:
           return;
        d = args['data'];
        if len(d) == 0: return;
        l = max([len(k) for k in d]);
        i = 0
        for k in d:
            if 'types' in args:
               if k in args['types']:
                   if args['types'][k] == "text":
                      d[k] = self.wrap({
                        'msg'    : d[k],
                        'linelen': 80
                      });
            i = i + 1;
            sp = ' ' * (l - len(k));
            self.info("  %s%s : %s" % (k, sp, d[k]));


    # args = {
    #  'linelen' : 'length of line'
    #  'msg'     : 'message to print
    #}
    def wrap(self, args):
        if 'msg' in args:
           if args['msg']:
              msglen  = len(args['msg'])
              linelen = args['linelen']
              if msglen < linelen: return args['msg'];
              args['msg'] = args['msg'].replace('\n', ' ');
              nolines = int(msglen/args['linelen']);
              msg = '\n';
              #args['msg'];
              for i in range(0, nolines):
                  msg += args['msg'][i*linelen:(i+1)*linelen] + '\n';
              return msg + args['msg'][(i+1)*linelen:];
        return '';
        
        
    def print(self, args):
        pprint.pprint(args);


    # Print a table
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
            self.outfile.write(self.t.yellow("%s%s" % (key[:textwidth], spaces)));
        self.outfile.write("\n");
        #print(keys, data);
        for row in data:
            for key in keys:
                element   = str(row[key]);
                numspaces = colspace if textwidth < len(element) else colwidth-len(element)
                spaces    =  ' ' * numspaces;
                self.outfile.write("%s%s" % (element[:textwidth], spaces));
            self.outfile.write("\n");

