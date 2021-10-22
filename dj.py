#This will hold everything related to dad jokes#this is a test for dad jokes
import random

def isDadJoke(msg):
  message = readMessage(msg)
  if message != "no im":
    return(formatDadJoke(message))
  else:
    return "null"


#formats the dad joke
def formatDadJoke(jokeContent):
  dadJokeNames = ["Konner", "DAD"]
  randNumb = random.randint(0,len(dadJokeNames)-1)
  dadName = dadJokeNames[randNumb]  
  joke = "Hi {0}, I'm {1}".format(jokeContent, dadName)
  print(joke)
  return joke

#parses the msg for variations of "im"
def readMessage(msg):
  dadJokeStarters = ['im','Im',"i'm","I'm","I am","i am"]
  formattedString = msg.split()
  counter = 0;
  joke = "no im"
  #loop to detects im's and then pushs the string to the content formatting function
  for s in formattedString:
    counter+=1
    for i in dadJokeStarters:
      if (s == i):
        print("im found")
        jokeContent = " ".join(formattedString[counter:])    
        return jokeContent
  return joke
    
