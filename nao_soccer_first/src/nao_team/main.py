'''
Created on Nov 9, 2013

@author: Astrid
'''
import sys;
# from multiprocessing import Process

import nao_player;

def processPlayer(robotIp, robotPort):
    player = nao_player.NaoPlayer(robotIp, robotPort);
    player.enter();
    
    while True:
        player.update();
        
        

if __name__ == '__main__':
    robotIp = "127.0.0.1"
 
    if len(sys.argv) <= 1:
        print "Usage python robotIP (optional default: 127.0.0.1)"
    else:
        robotIp = sys.argv[1]
#  
    #setup team here
#     p1 = Process(target=processPlayer, args=(robotIp, 9559));
#     p2 = Process(target=processPlayer, args=(robotIp, 9561));
#     p1.start();
#     p2.start();
    player = nao_player.NaoPlayer(robotIp, 9561);
    player.enter();
    
    while True:
        player.update();