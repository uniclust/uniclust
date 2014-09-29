# An implementation of Dartmouth BASIC (1964)
#

import sys
sys.path.insert(0,"../..")

if sys.version_info[0] >= 3:
    raw_input = input

import UNILAlex
import UNILAparse
import UNILAinterp

# If a filename has been specified, we try to run it.
# If a runtime error occurs, we bail out and enter
# interactive mode below
if len(sys.argv) == 2:
    data = open(sys.argv[1]).read()
    prog = UNILAparse.parse(data)
    if not prog: raise SystemExit
    u = UNILAinterp.UNILAInterpreter(prog)
    try:
        u.run()
        raise SystemExit
    except RuntimeError:
        pass

else:
    u = UNILAinterp.UNILAInterpreter({})

# Interactive mode.  This incrementally adds/deletes statements
# from the program stored in the BasicInterpreter object.  In
# addition, special commands 'NEW','LIST',and 'RUN' are added.
# Specifying a line number with no code deletes that line from
# the program.

while 1:
    try:
        line = raw_input("[UNILA] ")
    except EOFError:
        raise SystemExit
    if not line: continue
    line += "\n"
    prog = UNILAparse.parse(line)
    if not prog: continue

    keys = list(prog)

    if keys[0] > 0:
         u.add_statements(prog)
    else:
         stat = prog[keys[0]]
         if stat[0] == 'run':
             try:
                 u.run()
             except RuntimeError:
                 pass
         elif stat[0] == 'LIST':
             u.list()
         elif stat[0] == 'BLANK':
             u.del_line(stat[1])
         elif stat[0] == 'NEW':
             u.new()

  
            






