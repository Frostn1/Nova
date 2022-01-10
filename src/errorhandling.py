class Error:
    def __init__(self, errorSection = "", errorType = "", errorMessage = "", pos = (1,1), missValue = "") -> None:
        self.type = errorType
        self.message = errorMessage
        self.pos = pos
        self.value = missValue
        self.section = errorSection
    def printError(self):
        # TODO : Custom print error message with color
        pass
    def __str__(self) -> str:
        return "["+str(self.pos[0])+":"+str(self.pos[1])+"] { " + self.type +" } - "+self.message+" <> "+self.value+"\n"
    def __repr__(self) -> str:
        return "["+str(self.pos[0])+":"+str(self.pos[1])+"] { " + self.type +" } - "+self.message+" <> "+self.value+"\n"

class ErrorHandler:
    def __init__(self) -> None:
        self.errorList = []

    def write(self, outfile = "errors.txt"):
        print('Hello error')
        with open(outfile, 'w') as filep:
            if not filep.writable():
                print("output file not writeable")
                exit(1)
            for error in self.errorList:
                print(error)
                filep.write(str(error))
    def add(self, error : Error):
        self.errorList.append(error)