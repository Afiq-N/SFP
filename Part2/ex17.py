# TODO: Refer to the objective and sample output and figure out your own code!
# Time to graduate :p
import random
animals = ["Dog", "Cat", "Eagle"]
adjectives = ["Curious", "Stinky", "Smart"]
name = input("What's your name?")
print("Hello " +f"{name}" + "," + " " + "your codename is " + f"{random.choice(adjectives)}" + " " + f"{random.choice(animals)}" + ".")
