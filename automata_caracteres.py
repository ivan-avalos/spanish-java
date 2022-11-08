class automata_caracter:
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
                        if (stateN == 2):
                            state2(str[i]) 
                        else:
                            if (stateN == 3):
                                state3(str[i])
                            else:
                                return 0

            if (stateN == 3):
                return 1
            else:
                return 0
			
			def start(char c):
			    if (c == '\''):
			        stateN = 1
			    else:
			        stateN = -1

			def state1(char c):
			    if (c != '\''):
                    stateN = 2
			    else:
			    	stateN = 3
			
			def state2(char c):
			    if (c == '\''):
			        stateN = 3
			    else:
                    stateN = -1
			
			def state3(char c):
			    stateN = -1
			
			bool verified(char* token):
			    if (isAccepted(token)):
			        return true
			    else:
			        return false
