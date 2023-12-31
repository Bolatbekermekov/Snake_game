import tkinter
from random import randint



SIDE=700
snake_size=50
class Snake:
    def __init__(self,window,canvas):
        self.canvas=canvas
        self.window=window
        self.body=[
            self.canvas.create_rectangle((SIDE//2- snake_size,SIDE//2-snake_size),
            (SIDE//2,SIDE//2), fill='#00FF00')


        ]
        self.direction='space'#pause
        self.direction_x=0
        self.direction_y=0

    def move(self,food):
        global score
        if self.direction!='space':
            for i in range(len(self.body)-1,0,-1):
               prev_x,prev_y,_,_= self.canvas.coords(self.body[i-1])
               curr_x,curr_y,_,_= self.canvas.coords(self.body[i])
               self.canvas.move(self.body[i],prev_x-curr_x,prev_y-curr_y)

        self.canvas.move(self.body[0],self.direction_x,self.direction_y)
        self.fix_overflow()
        if self.collide_food(food):
            score+=1
            self.grow()
            label.config(text=f"Score: {score}")
            food.recreate()
        elif self.collide_itsef():
            game_over()
            return
        self.window.after(250,self.move,food)


    def collide_itsef(self):
        head_x,head_y,_,_ = self.canvas.coords(self.body[0])
        for i in range(1,len(self.body)):
            x0,y0,_,_=self.canvas.coords(self.body[i])
            if head_x==x0 and head_y==y0:
                return True
        return False
    def fix_overflow(self):
        for part in self.body:
            x0,y0,x1,y1=self.canvas.coords(part)
            if self.direction == "Up" and y0<0:
                self.canvas.move(part,0,SIDE)
            elif self.direction == "Down" and y1 > SIDE:
                self.canvas.move(part, 0, -SIDE)
            elif self.direction == "left" and x0 <0 :
                self.canvas.move(part, SIDE, 0)
            elif self.direction == "Right" and x1 > SIDE:
                self.canvas.move(part, -SIDE, 0)

    def turn(self,event):
        if event.keysym=="Up" and self.direction!="Down":
            self.direction_x=0
            self.direction_y=-snake_size
            self.direction = event.keysym

        elif event.keysym=="Down" and self.direction!="Up":
            self.direction_x=0
            self.direction_y=snake_size
            self.direction = event.keysym

        elif event.keysym=="Left" and self.direction!="Right":
            self.direction_x=-snake_size
            self.direction_y=0
            self.direction = event.keysym

        elif event.keysym=="Right" and self.direction!="Left":
            self.direction_x=snake_size
            self.direction_y=0
            self.direction = event.keysym

        elif event.keysym == "space":
                self.direction_x = 0
                self.direction_y = 0
                self.direction=event.keysym
    def collide_food(self,food):
        # snake head coordinates
        head_x,head_y,_,_=self.canvas.coords(self.body[0])
        #food coordinates
        food_x, food_y, _, _ =self.canvas.coords(food.circle)
        if head_x ==food_x and head_y==food_y:
            return True
        return False
    def grow(self):
        x0,y0,x1,y1=self.canvas.coords(self.body[-1])
        new_part=self.canvas.create_rectangle((x0+self.direction_x,y0+self.direction_y),
            (x1+self.direction_x,y1+self.direction_y), fill='#00FF00')
        self.body.append(new_part)



class Food:
    def __init__(self,canvas):
        self.canvas=canvas
        self.circle=None
        self.create()
    def create(self):
        number_of_cols=SIDE // snake_size
        x=randint(0,number_of_cols-1)*snake_size
        y=randint(0,number_of_cols-1)*snake_size
        self.circle=self.canvas.create_oval(
            x,y,
            x+snake_size,      y+snake_size,
            fill='red',
            tag="food"
        )
    def recreate(self):
        self.canvas.delete("food")
        self.create()
def game_over():
    canvas.delete(tkinter.ALL)
    canvas.create_text(
        canvas.winfo_height()/2,
        canvas.winfo_height()/2,
        text="GAME OVER",
        font=('consolas',70),
        fill='red',
        tags='gameover')
    snake.direction = 'space'

score=0
window=tkinter.Tk()
window.resizable(False,False)
canvas=tkinter.Canvas(window,bg="black",height=SIDE,width=SIDE)
label=tkinter.Label(text=f"Score: {score}",font=('consolas',40))
#snake
snake=Snake(window,canvas)
#food
food=Food(canvas)

label.pack()
canvas.pack()
window.bind('<KeyPress>',snake.turn)
snake.move(food)
window.mainloop()