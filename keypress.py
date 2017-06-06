#!/usr/bin/env python
from subprocess import Popen, PIPE
from time import sleep

control_q_sequence = '''keydown Control_L
key Q
keyup Control_L
'''

def keypress(sequence):
    p = Popen(['xte'], stdin=PIPE)
    p.communicate(input=sequence)

sleep(120)
keypress(control_q_sequence)
keypress(control_q_sequence)
keypress(control_q_sequence)
keypress(control_q_sequence)
keypress(control_q_sequence)
