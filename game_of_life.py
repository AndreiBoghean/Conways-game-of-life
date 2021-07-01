from collections import namedtuple

def ask(msg):
    print(msg)
    return input()

def test1():
    print("test1")
    
def test2():
    print("test2")

placement_names = ["manual", "random"]
palcement_functions = [ test1, test2]
placement_mode = ask(f"what placement mode would you like to use? {' '.join(placement_names)}")
print(type(placement_mode))
print(f"placement mode: {int(placement_mode)}")

#named_characters = namedtuple("named_chars", "block_double empty_double")
#named_chars = named_characters("\u2588\u2588", "\u2591\u2591")

#rows = ask("how many rows?")
#cols = ask("how many columns?")
