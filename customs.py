queueList = []
class customGame:
  def __init__(self):
    self.queueList = []

  def newCustom(self):
    print("starting new custom instance")
    self.queueList.clear()

  def add(self, player):
    for i in self.queueList:
      print("{0} player id\n{1} queueList id".format(player.get_id(), i.get_id()))
      if player.get_id() == i.get_id():
        return True
    
    self.queueList.append(player)
    
  def remove(self, id):
    for i in self.queueList:
      if i.get_id() == id:
        self.queueList.remove(i)
        return True
    return False
    
    

  def length(self):
    return len(self.queueList)
    
  def list(self):
    print("printing queue list")
    return self.queueList

  def retrieve(self,num):
    return self.queueList[0:num]
  
  def getNext(self):
    if self.length() > 0:
      user = self.queueList[0]
      self.queueList.pop(0)
      return user
    else:
      return False



      
customCmds = "```Custom Commands:\n\nnewCustoms: Starts a new customs instance and resets queue | admin use only (.newCustoms)\n\queue | will add you to the running queue (.queue)\n\queue_other | @ the person you want to add after the command (.queue_other @Bamoh0001)\n\ndelSelf | deletes you from the queue (.delSelf)\n\ndelOther | @ the person you want deleted | admin use only(.delOther @Bamoh#0001)\n```"


