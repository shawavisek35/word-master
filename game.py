
#Word Master game 

#importing modules
from random import randint
import threading
import pyttsx3
import datetime
import speech_recognition as sr
import time
import requests

#importing the contents of the file game.txt
#f = open("game.txt","r")
#game = f.read().split("\n")

'''lev = int(input("enter your choice :"))
if(lev == 1) :
    print(" You choose easy level ")
    speak(" You choose easy level ")
    f = open("easy.txt","r")
    game = f.read().split("\n")
elif(lev == 2):
     print(" You choose medium level ")
     speak(" You choose medium level ")
     f = open("medium.txt","r")
     game = f.read().split("\n")
elif (lev == 3):
     print(" You choose easy level ")
     speak(" You choose easy level ")
     f = open("hard.txt","r")
     game = f.read().split("\n")
else:
     print(" You did not choose a proper level ")
     speak(" You did not choose a proper level ")''' 
    




engine = pyttsx3.init('sapi5')#Initializing the voice given by microsoft
voices = engine.getProperty('voices')#getting voice

engine.setProperty('voice',voices[0].id)#setting the male voice of david for use
engine.setProperty('rate',150)#speed property of voice

#function for text to speech conversion
def speak(audio):
    engine.say(audio)
    engine.runAndWait()

#function taking command as a speech and converting it to text
def takeCommand():
    #it takes audio from microphone and returns a string
    r = sr.Recognizer()
    
    with sr.Microphone() as source:
        print("Listening.............")
        r.pause_threshold = 1
        
        audio = r.listen(source)

        try:
            print("Recognizing..............")
            query = r.recognize_google(audio, language="en-in")
            print(f"you said.......{query}\n")
            
        
        except Exception:
            print("Say again.................")
            return "none"
        
        return query
        

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if(hour>=5 and hour<12):
        speak("Good Morning")
    elif(hour>=12 and hour<16):
        speak("Good Afternoon")
    else:
        speak("Good Evening")

    speak("Hello game player we are team ligers How can i help you!")

#class for calculating the score
class Score(object):
    score = 0
    k = 0
    life = 3
    flag = 0

#for threading timer
def timeUp():
    print("Times Up!.....\nYou can still guess the correct answer but your score will not be increased : ")
    speak("Time's up ! but you can still guess the correct answer but your score will not be calculated")
    Score.flag = 1



class Scene(object):#Scene class
    def enter(self):
        print("Scene yet not configured............")

lev = int(input("enter your choice :"))
if(lev == 1) :
    print(" You choose easy level ")
    speak(" You choose easy level ")
    f = open("easy.txt","r")
    game = f.read().split("\n")
elif(lev == 2):
     print(" You choose medium level ")
     speak(" You choose medium level ")
     f = open("medium.txt","r")
     game = f.read().split("\n")
elif (lev == 3):
     print(" You choose easy level ")
     speak(" You choose easy level ")
     f = open("hard.txt","r")
     game = f.read().split("\n")
else:
     print(" You did not choose a proper level ")
     speak(" You did not choose a proper level ")

