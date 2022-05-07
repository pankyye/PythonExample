import turtle
import math



def square(t,length):
	for i in range(4):
		t.fd(length)
		t.lt(90)


def polyline(t,n,length,angle):
	for i in range(n):
		t.fd(length)
		t.lt(angle)

def polygon(t,n,length):
	angle=360/n
	polyline(t,n,length,angle)


def arc(t,r,angle):
	arc_length=2*math.pi*r*angle/360
	n=int(arc_length/3)+1
	step_length=arc_length/n
	step_angle=angle/n
	t.lt(step_angle/2)
	polyline(t,n,step_length,step_angle)
	t.rt(step_angle/2)


def circle(t,r):
	arc(t,r,360)


def petal(t,r,angle):
	for i in range(2):
		arc(t,r,angle)
		t.lt(180-angle)

def flower(t,n,r,angle):
	for i in range(n):
		petal(t,r,angle)
		t.lt(360/n)

def move(t,length):
	t.pu()
	t.fd(length)
	t.pd()

bob=turtle.Turtle()

move(bob,-100)
flower(bob,n=7,r=60,angle=60)

move(bob,100)
flower(bob,n=10,r=50,angle=60)

move(bob,100)
flower(bob,n=20,r=140,angle=20)

bob.hideturtle()
turtle.mainloop()














