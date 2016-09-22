from enum import Enum
from abc import abstractmethod, ABCMeta


class Element:
    def __init__(self, factory, node):
        self.__tag = node.tag
        short_name = node.find('SHORT-NAME')
        self.__name = short_name.text if short_name is not None else None
        self.__id = node.get('ID')

        for child in node:
            element = factory.create_element(child)
            if element is not None:
                setattr(self, element.attr, element)

    def __str__(self):
        return '%s -> %s' % (self.id, self.name)

    @property
    def name(self):
        return self.__name

    @property
    def id(self):
        return self.__id

    @property
    def attr(self):
        return self.__tag.lower().replace('-', '_')


class DiagDataDictionarySpec(Element):
    pass


class DiagLayerContainer(Element):
    pass


class BaseVariant(Element):
    pass


class Request(Element):
    @property
    def length(self):
        return sum([p.bit_length for p in self.params]) // 8

    @property
    def data(self):
        result = []
        for p in self.params:
            result = result + p.value
        return result

    def __getitem__(self, item):
        return self.data[item]


class Addressing(Enum):
    PHYSICAL = 'PHYSICAL'
    FUNCTIONAL = 'FUNCTIONAL'
    BOTH = 'FUNCTIONAL-OR-PHYSICAL'

    @property
    def name(self):
        return super(Addressing, self).name.capitalize()

    def __add__(self, other):
        if self == Addressing.PHYSICAL and other == Addressing.FUNCTIONAL:
            return Addressing.BOTH

        if self == Addressing.FUNCTIONAL and other == Addressing.PHYSICAL:
            return Addressing.BOTH
        return self


class DiagService(Element):
    def __init__(self, factory, node):
        super(DiagService, self).__init__(factory, node)
        self.__addressing = Addressing(node.get('ADDRESSING', 'PHYSICAL'))

    @property
    def addressing(self):
        return self.__addressing

    @property
    def pre_condition_states(self):
        if hasattr(self, 'pre_condition_state_refs'):
            return [p.ref for p in self.pre_condition_state_refs]
        else:
            return []

    @property
    def state_transitions(self):
        if hasattr(self, 'state_transition_refs'):
            return [p.ref for p in self.state_transition_refs]
        else:
            return []


class State(Element):
    pass


class UnitSpec(Element):
    pass


class Unit(Element):
    pass


class Dop(Element, metaclass=ABCMeta):
    @abstractmethod
    def bit_length(self):
        pass


class Structure(Dop):
    @property
    def bit_length(self):
        return sum([p.dop.bit_length for p in self.params])


class DtcDop(Dop):
    @property
    def bit_length(self):
        return self.diag_coded_type.bit_length


class DataObjectProperty(Dop):
    @property
    def bit_length(self):
        return self.diag_coded_type.bit_length


class CodedConst(Element):
    def __init__(self, factory, node):
        super(CodedConst, self).__init__(factory, node)
        self.__value = int(node.find('CODED-VALUE').text)

    @property
    def value(self):
        return [self.__value]

    @property
    def bit_length(self):
        return self.diag_coded_type.bit_length


class PhysConst(Element):
    def __init__(self, factory, node):
        super(PhysConst, self).__init__(factory, node)
        self.__value = int(node.find('PHYS-CONSTANT-VALUE').text)

    @property
    def value(self):
        return [self.__value]

    @property
    def bit_length(self):
        return self.dop.bit_length


class Value(Element):
    @property
    def bit_length(self):
        return self.dop.bit_length

    @property
    def value(self):
        return [0] * (self.bit_length // 8)


class StateChart(Element):
    pass


class StateTransition(Element):
    def __init__(self, factory, node):
        super(StateTransition, self).__init__(factory, node)
        self.__source = node.find('SOURCE-SNREF').get('SHORT-NAME')
        self.__target = node.find('TARGET-SNREF').get('SHORT-NAME')


class StandardLengthType(Element):
    def __init__(self, factory, node):
        super(StandardLengthType, self).__init__(factory, node)
        self.__bit_length = int(node.find('BIT-LENGTH').text)

    @property
    def bit_length(self):
        return self.__bit_length


class MinMaxLengthType(Element):
    @property
    def bit_length(self):
        return 0
