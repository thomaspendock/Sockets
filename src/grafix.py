from macColors import *
from random import randint
import sys
import time

def border(s, w, h, s_width=None, rgb=None, index=256):
    s_lines  = s.split('\n')
    if s_lines[-1] == '': s_lines = s_lines[:-1]
    s_height = len(s_lines)
    if not s_width:
        s_width = len(s_lines[0])
    verti_border = bg(' '*2, rgb=rgb, index=index)
    horiz_border = bg((' ' * s_width) + 2 * (w+1) * verti_border, rgb=rgb, index=index)

    border_s = ''
    
    border_s += horiz_border + '\n'
    
    for i in range(h):
        border_s += verti_border
        border_s += ' ' * (w * 4 + s_width)
        border_s += verti_border + '\n'

    for i in range(s_height):
        border_s += verti_border
        border_s += ' ' * (w * 2)
        border_s += s_lines[i]
        border_s += ' ' * (w * 2)
        border_s += verti_border + '\n'
    
    for i in range(h):
        border_s += verti_border
        border_s += ' ' * (w * 4 + s_width)
        border_s += verti_border + '\n'
    
    border_s += horiz_border + '\n'

    return border_s, s_width + 4 * w + 4

        
# GRAFIX ANIMATIONS !!! YESSSS

def light(s, i, color):
    '''Places a symmetrical light inside the text'''
    l = len(s)
    new_s = ''
    r = 10
    for j in range(len(s)):
        dis = abs(i - j)
        rj = 0 if dis > r else r - dis
        colorj = color + rj
        new_s += fg(s[j], index=colorj)
    
    return new_s, l, i < r + len(s), 0.019

def seperate(s, count, color):
    new_s = ''
    for c in s:
        new_s += ' '*(5 - count)
        new_s += c
    new_s += ' ' * len(s) # why did i need this???
    return new_s, len(new_s), count < 6, 0.15 + 0.019

def appear(s, i, color):
    base = 232
    return fg(s, index=base + i), len(s), i < 24, 0.045

def glitch(s, i, color):
    new_s = ''
    for j in range(len(s)):
        new_s += s[j] if j < i else chr(randint(ord('a'), ord('z')))
    return new_s, len(s), i < len(s), 0.019

def rev(s, count, color):
    '''write out each word in reverse, once completed reverse back'''
    new_s = ''
    letter_count = 0
    for word in s.split():
        new_word = ''
        stopped  = False
        for c in word[::-1]:
            if letter_count >= count:
                stopped = True
                break
            
            new_word += c
            letter_count += 1

        if stopped:
            new_s += fg(new_word, index=randint(0, 255))
        else:
            new_s += fg(new_word[::-1] + ' ', index=color)
            letter_count += 1
    new_s += ' '*(len(s) - letter_count)
    return new_s, len(s), count < len(s) - 1, 0.05

ANIMATIONS = [rev, glitch, light, seperate, appear]


def animate(s, color, animation):
    count = 0
    animating = True
    while animating:

        new_s, size, animating, wait = animation(s, count, color)

        # Print the modified string
        sys.stdout.write(new_s)
        sys.stdout.flush()

        # Wait for a split second
        time.sleep(wait)

        # Delete what was just printed 
        sys.stdout.write('\b' * size)

        count += 1

    sys.stdout.write(fg(s, index=color))
    sys.stdout.flush()











        
