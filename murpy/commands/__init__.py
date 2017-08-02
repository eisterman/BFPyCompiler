from abc import ABC


class BufferManager:
    """
    Object who manage the Operation Buffer common to all the InterfaceObj.
    With this object the class InterfaceObj manage the parsing of every operation.
    The object is used also as manager of the indentation in the parsing.
    """
    buffers = {0: []}  # BufferGrade: Buffer
    buffergrade = 0  # Actual/Active BufferGrade
    indentindex = []  # Indexes used for intendation management

    def AddPseudoCode(self, pcode):
        """
        Add a Pseudocode Operation at the actual active buffer.
        :param pcode: Pseudocode Operation
        :return: None
        """
        self.buffers[self.buffergrade].append(pcode)

    def IndentBuffer(self):
        """
        Increment the BufferGrade and initialize a new empty buffer.
        :return: None
        """
        self.buffergrade += 1
        self.buffers[self.buffergrade] = []

    def DeIndentBuffer(self):
        """
        Decrement the BufferGrade and pop out the buffer active before.
        :return: Buffer list
        """
        if self.buffergrade == 0:
            raise Exception("You can't deindent more.")
        self.buffergrade -= 1
        tmp = self.buffers[self.buffergrade + 1]
        del self.buffers[self.buffergrade + 1]
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
        """
        Get a reference to the actual buffer activated.
        :return: Buffer list (reference)
        """
        return self.buffers[self.buffergrade]

    def TrackIfIndex(self, index):
        """
        Track a code indentation index for successive utilization.
        :param index: Index to store
        """
        self.indentindex.append(index)

    def GetIfIndex(self):
        """
        Get the last code indentation index tracked as reference.
        :return: reference to the last code indentation index
        """
        return self.indentindex[-1]

    def PopIfIndex(self):
        """
        Pop (get and remove) the last code indentation index tracked.
        :return: last code indentation index
        """
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
