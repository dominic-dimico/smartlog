from blessings import Terminal
from sys       import stdin
import os


t = Terminal()


# Print an alert message.
def alert(msg):
    print t.red("*"), 
    print t.bold("Alert:"),
    print "%s!" % msg,
    rok()


# Print an alert message.
def prompt(msg):
    print t.magenta("*"), 
    print t.bold("%s: " % msg),
    ret = stdin.readline();
    return ret.rstrip().lstrip();

# Print a WARN message.
def warn(msg):
    print t.yellow("*"), 
    print t.bold("Warning:"),
    print "%s." % msg,
    warnok()


def optip(msg):
    """
    Give a tip that says:
    
    "You can set it with the %s flag."
    """
    print t.blue("*"), 
    print "You can set it with the %s flag." % msg,
    infook()


# Print an INFO message.
def tip(msg):
    print t.blue("*"), 
    print "%s." % msg,
    infook()


# Print an log message, but no OK or FAIL box.
def log(msg):
    print t.green("*"), 
    print "%s..." % msg,


# Print an OK box.
def ok():
    with t.location(x=t.width-10):
      print "[ ",
      print t.green("OK"),
      print " ]",
    print ""


# Print a FAIL box.
def fail():
    with t.location(x=t.width-10):
      print "[",
      print t.red("FAIL"),
      print "]",
    print ""


# Print a yellow OK box.
def yok():
    with t.location(x=t.width-10):
      print "[ ",
      print t.yellow("OK"),
      print " ]",
    print ""


# Print a red OK box.
def rok():
    with t.location(x=t.width-10):
      print "[ ",
      print t.red("OK"),
      print " ]",
    print ""


# Print a WARN box.
def warnok():
    with t.location(x=t.width-10):
      print "[",
      print t.yellow("WARN"),
      print "]",
    print ""


# Print an INFO box.
def infook():
    with t.location(x=t.width-10):
      print "[",
      print t.blue("INFO"),
      print "]",
    print ""


# Determine if program exists.
def which(program):
    str = ' '.join(["Checking location of",program])
    log(str)
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)
    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            ok()
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                ok()
                return exe_file
    fail()
    return None


# Check if directory exists.
def check_dir(name):
    str = ' '.join(["Checking if directory",name,"exists"])
    log(str)
    if os.path.isdir(name):
        ok()
        return True
    else:
        fail()
        return False


# Check if file exists.
def check_file(name):
    str = ' '.join(["Checking if file",name,"exists"])
    log(str)
    if os.path.isfile(name):
        ok()
        return True
    else:
        fail()
        return False


# Check if environment variable is set.
def check_var(name):
    val = os.getkey(name)
    str = ' '.join(["Checking if variable",name,"is set"])
    log(str)
    if val:
        ok()
    else:
        fail()

