import pytest


def test_equal_or_not_equal():
    assert 1 == 1
    assert 2 != 3
    assert 4 == 4
    assert 5 != 6
    assert 7 == 7
    assert 8 != 9
    assert 10 == 10
    
def test_boolean():
    validated = True
    assert validated is True
    assert ("Hello" == "Hell") is False
    
def test_type():
    assert type(1) == int
    assert type(1.0) == float
    assert type("Hello") == str
    assert type([1, 2, 3]) == list
    
class Student:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age
        
# Para reusar el objeto Student en las pruebas
# y no tener que crear uno nuevo cada vez
@pytest.fixture
def default_employee():
    return Student("John", 20)
        
def test_person_initialization(default_employee):
    assert default_employee.name == "John"
    assert default_employee.age == 20