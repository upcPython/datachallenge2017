from matplotlib.colors import rgb2hex
def LerpColour(c1,c2,t):
    return (int(c1[0]+(c2[0]-c1[0])*t),int(c1[1]+(c2[1]-c1[1])*t),int(c1[2]+(c2[2]-c1[2])*t))

def gradient(color_list,no_steps = 100):
    colors = []
    for i in range(len(color_list)-1):
        for j in range(no_steps):
            colors.append(LerpColour(color_list[i],color_list[i+1],j/no_steps))
    return colors

def getColor(radio):
    '''0<=radio<=1'''
    list_of_colors = [(254, 240, 217), (253, 204, 138), (252, 141, 89), (227, 74, 51), (179, 0, 0)]
    colors = gradient(list_of_colors)
    return '#%02x%02x%02x' % colors[int((len(colors)-1)*radio)]

if __name__ == "__main__":
    for i in range(20):
        print(getColor(i/19))