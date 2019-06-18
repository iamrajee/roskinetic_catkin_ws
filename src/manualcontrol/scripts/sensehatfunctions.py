from sense_hat import SenseHat
from time import sleep
from time import *
sense = SenseHat()

def emoji(face):
    yin=100
    y = (yin, yin, 0) #Yellow
    win = 200
    b = (win,win,win) # White
    smiley_face = [
       y, y, y, y, y, y, y, y,
       y, y, y, y, y, y, y, y,
       y, b, b, y, y, b, b, y,
       y, b, b, y, y, b, b, y,
       y, y, y, y, y, y, y, y,
       y, b, b, y, y, b, b, y,
       y, y, y, b, b, y, y, y,
       y, y, y, y, y, y, y, y
    ]
    frowning_face = [
       y, y, y, y, y, y, y, y,
       y, y, y, y, y, y, y, y,
       y, b, b, y, y, b, b, y,
       y, b, b, y, y, b, b, y,
       y, y, y, y, y, y, y, y,
       y, y, y, b, b, y, y, y,
       y, y, b, y, y, b, y, y,
       y, b, y, y, y, y, b, y
    ]
    if face == "smile":
       sense.set_pixels(smiley_face)
    elif face == "sad":
       sense.set_pixels(frowning_face)
def clear():
	sense.clear()
def red():
        rin=255
        r = (rin, 0, 0) #red
        sense.set_pixels([r for i in range(64)])
def green():
        gin = 255
        g = (0, gin, 0) #green
        sense.set_pixels([g for i in range(64)])
def blue():
        bin = 255
        b = (0, 0, bin) #blue
        sense.set_pixels([b for i in range(64)])
def print_text(text):
        sense.show_message(text)

def rotate(angle):
        sense.set_rotation(angle)
def temp():
        return sense.get_temperature()
def pres():
        return sense.get_temperature()
def humi():
        return sense.get_temperature()
def compass():
        return sense.get_compass()
def display_env():
        sense.show_message("T="+str(temp()).split(".")[0])
	sense.show_message("P="+str(pres()).split(".")[0])
	sense.show_message("H="+str(humi()).split(".")[0])
def arrow(dir):
        X = (255, 0, 0)
        O = (0, 0, 0)
        arrowmat = [
            O, O, O, X, X, O, O, O,
            O, O, X, X, X, X, O, O,
            O, X, O, X, X, O, X, O,
            X, O, O, X, X, O, O, X,
            O, O, O, X, X, O, O, O,
            O, O, O, X, X, O, O, O,
            O, O, O, X, X, O, O, O,
            O, O, O, X, X, O, O, O
        ]
        sense.set_pixels(arrowmat)
        if dir == "L":
                sense.set_rotation(90)
        elif dir == "F":
                sense.set_rotation(180)
        elif dir == "R":
                sense.set_rotation(270)
        elif dir == "B":
                sense.set_rotation(0)

def orient():
        return sense.get_orientation().values()
def rainbow():
        rainbow_pixels = [
            [255, 0, 0], [255, 0, 0], [255, 87, 0], [255, 196, 0], [205, 255, 0], [95, 255, 0], [0, 255, 13], [0, 255, 122],
            [255, 0, 0], [255, 96, 0], [255, 205, 0], [196, 255, 0], [87, 255, 0], [0, 255, 22], [0, 255, 131], [0, 255, 240],
            [255, 105, 0], [255, 214, 0], [187, 255, 0], [78, 255, 0], [0, 255, 30], [0, 255, 140], [0, 255, 248], [0, 152, 255],
            [255, 223, 0], [178, 255, 0], [70, 255, 0], [0, 255, 40], [0, 255, 148], [0, 253, 255], [0, 144, 255], [0, 34, 255],
            [170, 255, 0], [61, 255, 0], [0, 255, 48], [0, 255, 157], [0, 243, 255], [0, 134, 255], [0, 26, 255], [83, 0, 255],
            [52, 255, 0], [0, 255, 57], [0, 255, 166], [0, 235, 255], [0, 126, 255], [0, 17, 255], [92, 0, 255], [201, 0, 255],
            [0, 255, 66], [0, 255, 174], [0, 226, 255], [0, 117, 255], [0, 8, 255], [100, 0, 255], [210, 0, 255], [255, 0, 192],
            [0, 255, 183], [0, 217, 255], [0, 109, 255], [0, 0, 255], [110, 0, 255], [218, 0, 255], [255, 0, 183], [255, 0, 74]
        ]
        sense.set_pixels(rainbow_pixels)
'''
emoji("smile")
sleep(1)
emoji("sad")
sleep(1)
print_text("rajee")
rainbow()
sleep(1)
emoji("smile")
sleep(1)
rotate(90)
emoji("smile")
sleep(1)
display_env()
'''
