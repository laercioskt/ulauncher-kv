from actions import ActionFactory, DefatulAction, GetAction, SetAction, UnsetAction

def test_create_action_default_when_type_no_arguments():
    arguments = []
    
    action = ActionFactory(arguments).create()

    assert isinstance(action, DefatulAction), "Should be DefatulAction"

def test_create_action_get_when_type_text_without_get():
    arguments = ['aKey']
    
    action = ActionFactory(arguments).create()

    assert isinstance(action, GetAction), "Should be GetAction"
    assert action.text == "aKey", "Should be key"

def test_create_action_get_when_type_text_with_get():
    arguments = ['get', 'key']
    
    action = ActionFactory(arguments).create()

    assert isinstance(action, GetAction), "Should be GetAction"
    assert action.text == "key", "Should be key"

def test_create_action_get_unset():
    arguments = ['get', 'aKey', 'unset']
    
    action = ActionFactory(arguments).create()

    assert isinstance(action, UnsetAction), "Should be UnsetAction"
    assert action.key == "aKey", "Should be aKey"

def test_create_action_set_without_space_in_value():
    arguments = ['set', 'aKey', 'aValue']
    
    action = ActionFactory(arguments).create()

    assert isinstance(action, SetAction), "Should be SetAction"
    assert action.key == "aKey", "Should be aKey"
    assert action.value == "aValue", "Should be aValue"

def test_create_action_set_with_space_in_value():
    arguments = ['set', 'aKey', 'a', 'Value']
    
    action = ActionFactory(arguments).create()

    assert isinstance(action, SetAction), "Should be SetAction"
    assert action.key == "aKey", "Should be aKey"
    assert action.value == "a Value", "Should be a Value"
