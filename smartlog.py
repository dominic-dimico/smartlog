from   blessings import Terminal
import sys
import os


class Smartlog():

    t  = None;
    fd = None;


    def __init__(self, filename="/dev/stdout"):
        try: self.fd = open(filename, "a");
        except: print("File Exception");
        self.t = Terminal(stream=self.fd, force_styling=True);


    # Be silent
    def quiet(self):
        self.fd = open('/dev/null', "a");


    # Continue printint to stdout
    def resume(self):
        self.fd = open('/dev/stdout', "a");


    # Print an alert message.
    def reprint(self, msg):
        self.fd.write("\r\033[K"+msg);


    # Print an alert message.
    def alert(self, msg):
        self.fd.write(self.t.red("*")), 
        self.fd.write(self.t.bold(" Alert:")),
        self.fd.write(" %s!" % msg),
        self.rok()


    # Print a prompt message.
    def prompt(self, msg, opts={}):
        p = self.t.magenta("*") + self.t.bold(" %s: " % msg);
        self.fd.write(p);
        self.fd.flush();
        if opts['auto']:
           opts['auto'].prompt = p;
           ret = opts['auto'].run();
        else: ret = sys.stdin.readline();
        return ret.rstrip().lstrip();


    # Print an alert message.
    def yesno(self, msg):
        self.fd.write(self.t.magenta("*")), 
        self.fd.write(self.t.bold(" %s? (y/n): " % msg)),
        self.fd.flush();
        ret = sys.stdin.readline();
        if ret.rstrip().lstrip() == 'y':
           return True;
        else: return False;


    # Print a WARN message.
    def warn(self, msg):
        self.fd.write(self.t.yellow("*")), 
        self.fd.write(self.t.bold(" Warning:")),
        self.fd.write(" %s." % msg),
        self.warnok()


    def optip(self, msg):
        """
        Give a tip that says:
        
        "You can set it with the %s flag."
        """
        self.fd.write(self.t.blue("*")), 
        self.fd.write(" You can set it with the %s flag." % msg),
        self.infook()


    # Print an INFO message.
    def tip(self, msg):
        self.fd.write(self.t.blue("*")), 
        self.fd.write(" %s." % msg),
        self.infook()


    # Print an INFO message.
    def info(self, msg):
        self.fd.write(self.t.blue("*")), 
        self.fd.write(" %s" % msg),
        self.infook()


    # Print an log message, but no OK or FAIL box.
    def log(self, msg):
        self.fd.write(self.t.green("*")), 
        self.fd.write(" %s..." % msg),

    # Print an log message, but no OK or FAIL box.
    def logn(self, msg):
        self.log(msg);
        self.fd.write("\n");

    # Print an log message, with OK.
    def logok(self, msg):
        self.log(msg);
        self.ok();

    # Print an log message, with no OK and newline.
    def lognok(self, msg):
        self.log(msg);
        self.fd.write("\n");

    # Print an OK box.
    def ok(self):
        with self.t.location(x=self.t.width-10):
          self.fd.write("[  "),
          self.fd.write(self.t.green("OK")),
          self.fd.write("  ]"),
        self.fd.write("\n")
        #self.fd.write(str(self.t.width)+"\n")


    # Print a FAIL box.
    def fail(self):
        with self.t.location(x=self.t.width-10):
          self.fd.write("[ "),
          self.fd.write(self.t.red("FAIL")),
          self.fd.write(" ]"),
        self.fd.write("\n")


    # Print a yellow OK box.
    def yok(self):
        with self.t.location(x=self.t.width-10):
          self.fd.write("[  "),
          self.fd.write(self.t.yellow("OK")),
          self.fd.write("  ]"),
        self.fd.write("\n")


    # Print a red OK box.
    def rok(self):
        with self.t.location(x=self.t.width-10):
          self.fd.write("[  "),
          self.fd.write(self.t.red("OK")),
          self.fd.write("  ]"),
        self.fd.write("\n")


    # Print a WARN box.
    def warnok(self):
        with self.t.location(x=self.t.width-10):
          self.fd.write("[ "),
          self.fd.write(self.t.yellow("WARN")),
          self.fd.write(" ]"),
        self.fd.write("\n")


    # Print an INFO box.
    def infook(self):
        with self.t.location(x=self.t.width-10):
          self.fd.write("[ "),
          self.fd.write(self.t.blue("INFO")),
          self.fd.write(" ]"),
        self.fd.write("\n")


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


    # opts is a dictionary loaded with info:
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
        except Exception as e:
           self.fail();
           if 'fail' in opts.keys():
              self.alert(opts['fail']);
              self.alert(e);
        return ret;



    # Gather data into a dictionary, line by line,
    # with prompts
    def gather(self, keys, xs=[], d={}, opts={
       'overwrite' : True
      }
    ):
        keys = list(keys);
        maxlength = max([len(key) for key in keys]);
        i = 0;
        j = 0;
        # Gather from xs
        for i in range(len(xs)):
            spaces = ' ' * (maxlength - len(keys[i]));
            if i >= len(keys):
               self.warn("More inputs than keys");
               return d;
            d[keys[i]] = xs[i];

        # Gather remaining keys from here
        for j in range(i, len(keys)):
            key = keys[j];
            spaces = ' ' * (maxlength - len(key));
            x = None;
            if key in d.keys():
               self.info("%s%s  : %s" % (key, spaces, d[key]));
               if opts['overwrite']:
                  x = self.prompt("%s%s  " % (key, spaces));
            else: x = self.prompt("%s%s  " % (key, spaces));
            if x: d[key] = x;
        return d;


    # Gather words into a dictionary.  Prompts may be given
    # one at a time for each word, or all words may be entered
    # on a single line.
    #
    #   keys - keys to gather, in order
    #   y    - starter list
    #
    def gatherwords(self, keys, xs=None, d={}, opts={}):
        maxlength = max([len(key) for key in keys]);
        i = 0;
        while True:
            # Columnate the keys and prompts with spaces (sp)
            spaces = ' ' * (maxlength - len(keys[i]));
            if not xs:
              x  = self.prompt("%s%s  " % (keys[i], spaces));
              xs = x.split(" ");
            n = i + len(xs);
            k = 0;
            # Loop over ith key to i+size of input (y) to copy in
            for j in range(i, n):
                d[keys[j]] = xs[k];
                i = i + 1;
                k = k + 1;
                if i >= len(keys): 
                   d['xs'] = xs[k:];
                   return d;
            xs = None;
        return d;


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
            self.fd.write(self.t.yellow("%s%s" % (key[:textwidth], spaces)));
        self.fd.write("\n");
        for row in data:
            for key in keys:
                element   = str(row[key]);
                numspaces = colspace if textwidth < len(element) else colwidth-len(element)
                spaces    =  ' ' * numspaces;
                self.fd.write("%s%s" % (element[:textwidth], spaces));
            self.fd.write("\n");


