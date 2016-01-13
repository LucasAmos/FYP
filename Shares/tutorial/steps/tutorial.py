from behave import *

@given('2 is less than 4')
def step_impl(context):
    pass

@when('three equals three')
def step_impl(context):
    assert 3 == 3

@then('five is greater than two')
def step_impl(context):
    #assert context.failed is False
    assert 5 > 2