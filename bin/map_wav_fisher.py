#!/usr/bin/env python

from __future__ import print_function

import sys
import errno
import os
from subprocess import check_call

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

if len(sys.argv) != 2:
  print("Usage: %s <mapping file>" % sys.argv[0])
  sys.exit(1)

fisher="/home/usuaris/veu4/jadrian/data/LDC/fisher_spa/data/speech/"
data="speech"
sph2pipe="/veu4/jadrian/projects/kaldi/egs/fisher_callhome_spanish/s5/../../../tools/sph2pipe_v2.5/sph2pipe"

transcript = None
mapping = {}
for line in sys.stdin:
  if line.startswith('##'):
    transcript = line.strip().split(' ')[2]
    lineno = 1
  else:
    mapping[(transcript,repr(lineno))] = line.strip()
    lineno += 1

for line in open(sys.argv[1]):
  transcript, ids = line.split()
  ids = ids.split('_')
  t_ini = mapping[(transcript,ids[0])].split()
  t_end = mapping[(transcript,ids[-1])].split()
  print(t_ini, t_end)
  fname = t_ini[0].split('.')
  mkdir_p("{}/{}".format(data,fname[0]))
  wavf = "{}/{}/{}_{}_{}.wav".format(data,fname[0],fname[0],ids[0],ids[-1])
  s_ini = float(t_ini[2])
  s_end = float(t_end[-1])
  if s_end <= s_ini:
    s_end = s_ini + 0.01
  cmd = "{} -f wav -p -c {} -t {}:{} {} {}".format(sph2pipe, int(t_ini[1])+1, s_ini, s_end, fisher+t_ini[0], wavf)
  print(wavf)
  check_call(cmd, shell=True)
