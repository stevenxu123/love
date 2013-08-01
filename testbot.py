import socket
import sys
import random
import pickle
import gamestate
import deck

class TestBot(object):

    def __init__(self):
        return

ipaddress = "192.168.1.5"
def main():
    if len(sys.argv) > 1:
        botId = "testbot" + str(sys.argv[1])
    tb = TestBot()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ipaddress, 8002))
    s.send(botId)

#    message = gamestate.GameState()
#    message.deck = deck.Deck()
#
#    pickled = pickle.dumps(message)
#    unpickled = pickle.loads(pickled)
#    s.send(pickled)
#
#    print message.deck.__dict__
#    print pickled
#    print unpickled.deck.__dict__

#    data = s.recv(1024)
#    print data
#
#    data2 = s.recv(1024)
#    gameState = pickle.loads(data2)
#    print gameState

    data3 = s.recv(1024)
    gameState = pickle.loads(data3)
    print gameState.__dict__

if __name__ == "__main__":
    main()