class Game(Scene):#inheritng from scene class
    
    def enter(self):
        Score.flag = 0
        l2 = []
        b = game[Score.k]
        Score.k = Score.k+1#next question
        c = list(b)
        d = randint(2,len(b) - 1)
        for i in range(d):
            h = randint(0,len(c) - 1)
            if(h in l2):
                i = i-1
            else:
                l2.append(h)
        #printing incomplete word
        print(f"Your remaining life : {Score.life}")
        speak(f"Your remaining life is {Score.life}")
        speak("Your incomplete word is")
        print("Word : ",end = " ")

        for j in range(len(c)):
            if(j in l2):
                print("__",end = " ")
            else:
                print(c[j],end = " ")
        print("\n")

        #for another thread for the timer
        timer = threading.Timer(8.0,timeUp)
        timer.start()#starting the second thread
        print("Guess the correct word.....")
        
        answe = "none"
        while(answe=="none"):
            answe = takeCommand()
            
        answer = answe.split(" ")
        
        app_id = '0d2e058d' #dictionary api app id
        app_key = '1e3a9ae05fa064c632aec887792d61f0' #app key to authenticate requests
        url= "https://od-api.oxforddictionaries.com/api/v2/lemmas" + "/" +  "en-us" + "/" + answer.lower()
        r = requests.get(url, headers = {'app_id': app_id, 'app_key': app_key})
        
        if(b in answer):
            #if the user does not give answer
            if(Score.flag==1):
                Score.flag = 0
                
                print(f"Time is up but Your answer is correct so we will not make any changes to your current score.\nYour Score is : {Score.score}")
                speak(f"Time is up but Your answer is correct so we will not make any changes to your current score and Your Score is : {Score.score}")

            #if the user gave the answer
            else:
                timer.cancel()#ending the second thread
                Score.score = Score.score + 10
                print(f"Wohoo! You made it.\nYour score is : {Score.score}\n")
                speak(f"Wohoo! You made it and Your score is : {Score.score}")

                
            
                if(Score.k == len(game)):
                    return "over"

                #else:
                 #   level()
        
        #if answer exists in dictionary and time is not up        
        elif("error" not in r.text and Score.flag!=1):
            timer.cancel()#ending the second thread
            Score.score = Score.score + 10
            print(f"Wohoo! You made it.\nYour score is : {Score.score}\n")
            speak(f"Wohoo! You made it and Your score is : {Score.score}")
            
            if(Score.k == len(game)):
                    return "over"
            
            
        else:
            if(Score.flag==1):
                Score.flag = 0
                Score.score = Score.score - 5
                Score.life = Score.life - 1
                print(f"Time is up and your answer is wrong .\nCorrect answer is : {b}\nYour score is : {Score.score}\n")
                speak(f"Time is up and your answer is wrong and Correct answer is : {b} and Your score is : {Score.score}")
            else:
                timer.cancel()
                Score.score = Score.score - 5
                Score.life = Score.life - 1
                print(f"Ahaa!! Wrong answer.\nCorrect answer is : {b}\nYour score is : {Score.score}\n")
                speak(f"Ahaa!! Wrong answer and Correct answer is : {b} and Your score is : {Score.score}")
            
                if(Score.life == 0):
                    return "lifeN"
                elif(Score.k == len(game)):
                    return "over"

        print("Would you like to continue[Yes(y)/No(n)] : ")
        speak("Would you like to continue.")
        prompt = takeCommand().split(" ")
        if("no" in prompt):
            return "end"
        else:
            return "game"

class End(Scene):#inheritng from scene class
    def enter(self):
        print("You wished to discontinue the game.........\n")
        speak("You wished to discontinue the game")
        return "finished"


# adding level function
'''def level():
    if Score.score < -10 :
        f = open("easy.txt","r")
        game = f.read().split("\n")
    elif Score.score > -10 :
        f = open("medium.txt","r")
        game = f.read.split("\n")
    else:
        f = open("game.txt","r")
        game = f.read().split("\n")
    return "lev" '''

class GameOver(Scene):#inheritng from scene class
    def enter(self):
        print("The game is over you made it to the second round.........\n")
        speak("The game is over you made it to the second round")
        return "finished"

class LifeOver(Scene):
    def enter(self):
        print("Your life is over..........\n")
        speak("Your life is over")
        return "finished"

class Finished(Scene):#inheritng from scene class
    def enter(self):
        print("********************Thanks for playing**********************")
        print(f"Your Score is ||{Score.score}||\n")
        speak("Thanks for playing")
        speak(f"Your Score is {Score.score}")

class Map(object):
    mapping = {"game":Game(),
                "end":End(),
                "over":GameOver(),
                "lifeN":LifeOver(),
                "finished":Finished(),
                "lev":level()
                }
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
    wishMe()
    
    while True :
        query = takeCommand()
        
        if (("game" in query) or ("play" in query)):
            print("*********************Welcome to the game of Word Master***************************")
            speak("Welcome to the game of Word Master.")
            print("""The rules of the game are : 
            1.You have only 3 lives.
            2.Each correct answer will give you 10 points.
            3.Each wrong answer will deduct 5 points from your total score
            4.You have 5 seconds to answer a particular question
            
            
            Choose your difficulty level :
            1. Easy 
            2. Medium
            3. Hard  """)
            speak("""The rules of the game are : 
            1 You have only 3 lifes.
            2 Each correct answer will give you 10 points.
            3 Each wrong answer will deduct 5 points from your total score
            4 You have 5 seconds to answer a particular question
            
            
            Choose your difficulty level :
            1. Easy 
            2. Medium
            3. Hard  """)

            time.sleep(1)
            
            a = Map("game")
            gi = Engine(a)
            gi.play()

        elif("exit" or "quit" in query):
            break

#query = takeCommand()
