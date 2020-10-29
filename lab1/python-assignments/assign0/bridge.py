#!/usr/bin/env python3
import random
"""Module-level comment."""

def question(answer):
    answer = answer.translate({ord(i): None for i in '!.'}).rstrip()
    return answer[len(answer) - 1]

def main():
    f = open("answers.txt", "r")
    qa = [i.split('? ') for i in f.readlines()]
    qa = [list([i[0], i[1].replace('\n', '').split('|')]) for i in qa]
    print(qa)
    ok = 0
    while(ok == 0):
        print("KEEPER: Stop! Who would cross the Bridge of Death must answer me these questions three, 'ere the other side he see.")
        print("KEEPER: What is your name?")
        name = input()
        if question(name) == '?':
            print("KEEPER: Auuuuuuuugh!")
            quit()
        print("KEEPER: What is your quest?")
        quest = input()
        if question(quest) == '?':
            print("KEEPER: Auuuuuuuugh!")
            quit()
        random_item = random.choice(qa)
        qa.remove(random_item)
        print("KEEPER: What is " + str(random_item[0]) + "?")
        answer = input()
        if answer in random_item[1]:
            print("Right. Off you go.")
        else:
            if question(answer) == '?':
                print("KEEPER: Auuuuuuuugh!")
                quit()
            else:
                print(str(name).upper()+ ": Auuuuuuuugh!")
        if len(qa) == 0:
            ok = 1
if __name__ == '__main__':
    main()
