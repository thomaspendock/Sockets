def bit8RGB(r, g, b):
    index = b + 6 * g + 36 * r + 16
    return index

def color(s, code, index=256, rgb=None):
    if rgb: index = bit8RGB(*rgb)
    color_reset = '[%dm'
    color_index = '[%d;5;%dm'
    return color_index % (code, index) + s + color_reset % (code + 1)
    
def fg(s, index=256, rgb=None):
    return color(s, 38, index, rgb)

def bg(s, index=256, rgb=None):
    return color(s, 48, index, rgb)


if __name__ == '__main__':
    for i in range(0, 256 // 6):
        for j in range(0, 6):

            index = 6*i + j - 2
            
            #s = (fg_index % index) + str(index) + fg_reset
            s = fg(bg(str(index), index), index)
            print(s, end=' ')

        print('')


# right is blue
# down is green
# block down is red
# 6 colors each

# start at 16
# % 36 == blue
# % 6  == green
# r    == red



