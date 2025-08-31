color = {
    "None":"\033[0m",
    "red":"\033[31m",
    "green":"\033[32m", 
    "yellow":"\033[33m", 
    "blue":"\033[34m",
    "purple":"\033[35m",
    "cyan":"\033[36m", 
    "white":"\033[37m", 
    "GREY":"\033[90m",
    "RED":"\033[91m",
    "GREEN":"\033[92m", 
    "YELLOW":"\033[93m", 
    "BLUE":"\033[94m",
    "PURPLE":"\033[95m",
    "CYAN":"\033[96m", 
    "WHITE":"\033[97m", 
}
BackGround_color = {
    "None":"\033[0m",
    "black":"\033[40m",
    "red":"\033[41m",
    "green":"\033[42m", 
    "yellow":"\033[43m", 
    "blue":"\033[44m",
    "purple":"\033[45m",
    "cyan":"\033[46m", 
    "white":"\033[47m", 
}

def demo():
    greyFound = False
    print("**Normal Colors**")
    for colors,ID in color.items():
        if colors == 'GREY':
            print(f"{color['None']}**Bright Colors**")
        print(f"{ID}{colors}")
    print("**BackGround Colors**")
    for name,Id in BackGround_color.items():
        blank = BackGround_color["None"]
        print(f"{Id}{name}{blank}")
    print(color["None"])

if __name__ == '__main__':
    demo()
