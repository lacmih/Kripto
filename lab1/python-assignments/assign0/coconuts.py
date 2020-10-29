#!/usr/bin/env python3
"""Module-level comment."""

def main():
    bird_weight = float(input("How many ounces of birds are carrying the coconuts? "))
    coconut_weight = float(input("How many pounds of coconuts are there? "))
    if bird_weight / coconut_weight >= 5.5:
        print("Yes! Carrying the coconuts is possible.")
    else:
        print("No. Carrying the coconuts is impossible.")

if __name__ == '__main__':
    main()
