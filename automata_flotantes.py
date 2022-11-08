class automata_flotante:
    int stateN = 0
    int isAccepted(char str[]):
    
        int len = len(str)
        
        for i in len:
            if (stateN == 0):
                start(str[i])
            else:
                if (stateN == 1):
                    state1(str[i])
                else 
                    if (stateN == 2):
                        state2(str[i])
                    else:
                        if (stateN == 3):
                            state3(str[i])
                        else: 
                            if (stateN == 4):
                                state4(str[i])
                            else: 
                                if (stateN == 5):
                                    state5(str[i])	            
                                else
                                    return 0

        if (stateN == 5):
            return 1
        else:
            return 0
    
    def start(char c):
        if (c == '0'):
            stateN = 1
        else: 
            if(c == '-'):
                stateN = 2
            else: 
                if(c == '1' or c == '2' or c == '3' or c == '4' or c == '5' or 
                    c == '6' or c == '7' or c == '8' or c == '9'):
                    stateN = 3
                else:
                    stateN = -1
        
    def state1(char c):
        if (c == '.'):
            stateN = 4
        else:
            stateN = -1
    
    def state2(char c):
        if(c == '0'):
            stateN = 1
        else:
            if(c == '1' or c == '2' or c == '3' or c == '4' or c == '5' or 
                    c == '6' or c == '7' or c == '8' or c == '9'):
                stateN = 3
            else:
                stateN = -1
    
    def state3(char c):
        if(c == '.'):
            stateN = 4
        else:
            if(isdigit(c)):
                stateN = 3
            else: 
                stateN = -1
    
    def state4(char c):
        if(isdigit(c)):
            stateN = 5
        else:
            stateN = -1
    
    def state5(char c):
        if(isdigit(c)):
            stateN = 5
        else:
            stateN = -1
    
    bool verified(char* token):
        if (isAccepted(token)):
            return true
        else:
            return false
