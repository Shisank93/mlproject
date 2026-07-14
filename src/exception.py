import sys   ## help to interact with python interpretar
from src.logger import logging
def error_message_detail(error, error_detail: sys):
    _,_,exc_tb= error_detail.exc_info() #gives information about the exception that just occurred.  returns (type, value, traceback)
    file_name = exc_tb.tb_frame.f_code.co_filename
    error_message = "Error occurred in python script name [{0}]\nline number [{1}]\nerror message [{2}]".format(file_name, exc_tb.tb_lineno, str(error))
    return error_message

class customException(Exception):
    def __init__(self, error, error_detail: sys):   #error = e error_detail = sys
        super().__init__(error) #calls the parent class (Exception) constructor.
        self.error_message = error_message_detail(error, error_detail=error_detail)
    
    def __str__(self):
        return self.error_message