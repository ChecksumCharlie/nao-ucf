'''
Created on Apr 4, 2014

@author: Sarah
'''

#from threading import Thread

class Behavior ( object ):

    def __init__ ( self, target, name, args ):
        None#Thread.__init__(self, None, target, name, args, {}, None)
                
    def Run ( self, robot ):
        if ( robot.isInitialized () == False ):
            print ( "Robot was not initialized" )
            return
            
    def Stop_All_Action ( self, robot ):
        return