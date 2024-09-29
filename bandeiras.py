#import streamlit as st
import turtle
from turtle import *

sreen = turtle.Screen()
t = turtle.Turtle()
t.speed(5)

t.penup()
t.goto(0, 200)
t.pendown()
t.color("orange")
t.write("Bandeiras", align="center", font=("Arial", 24, "bold"))
  
# Green rectangle
def draw_orange_rectangle():
    t.color("green")
    t.begin_fill()
    t.forward(84)
    t.left(90)
    t.forward(400)
    t.left(90)
    t.forward(84)
    t.end_fill()
    
# Draw the circle Blue
def draw_blue_circle():
    t.penup()
    t.goto(35, 0)
    t.pendown()
    t.color("navy")
    t.begin_fill()
    t.circle(35)
    t.end_fill()
    
    # Draw the circle White
def draw_white_circle():
    t.penup()
    t.goto(35, 0)
    t.pendown()
    t.color("white")
    t.begin_fill()
    t.circle(30)
    t.end_fill()
        
# Draw blue circle of flag
def mini_blue():
    t.penup()
    t.goto(-27, -4)
    t.pendown()
    t.color("navy")
    for i in range(24):
        t.begin_fill()
        t.circle(2)
        t.end_fill()
        t.penup()
        t.forward(7)
        t.right(15)
        t.pendown()
                
# Small white circle of 
def draw_small_white_circle():
    t.color("navy")
    t.penup()
    t.goto(10, 0)
    t.pendown()
    t.begin_fill()
    t.circle(10)
    t.end_fill()

# Draw spokes of flag
def flag_spokes():
    t.penup()
    t.goto(0, 0)
    t.pendown
    t.pensize(1)
    for i in range(24):
        t.forward(30)
        t.backward(30)
        t.left(15)
        
# Drwa stck of flag
def flag_stick():
    t.color("brown")
    t.pensize(10)
    t.penup()
    t.goto(-200, -125)
    t.right(180)
    t.pendown()
    t.forward(800)
    
draw_orange_rectangle()
draw_blue_circle()
draw_white_circle()
mini_blue()
draw_small_white_circle()
flag_spokes()
flag_stick()

tuple.done()
            
            