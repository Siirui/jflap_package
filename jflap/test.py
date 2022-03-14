import jflap_basic as jf
import os

test = jf.Jflap("test")
test.create_file(os.getcwd())
test.add_state("q0","0,0", initial=True)
test.add_state("q1","1,2", final=True)
test.add_state("q2", "ready to be deleted", final=True, initial=True)
test.create_sigma(['0', '1', '2', '3', '4'])
test.add_transition(0, 1, ['0'])
test.add_transition(1, 0, ['2'])
test.add_transition(0, 1, ['1'])
test.add_transition(1, 2, ["/sigma"])
test.change_state(0, initial=False)
test.change_state(1, final=False)
test.change_state_label(1, "I am state 1")
test.change_transition(0, 1, pre_symbols=[], new_symbols=['3', '4'], all=True)
help(test.add_transition)