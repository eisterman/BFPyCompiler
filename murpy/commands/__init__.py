from abc import ABC


class BufferManager:
    buffers = {0: []}
    buffer = 0
    indentindex = []

    def AddPseudoCode(self, pcode):
        self.buffers[self.buffer].append(pcode)

    def IndentBuffer(self):
        self.buffer += 1
        self.buffers[self.buffer] = []

    def DeIndentBuffer(self):
        if self.buffer == 0:
            raise Exception("You can't deindent more.")
        self.buffer -= 1
        tmp = self.buffers[self.buffer + 1]
        del self.buffers[self.buffer + 1]
        return tmp

    def GetMainBuffer(self):
        """
        Will return the shared buffer of all the self subclasses.
        :return: The self Buffer
        """
        tmp = self.buffers[0]
        self.buffers[0] = []
        return tmp

    def RefBuffer(self):
        return self.buffers[self.buffer]

    def TrackIfIndex(self, index):
        self.indentindex.append(index)

    def GetIfIndex(self):
        return self.indentindex[-1]

    def PopIfIndex(self):
        return self.indentindex.pop()


class InterfaceObj(ABC):
    """
    Abstract Base Class for the Interface Object. This contain the
    buffer list used by all the subclasses for the stocking of the
    operations producted by there. This buffer list is a trick for
    the compilation, use with caution.
    """
    BUFFER = BufferManager()


class NestedInterfaceObj(ABC):
    """
    Abstract Base Class for the Nested Interface Object. This is
    different from classic Interface Object. This contain the
    method and the attribute definition for the NestedInterface
    infrastructure for the Operations.
    """
    def __init__(self):
        """Initialization of protected Operation Object attribute for subclasses."""
        self._OPERATION = None

    def getOp(self):
        """Get the Operation Object generated by the command."""
        return self._OPERATION
