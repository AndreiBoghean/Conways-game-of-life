from collections import namedtuple

def ask(msg):
    print(msg)
    return input()

named_characters = namedtuple("named_chars", "block_double empty_double")
named_chars = named_characters("\u2588\u2588", "\u2591\u2591")

rows = ask("how many rows?")
cols = ask("how many columns?")

operation_mode = namedtouple("operation_mode", "mode_name mode_entry_point")

operation_modes = { operation_mode() }
operation_mode = ask("how would you like to run? " + " ".join(operation_modes) )



exit()
for i in range(10):
    outp += named_chars.block_double
    outp += named_chars.empty_double

print(outp)