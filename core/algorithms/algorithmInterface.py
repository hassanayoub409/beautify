#########################################################
#   Written by  :   Hassan Ayoub                        #
#   Date        :   December 5, 2025                    #
#   Purpose     :   Interface for algorithms            #
#########################################################

# Class Algorithm
class Algorithm:
    '''
    This class acts as an interface for algorithms
    '''
    def step(self):
        '''
        Perform one iteration. Return (positions_dict, is_finished)
        '''
        raise NotImplementedError
    
    def reset(self):
        '''
        Reset the parameters, optional
        '''
        pass