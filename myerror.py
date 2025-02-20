import configparser
import inspect

import sys

config = None

class MyError():

  def __init__(self, et):
    self.config = configparser.RawConfigParser()
    self.config.read('ErrorMessages.properties')
    self.errorType = et

  def newError(self, flag, key, line=None, column=None, **data):
    message = ''
    if(key):
      if(flag):
        message = key
      
      else:
        message = self.config.get(self.errorType, key)
    if(data):
      if(not flag):
        for key, value in data.items():
          message = f"Error[{line}][{column}]: " + message + ", " f"{key}: {value}"

    return(message.strip())

