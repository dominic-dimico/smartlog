from   blessings import Terminal
from   sys       import stdin
import os


class Smartlog():

    t  = None;
    fd = None;

    def __init__(self, filename="/dev/stdout"):
        try: self.fd = open(filename, "a");
        except: print "File Exception"
        self.t = Terminal(stream=self.fd, force_styling=True);

    # Print an alert message.
    def alert(self, msg):
        self.fd.write(self.t.red("*")), 
        self.fd.write(self.t.bold("Alert:")),
        self.fd.write(" %s!" % msg),
        self.rok()


    # Print an alert message.
    def prompt(self, msg):
        self.fd.write(self.t.magenta("*")), 
        self.fd.write(self.t.bold(" %s: " % msg)),
        ret = stdin.readline();
        return reself.t.rstrip().lstrip();

    # Print a WARN message.
    def warn(self, msg):
        self.fd.write(self.t.yellow("*")), 
        self.fd.write(self.t.bold("Warning:")),
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
    def check_dir(self, name):
        str = ' '.join(["Checking if directory",name,"exists"])
        self.log(str)
        if os.path.isdir(name):
            self.ok()
            return True
        else:
            self.fail()
            return False


    # Check if file exists.
    def check_file(self, name):
        str = ' '.join(["Checking if file",name,"exists"])
        self.log(str)
        if os.path.isfile(name):
            self.ok()
            return True
        else:
            self.fail()
            return False


    # Check if environment variable is set
    def check_var(self, name):
        val = os.getkey(name)
        str = ' '.join(["Checking if variable",name,"is set"])
        self.log(str)
        if val:
            self.ok()
        else:
            self.fail()

