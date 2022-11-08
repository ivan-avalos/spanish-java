class automata_identificadores:
    int stateN = 0
    int isAccepted(char str[]):
    
    int len = len(str)
            
            for i in len:
                if (stateN == 0):
                    start(str[i])
                else: 
                    if (stateN == 1):
                        state1(str[i])
                    else:
                        return 0
    
            if (stateN == 1):
                return 1
            else:
                return 0
        
        def start(char c):
            if (isalpha(c) or c == '_'):
                stateN = 1
            else:
                stateN = -1
            
        def state1(char c):
            if (isalpha(c) or c == '_' or isdigit(c)):
                stateN = 1
            else:
                stateN = -1
        
        bool no_es_main(char* token):
            if (isAccepted(token))
                return true
            else:
                return false
