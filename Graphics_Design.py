from turtle import *
import colorsys as cs

title("Graphics Design")
bgcolor("black")
tracer(200)

def draw():
    h=0
    n=20
    up()
    goto(0,30)
    down()
    pensize(5)
    for i in range(300):
        c=cs.hsv_to_rgb(h,1,1)
        h+=1/n
        color(c)
        fd(10)
        circle(i,4,10)
        for j in range(500):
            lt(971)
            circle(i* 0.1,j,steps=2)
            circle(i,2)

draw()
done()