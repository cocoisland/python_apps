from sklearn.model_selection import train_test_split

class TrainValTest:
  '''
  split(X,y) - 
    Return 
      X_train, y_train for training model.
      X_val, y_val for validation test model.
      X_test, y_test for testing model.

    Parameters
    -----------
      X : two dimensions or above of numerical dataframe
      y : Series of numerical or object values.
      train_size = 0.8 : default 80% split for X_train dataset
      val_size   = 0.1 : default 10% split for X_val dataset
      test_size  = 0.1 : default 10% split for X_test dataset
      random_state = None : default None, or True
      
      
    Returns
    -------
      X_train, X_val, X_test, y_train, y_val, y_test
      
    Examples
    --------
      X_train, X_val, X_test, y_train, y_val, y_test = split(X,y)
      
  '''
  def __init__(self, train_size=0.8, val_size=0.1, test_size=0.1, 
                 random_state=None, shuffle=True):
    self.train_size=train_size,
    self.val_size=val_size,
    self.test_size=test_size,
    self.random_state=random_state,
    self.shuffle=shuffle
    
  def split(self,X,y):  
    assert self.train_size + self.val_size + self.test_size == 1
    X_train_val, X_test, y_train_val, y_test = train_test_split(
          X, y, test_size=self.test_size, random_state=self.random_state, 
          shuffle=self.shuffle)

    X_train, X_val, y_train, y_val = train_test_split(
          X_train_val, y_train_val, 
          test_size=self.val_size/(self.train_size+self.val_size), 
          random_state=self.random_state, shuffle=self.shuffle)

    return X_train, X_val, X_test, y_train, y_val, y_test
