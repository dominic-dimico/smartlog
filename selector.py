#!/usr/bin/python
import smartlog
import sys


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



class Selector(smartlog.Smartlog):


    def __init__(self, ls):
          super().__init__();
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
                 if i == c.y:    self.write("   > "+t.black_on_yellow(s));
                 elif i in sels: self.write("   > "+t.yellow(s));
                 else:           self.write("   > "+t.white(s));
                 self.outfile.flush();


    def radio(self):
        ls = self.ls; c = self.c; t = self.t; 
        n = self.n; z = None;
        self.write("Select one:\n"+"\n"*n);
        while not z:
            self.draw();
            (_, z) = c.kb.wait();
        (x, y) = z;
        return y;


    def check(self):
        c = self.c; t = self.t; n = self.n;
        z = self.z; k = '';  sels = [];
        self.write("Select any (q to quit): \n"+"\n"*n);
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
             self.write("   > ");
             if isinstance(ls, dict):
                self.write(self.space(self.ks[c.y])+": ");
             self.outfile.flush();
        with t.location(0, t.height-n+c.y-1):
             inp = input();
        with t.location(0, t.height-n+c.y-1):
             self.write("   > ");
             self.write(self.space(self.ks[c.y])+": ");
             self.write(' '*len(str(ls[self.ks[c.y]])));
        return inp;


    def edit(self):
        c = self.c; t = self.t; n = self.n;
        ls = self.ls; z = self.z; k = ''; 
        eds = [];
        self.write("q to quit: \n"+"\n"*n);
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
        

class DataSelector(smartlog.Smartlog):

      def __init__(self, ds):
          super().__init__();
          import toolbelt;
          #self = log;
          #self.t   = log.t;
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
                   self.write(t.yellow(self.space(k)));
              j += 1;


      def color(self, i):
          colors = ['blue', 'yellow', 'green', 'purple', 'red']
          if 'color' in self.ks:
             return self.ds[i]['color']
          elif 'tags' in self.ks[i]:
             for c in colors:
                 if c in self.ks[i]['tags']:
                    return c;
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
                      self.write(s.format(t=t));
                      j += 1;
          self.outfile.flush();


      def check(self):
          c = self.c; t = self.t; n = self.n;
          z = self.z; k = ''; eds = [];
          self.write("Select any: \n"+"\n"*n);
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
               self.write(" > ");
               self.outfile.flush();
               v = input();
          k = self.ks[c.y];
          with self.t.location(0, self.t.height-2):
               self.write(" > "+' '*len(v));
          self.ds[c.x][k] = v;
          self.eds += (c.x, c.y);
          

      def edit(self):
          c  = self.c; t = self.t; n = self.n;
          z  = self.z; k = ''; eds = [];
          ds = self.ds;
          self.write("Select any: \n"+"\n"*n+"\n\n");
          while True:
                self.draw();
                (k, z) = c.kb.wait();
                if k=='q': break;
                if k=='\n':
                   self.editx();
          return self.ds;


