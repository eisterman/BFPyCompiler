from abc import ABC
from _operations import NewStaticOp, ChangeStaticValueOp, RegToStackOp, CopyStackToRegOp, NestedOp
from _mathoperations import AdditionOp, SubtractionOp, MultiplicationOp
from _controlflowoperations import IFConditionOp


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


BUFFER = BufferManager()  # TODO: Find a better way to manage the BUFFER


class InterfaceObj(ABC):
    """
    Abstract Base Class for the Interface Object. This contain the
    buffer list used by all the subclasses for the stocking of the
    operations producted by there. This buffer list is a trick for
    the compilation, use with caution.
    """
    # C'è da overloaddare __init__ per creare InterfaceObj
    pass


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


class VAR(InterfaceObj):
    """
    This command will create a new variable in the stack.
    This command can take as value a NestedInterfaceObj SubClass.
    """
    def __init__(self, name, value=0):  # TODO: Typecoding
        """
        This command will create a new variable in the stack.
        :param name: Name of the new variable
        :param value: Value assigned at the variable
        """
        # PER ORA SOLO VALORI NUMERICI PURI
        if isinstance(value, NestedInterfaceObj):
            oplist = [NewStaticOp(name, 0), value.getOp(), RegToStackOp(name)]
            op = NestedOp(oplist)
        else:
            op = NewStaticOp(name, value)
        BUFFER.AddPseudoCode(op)


class SET(InterfaceObj):
    """
    This command will edit the value into a already existing variable
    in the stack.
    This command can take as value a NestedInterfaceObj SubClass.
    """
    def __init__(self, name, value=0):
        """
        This command will edit the value into a already existing variable
        in the stack.
        This command can take as value a NestedInterfaceObj SubClass.
        :param name: Name of the variable to be changed.
        :param value: Value or NestedInterfaceObj to be inserted in the variable.
        """
        if isinstance(value, NestedInterfaceObj):
            oplist = [value.getOp(), RegToStackOp(name)]
            op = NestedOp(oplist)
        else:
            op = ChangeStaticValueOp(name, value)
        BUFFER.AddPseudoCode(op)


class ADD(InterfaceObj, NestedInterfaceObj):
    """
    This command will sum two variable using a Registry as output.
    This command is a NestedInterfaceObj.
    """
    def __init__(self, name1, name2):
        """
        This command will sum two variable using a Registry as output.
        This command is a NestedInterfaceObj.
        :param name1: First member
        :param name2: Second member
        """
        super().__init__()
        self._OPERATION = AdditionOp(name1, name2)


class SUB(InterfaceObj, NestedInterfaceObj):
    """
    This command will subtract two variable using a Registry as output.
    The algorithm is classical progressive subtraction.
    This command is a NestedInterfaceObj.
    """
    def __init__(self, name1, name2):
        """
        This command will sum two variable using a Registry as output.
        This command is a NestedInterfaceObj.
        :param name1: First member
        :param name2: Second member
        """
        super().__init__()
        self._OPERATION = SubtractionOp(name1, name2)


class MUL(InterfaceObj, NestedInterfaceObj):
    """
    This command will multiply two variable using a Registry as output.
    The algorithm use heavily the registry for the operations.
    This command is a NestedInterfaceObj.
    """
    def __init__(self, name1, name2):
        """
        This command will multiply two variable using a Registry as output.
        The algorithm use heavily the registry for the operations.
        This command is a NestedInterfaceObj.
        :param name1: First member
        :param name2: Second member
        """
        super().__init__()
        self._OPERATION = MultiplicationOp(name1, name2)


class IF(InterfaceObj):
    def __init__(self, condition):
        preludeops = []
        if isinstance(condition, str):
            preludeops.append(CopyStackToRegOp(condition))
        elif isinstance(condition, NestedInterfaceObj):
            preludeops.append(condition.getOp())
        else:
            raise Exception("IF can take only variable or NestedInterfaceObj")
        preludeops.append(IFConditionOp())
        BUFFER.TrackIfIndex(len(BUFFER.RefBuffer()))
        BUFFER.AddPseudoCode(NestedOp(preludeops))
        BUFFER.IndentBuffer()


class ELSE(InterfaceObj):
    def __init__(self):
        outif = BUFFER.DeIndentBuffer()
        refbuffer = BUFFER.RefBuffer()
        refbuffer[BUFFER.GetIfIndex()].RefLastOp().SetOpList(outif)
        BUFFER.IndentBuffer()


class ENDIF(InterfaceObj):
    def __init__(self):
        outif = BUFFER.DeIndentBuffer()
        refbuffer = BUFFER.RefBuffer()
        refbuffer[BUFFER.PopIfIndex()].RefLastOp().SetOpList(outif)
