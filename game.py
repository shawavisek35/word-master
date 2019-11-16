#Word Master game 

#importing modules
from random import randint
import threading

#importing the contents of the file game.txt
f = open("game.txt","r")
game = f.read().split("\n")

#class for calculating the score
class Score(object):
    score = 0
    k = 0
    life = 3
    flag = 0

#for threading timer
def timeUp():
    print("Times Up!.....\nYou can still guess the correct answer but your score will not be increased : ")
    Score.flag = 1



class Scene(object):#Scene class
    def enter(self):
        print("Scene yet not configured............")

class Game(Scene):#inheritng from scene class
    def enter(self):
        Score.flag = 0
        l2 = []
        b = game[Score.k]
        Score.k = Score.k+1
        c = list(b)
        d = randint(3,4)
        for i in range(d):
            h = randint(0,len(c) - 1)
            if(h in l2):
                i = i-1
            else:
                l2.append(h)
        
        print("Word : ",end = " ")

        for j in range(len(c)):
            if(j in l2):
                print("__",end = " ")
            else:
                print(c[j],end = " ")
        print("\n")
        timer = threading.Timer(25.0,timeUp)
        timer.start()
        answer = input("Guess the correct word : ")
        if(answer==b):
            if(Score.flag==1):
                Score.flag = 0
            else:
                timer.cancel()
                Score.score = Score.score + 10
                print(f"Wohoo! You made it.\nYour score is : {Score.score}\n")
            
                if(Score.k == len(game)):
                    return "over"
            
        else:
            if(Score.flag==1):
                Score.flag = 0
            else:
                timer.cancel()
                Score.score = Score.score - 5
                Score.life = Score.life - 1
                print(f"Ahaa!! Wrong answer.\nCorrect answer is : {b}\nYour score is : {Score.score}\n")
            
                if(Score.life == 0):
                    return "lifeN"
                elif(Score.k == len(game)):
                    return "over"


        prompt = input("Would you like to continue[Yes(y)/No(n)] : ")
        if(prompt == 'n' or prompt == 'no' or prompt == 'No'):
            return "end"
        else:
            return "game"

class End(Scene):#inheritng from scene class
    def enter(self):
        print("You wished to discontinue the game.........\n")
        return "finished"

class GameOver(Scene):#inheritng from scene class
    def enter(self):
        print("The game is over you made it to the second round.........\n")
        return "finished"

class LifeOver(Scene):
    def enter(self):
        print("Your life is over..........\n")
        return "finished"

class Finished(Scene):#inheritng from scene class
    def enter(self):
        print("********************Thanks for playing**********************")
        print(f"Your Score is ||{Score.score}||\n")

class Map(object):
    mapping = {"game":Game(),
                "end":End(),
                "over":GameOver(),
                "lifeN":LifeOver(),
                "finished":Finished()}
    def __init__(self,start):
        self.start = start

    def nextScene(self,scene):
        val = Map.mapping[scene]
        return val
    def OpeningScene(self):
        return self.nextScene(self.start)

class Engine(object):
    def __init__(self,map):
        self.map = map
    def play(self):
        currentScene = self.map.OpeningScene()
        lastScene = self.map.nextScene("finished")
        while(currentScene!=lastScene):
            next = currentScene.enter()
            currentScene = self.map.nextScene(next)

        currentScene.enter()


if __name__=="__main__":
    a = Map("game")
    gi = Engine(a)
    gi.play()
