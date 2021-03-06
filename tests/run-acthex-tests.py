#!/usr/bin/env python3

import unittest
import subprocess
import re
import sys
import logging
import os

logging.basicConfig(
  level=logging.DEBUG, stream=sys.stderr,
  format="%(levelname)1s:%(filename)10s:%(lineno)3d:%(message)s")

INPUTDIR='./inputs/'

class BubbleSortTestcase(unittest.TestCase):
  def my_run(self, hexfile):
    params = os.path.join(INPUTDIR, hexfile)
    return subprocess.run('acthex --pluginpath=../plugins --plugin=acthex-testplugin '+params,
                          shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf8')

  def test_persistenceenv(self):
    hexfile = 'acthex_bubblesort_persistenceenv.hex'
    proc = self.my_run(hexfile)
    for line in proc.stderr.split('\n'):
      logging.debug("E: %s", line.rstrip())
    self.assertEqual(proc.stderr, '')

    lastValue = None
    for line in proc.stdout.split('\n'):
      logging.debug("O: %s", line.rstrip())
      if line.startswith('Sequence is '):
        lastValue = line
    integers = lastValue.split(' ')[2:]
    logging.debug('integers: '+repr(integers))
    self.assertEqual([int(x) for x in integers], [1, 2, 2, 3, 3, 5, 6])

  def test_sortenv(self):
    hexfile = 'acthex_bubblesort_sortenv.hex'
    proc = self.my_run(hexfile)
    for line in proc.stderr.split('\n'):
      logging.debug("E: %s", line.rstrip())
    self.assertEqual(proc.stderr, '')

    lastValue = None
    for line in proc.stdout.split('\n'):
      logging.debug("O: %s", line.rstrip())
      if line.startswith('Value: '):
        lastValue = line
    mos = re.findall(r'\s([0-9]+)', lastValue)
    logging.debug("mos "+repr(mos))
    self.assertEqual([int(x) for x in mos], [1, 2, 2, 3, 3, 5, 6])

if __name__ == '__main__':
  unittest.main()
