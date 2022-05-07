import turtle
import math

bob=turtle.Turtle()

def isosceles(t,r,angle):
	y=r*math.sin(angle*math.pi/180)
	t.rt(angle)
	t.fd(r)
	t.lt(90+angle)
	t.fd(2*y)
	t.lt(90+angle)
	t.fd(r)
	t.lt(180-angle)

def polypie(t,n,r):
	angle=360/n 
	for i in range(n):
		isosceles(t,r,angle/2)
		t.lt(angle)

def draw_pie(t,n,r):
	polypie(t,n,r)
	t.pu()
	t.fd(r*2+10)
	t.pd()


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

bob.pu()
bob.bk(130)
bob.pd()

size=40

draw_pie(bob,5,size)
draw_pie(bob,6,size)
draw_pie(bob,7,size)
draw_pie(bob,8,size)


bob.hideturtle()
turtle.mainloop()














