'''
Created on 28 sept. 2012

@author: Florentin
'''
class IO:
    
    def __init__(self,path) :
        self.path = path 
          

    def init_reader(self):
        """
        Initialize the reader. You must do it before to use any method to read in the file
        """
        self.file = open(self.path,"r")
    
    def read_line(self):
        """
        You can use too "for line in IO.file : ..." after having called init_reader
        """
        return self.file.readline()
    
    
    def close(self):
        self.file.close()
        
# working if test.txt exist.
if __name__ == "__main__":
    Io = IO("test.txt")
    Io.init_reader()
    print(Io.read_line())
    Io.close()
    
