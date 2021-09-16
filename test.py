import smartlog
import time 
import os

log = smartlog.Smartlog();
#os.mkfifo('~/.smartlog.fifo');
log.outfile = open('~/.smartlog.fifo', 'w');

while True:
      time.sleep(1);
      log.info("Hello!");
      log.outfile.flush();
