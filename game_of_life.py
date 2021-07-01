from collections import namedtuple

def ask(msg):
    print(msg)
    return input()

placement_mode = namedtouple("operation_mode", "mode_name mode_entry_point")

placement_modes = { placement_mode("manual-placement", "placement-function-1"), placement_mode("random-placement", "placement-function-2") }

placement_mode = ask("test")

named_characters = namedtuple("named_chars", "block_double empty_double")
named_chars = named_characters("\u2588\u2588", "\u2591\u2591")

rows = ask("how many rows?")
cols = ask("how many columns?")
