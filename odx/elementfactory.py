from xml.etree import ElementTree as ET
from collections import defaultdict

from odx.element import BaseVariant, CodedConst, PhysConst, \
    DataObjectProperty, DiagDataDictionarySpec, DiagLayerContainer, \
    DiagService, DtcDop, MinMaxLengthType, Request, StandardLengthType, \
    State, StateChart, Unit, UnitSpec, StateTransition, Element, Structure, \
    Value, Dop


class Container:
    def __init__(self, manager, e):
        self.__manager = manager
        self.__name = e.tag
        self.__data = []
        self.__by_id = {}
        self.__by_name = {}
        for i in e:
            element = manager.create_element(i)
            self.__data.append(element)
            if isinstance(element, Element):
                self.__by_id[element.id] = element
                self.__by_name[element.name] = element

    def __str__(self):
        return self.__name

    def __iter__(self):
        for i in self.__data:
            yield i

    def __getitem__(self, item):
        return self.__data[item]

    def get(self, id=None, name=None):
        if id is not None:
            return self.__by_id[id]
        else:
            return self.__by_name[name]

    def filter(self, function):
        return filter(function, self)

    @property
    def attr(self):
        return self.__name.lower().replace('-', '_')


class Reference:
    def __init__(self, manager, e, id_name, leng):
        self.__name = e.tag
        self.__ref_id = e.get(id_name)
        self.__manager = manager
        self.__len = leng

    @property
    def ref(self):
        return self.__manager.ref(self.__name, self.__ref_id)

    def __str__(self):
        return self.ref.__str__()

    def __getattr__(self, item):
        return getattr(self.ref, item)

    def __getitem__(self, item):
        return self.ref.__getitem__(item)

    @property
    def attr(self):
        return self.__name[:-self.__len].lower()


class IdReference(Reference):
    def __init__(self, manager, e):
        super(IdReference, self).__init__(manager, e, 'ID-REF', 4)


class SnReference(Reference):
    def __init__(self, manager, e):
        super(SnReference, self).__init__(manager, e, 'SHORT-NAME', 6)


class ElementFactory:
    CONTAINERS = [
        'BASE-VARIANTS',
        'DATA-OBJECT-PROPS',
        'DIAG-COMMS',
        'DTC-DOPS',
        'PARAMS',
        'PRE-CONDITION-STATE-REFS',
        'REQUESTS',
        'STATE-CHARTS',
        'STATE-TRANSITIONS',
        'STATE-TRANSITION-REFS',
        'STATES',
        'STRUCTURES',
        'UNITS',
    ]

    ELEMENTS = {
        'BASE-VARIANT': BaseVariant,
        'CODED-CONST': CodedConst,
        'PHYS-CONST': PhysConst,
        'DATA-OBJECT-PROP': DataObjectProperty,
        'DIAG-DATA-DICTIONARY-SPEC': DiagDataDictionarySpec,
        'DIAG-LAYER-CONTAINER': DiagLayerContainer,
        'DIAG-SERVICE': DiagService,
        'DTC-DOP': DtcDop,
        'MIN-MAX-LENGTH-TYPE': MinMaxLengthType,
        'REQUEST': Request,
        'STANDARD-LENGTH-TYPE': StandardLengthType,
        'STATE': State,
        'STATE-CHART': StateChart,
        'STATE-TRANSITION': StateTransition,
        'STRUCTURE': Structure,
        'UNIT': Unit,
        'UNIT-SPEC': UnitSpec,
        'VALUE': Value,
    }

    REFERENCE_TYPES = {
        'DOP-REF': Dop,
        'REQUEST-REF': Request,
        'STATE-TRANSITION-REF': StateTransition,
        'PRE-CONDITION-STATE-REF': State,
        'SOURCE-SNREF': State,
        'TARGET-SNREF': State,
        'START-STATE-SNREF': State,
        'UNIT-REF': Unit,
    }

    def __init__(self, root):
        self.__refs = defaultdict(dict)
        self.__root = self.create_element(root[0])

    @property
    def root(self):
        return self.__root

    def create_element(self, e):
        if e.tag in self.CONTAINERS:
            return Container(self, e)

        element_type = e.get('{http://www.w3.org/2001/XMLSchema-instance}type',
                             default=e.tag)
        if element_type in self.ELEMENTS:
            cls = self.ELEMENTS[element_type]
            assert not isinstance(cls, Element)
            element = cls(self, e)

            for ref_cls in self.REFERENCE_TYPES.values():
                if isinstance(element, ref_cls):
                    self.__refs[ref_cls][element.id] = element
                    self.__refs[ref_cls][element.name] = element
            return element

        if e.tag.endswith('-REF'):
            return IdReference(self, e)
        if e.tag.endswith('-SNREF'):
            return SnReference(self, e)

    def ref(self, ref_name, ref_id):
        ref_cls = self.REFERENCE_TYPES[ref_name]
        try:
            return self.__refs[ref_cls][ref_id]
        except KeyError:
            raise KeyError('%s -> %s' % (ref_name, ref_id))


def parse(filename, variant_id):
    tree = ET.parse(filename)
    factory = ElementFactory(tree.getroot())
    base_variant = factory.root.base_variants.get(id=variant_id)
    return base_variant
