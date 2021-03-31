from macColors import *

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

        










        
