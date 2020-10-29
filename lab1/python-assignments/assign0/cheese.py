#!/usr/bin/env python3
"""Module-level comment."""

def main():
    cheeses = ["Muenster", "Cheddar", "Red Leicester"]
    print("Good morning. Welcome to the National Cheese Emporium!")

    out = 0
    while out == 0:
        print("What would you like, good Sir?")
        cheese = input()
        if cheese in ["You... do have some cheese, don't you?", "Have you in fact got any cheese here at all?"]:
            print("We have " + str(len(cheeses)) + " cheese(s)!")
            for i in cheeses:
                print(i)
        else:
            if cheese in cheeses:
                print("We have " + cheese + ", yessir.")
                out = 1
            else:
                print("I'm afraid we don't have any " + cheese + ".")

if __name__ == '__main__':
    main()
