from odx import ElementFactory
from xml.etree.ElementTree import Element
import pytest

VARIANT_ID = '_177'
VARIANT_NAME = 'MyVariant'


def XmlElement(tag, id=None, name=None, text=None, sub_elements=[], attrib={}):
    if id is not None:
        attrib['ID'] = id
    element = Element(tag, attrib)
    for sub_element in sub_elements:
        element.append(sub_element)
    if text is not None:
        element.text = text
    if name is not None:
        e = Element('SHORT-NAME')
        e.text = name
        element.append(e)
    return element


request1 = XmlElement('REQUEST', id=1)
request2 = XmlElement('REQUEST', id=2)
requests = XmlElement('REQUESTS', sub_elements=[request1, request2])

source_snref = XmlElement('SOURCE-SNREF', attrib={'SHORT-NAME': 'Default'})
target_snref = XmlElement('TARGET-SNREF', attrib={'SHORT-NAME': 'Default'})
state_transition = XmlElement('STATE-TRANSITION', id='_220',
                              name='Default_Default',
                              sub_elements=[source_snref, target_snref])
state_transitions = XmlElement('STATE-TRANSITIONS',
                               sub_elements=[state_transition])
default_state = XmlElement('STATE', id='_147', name='Default')
states = XmlElement('STATES', sub_elements=[default_state])
state_char = XmlElement('STATE-CHART', id='_146', name='Session',
                        sub_elements=[state_transitions, states])
state_charts = XmlElement('STATE-CHARTS', sub_elements=[state_char])
long_name = XmlElement('LONG-NAME', text='LongName')
base_variant = XmlElement('BASE-VARIANT', name=VARIANT_NAME, id=VARIANT_ID,
                          sub_elements=[requests, state_charts, long_name])
base_variants = XmlElement('BASE-VARIANTS', sub_elements=[base_variant])
diag_layer_container = XmlElement('DIAG-LAYER-CONTAINER', id='_139',
                                  sub_elements=[base_variants])
root = XmlElement('ODX', sub_elements=[diag_layer_container])


@pytest.fixture
def factory():
    return ElementFactory(root)


@pytest.fixture
def base_variant():
    return factory().root.base_variants.get(id=VARIANT_ID)


def test_get_root(factory):
    assert factory.root.id == '_139'


def test_base_variant_get_by_id(factory):
    assert factory.root.base_variants.get(id=VARIANT_ID).id is VARIANT_ID


def test_base_variant_get_by_name(factory):
    assert factory.root.base_variants.get(name=VARIANT_NAME).id is VARIANT_ID


def test_base_variant_name(base_variant):
    assert base_variant.name is VARIANT_NAME


def test_base_variant_attribute(base_variant):
    assert base_variant.attr == 'base_variant'


def test_base_variant_str(base_variant):
    assert str(base_variant) == '%s -> %s' % (VARIANT_ID, VARIANT_NAME)


def test_requests_length(base_variant):
    assert len(base_variant.requests) == 2


def test_requests_str(base_variant):
    assert str(base_variant.requests) == 'REQUESTS'


def test_requests_index(base_variant):
    assert base_variant.requests[1].id == 2


def test_requests_iter(base_variant):
    assert list(base_variant.requests) == [base_variant.requests[0],
                                           base_variant.requests[1]]


def test_requests_filter(base_variant):
    assert list(base_variant.requests.filter(lambda x: x.id == 2))[0].id == 2


def test_snref(base_variant):
    source = base_variant.state_charts[0].state_transitions[0].source
    assert str(source) == '_147 -> Default'
