from twisted.protocols.telnet import *
from twisted.application import service, internet
from twisted.internet import protocol, defer

class TelnetProtocol(Telnet):
    def connectionMade(self):
        print "TelnetProtocol.connectionMade"
        Telnet.connectionMade(self)

    def telnet_Password(self, passwd):
        """I accept a password as an argument."""
        self.write(IAC+WONT+ECHO+"*****\r\n")

    def dataReceived(self, data):
        print "TelnetProtocol.dataReceived"
        print data
        Telnet.dataReceived(self, data)
        return "Command"

class TelnetFactory(protocol.ServerFactory):
    protocol = TelnetProtocol

    def __init__(self, **kwargs):
        self.users = kwargs

    def getUser(self, user):
        print "TelnetFactory.getUser"
        print user
        return defer.succeed(self.users.get(user, "No such user"))

application = service.Application("serial", uid=1000, gid=100)

factory = TelnetFactory()
internet.TCPServer(1021, factory).setServiceParent(
    service.IServiceCollection(application))
