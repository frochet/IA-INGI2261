'''
Created on 28 sept. 2012

@author: Debroux Léonard, Rochet Florentin
'''
class IO:
    
    def __init__(self,path) :
        self.path = path 
          

    def init_reader(self):
        """
        Initialize the reader. You must do it before to use any method to read in the file
        """
        try :
            self.file = open(self.path,"r")
        except IOError:
            print("An error occured when opening the file in read mode")
    
    def init_writter(self):
        try :
            self.file = open(self.path,"w")
        except IOError :
            print("An error occured when opening the file in write mode")
    
    def read_line(self):
        """
        You can use too "for line in IO.file : ..." after having called init_reader
        """
        return self.file.readline()
    
    def write_line(self, line):
        try:
            self.file.write(line)
        except IOError :
            print("An error occured when writting in the file")
    
    def close(self):
        self.file.close()
        
# working if test.txt exist.
if __name__ == "__main__":
    Io = IO("test.txt")
    Io.init_reader()
    print(Io.read_line())
    Io.close()
    
