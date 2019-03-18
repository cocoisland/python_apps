import random

class Product:
  '''
    Return 

    Parameters
    -----------

    Returns
    -------
      
    Examples
    --------
      
  '''

  def __init__(self,name) :
    self.name=name
    self.price=10
    self.weight=20
    self.flammability=0.5
    self.identifier=random.randint(1000000, 9999999)

  def stealability(self):  
    stealable = self.price / self.weight
    if (stealable) < 0.5:
       return "Not so stealable..."
    elif (stealable >= 0.5 and stealable < 1.0):
       return "Kinda stealable."
    else:
       return "Very stealable!"

  def explode(self):  
    flammable = self.flammability * self.weight
    if (flammable) < 10:
       return "...fizzle."
    elif (flammable >= 10 and flammable < 50):
       return "...boom!"
    else:
       return "...BABOOM!!"

class BoxingGlove(Product):
   def __init__(self, name):
      super().__init__(name)
      self.weight=10
      

   def explode(self):
      return "...it's a glove."

   def punch(self):
      if (self.weight < 5):
         return "That tickles."
      elif (self.weight >= 5 and self.weight < 15):
         return "Hey that hurt!"
      else:   
         return "OUCH!."

