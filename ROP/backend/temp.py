__all__ = ['temp']

# Don't look below, you will not understand this Python code :) I don't.

from js2py.pyjs import *
# setting scope
var = Scope( JS_BUILTINS )
set_global_object(var)

# Code follows:
var.registers(['func6', 'var5', 'var4', 'var2', 'func5', 'var1', 'func7', 'userTotal', 'start', 'total', 'didWin', 'executeCall', 'callGlobal', 'var7', 'func1', 'var6', 'func3', 'func4', 'execute', 'var3', 'func2', 'getRandomInt', 'logging_string'])
@Js
def PyJsHoisted_start_(this, arguments, var=var):
    var = Scope({'this':this, 'arguments':arguments}, var)
    var.registers([])
    var.put('var1', var.get('getRandomInt')(Js(10000000000.0)))
    var.put('var2', var.get('getRandomInt')(Js(10000000000.0)))
    var.put('var3', var.get('getRandomInt')(Js(10000000000.0)))
    var.put('var4', var.get('getRandomInt')(Js(10000000000.0)))
    var.put('var5', var.get('getRandomInt')(Js(10000000000.0)))
    var.put('var6', var.get('getRandomInt')(Js(10000000000.0)))
    var.put('var7', var.get('getRandomInt')(Js(10000000000.0)))
    var.put('userTotal', Js(0.0))
    var.put('total', ((((((var.get('var1')+var.get('var2'))+var.get('var3'))+var.get('var4'))+var.get('var5'))+var.get('var6'))+var.get('var7')))
    var.put('logging_string', Js(''))
PyJsHoisted_start_.func_name = 'start'
var.put('start', PyJsHoisted_start_)
@Js
def PyJsHoisted_executeCall_(array_input, this, arguments, var=var):
    var = Scope({'array_input':array_input, 'this':this, 'arguments':arguments}, var)
    var.registers(['array_input', 'execute_result', 'logging'])
    var.get('start')()
    var.put('execute_result', var.get('execute')(var.get('array_input')))
    var.put('logging', var.get('document').callprop('getElementById', Js('logging')))
    var.get('logging').put('innerHTML', var.get('logging_string'))
    if PyJsStrictEq(var.get('execute_result'),Js(True)):
        var.get('logging').put('innerHTML', (var.get('logging').get('innerHTML')+Js('<br><br><b>Success!</b> :)')))
    return var.get('execute_result')
PyJsHoisted_executeCall_.func_name = 'executeCall'
var.put('executeCall', PyJsHoisted_executeCall_)
@Js
def PyJsHoisted_getRandomInt_(max, this, arguments, var=var):
    var = Scope({'max':max, 'this':this, 'arguments':arguments}, var)
    var.registers(['max'])
    return var.get('Math').callprop('floor', (var.get('Math').callprop('random')*var.get('max')))
PyJsHoisted_getRandomInt_.func_name = 'getRandomInt'
var.put('getRandomInt', PyJsHoisted_getRandomInt_)
@Js
def PyJsHoisted_func1_(this, arguments, var=var):
    var = Scope({'this':this, 'arguments':arguments}, var)
    var.registers([])
    var.put('userTotal', var.get('var1'), '+')
    var.get('console').callprop('log', Js('Adding func1: '), var.get('var1'))
    var.put('logging_string', (Js('<br/>Adding func1: ')+var.get('var1')), '+')
PyJsHoisted_func1_.func_name = 'func1'
var.put('func1', PyJsHoisted_func1_)
@Js
def PyJsHoisted_func2_(this, arguments, var=var):
    var = Scope({'this':this, 'arguments':arguments}, var)
    var.registers([])
    var.put('userTotal', var.get('var2'), '+')
    var.get('console').callprop('log', Js('Adding func2: '), var.get('var2'))
    var.put('logging_string', (Js('<br/>Adding func2: ')+var.get('var2')), '+')
PyJsHoisted_func2_.func_name = 'func2'
var.put('func2', PyJsHoisted_func2_)
@Js
def PyJsHoisted_func3_(param1, this, arguments, var=var):
    var = Scope({'param1':param1, 'this':this, 'arguments':arguments}, var)
    var.registers(['param1'])
    var.put('logging_string', (Js('<br/>Param1: ')+var.get('param1')), '+')
    if PyJsStrictEq(var.get('param1'),Js('ROP')):
        var.put('userTotal', var.get('var3'), '+')
        var.get('console').callprop('log', Js('Adding func3: '), var.get('var3'))
        var.put('logging_string', (Js('<br/>Adding func3: ')+var.get('var3')), '+')
    else:
        var.get('console').callprop('log', Js('Missed func3 :('))
        var.put('logging_string', Js('<br/>Missed func3 :('), '+')
PyJsHoisted_func3_.func_name = 'func3'
var.put('func3', PyJsHoisted_func3_)
@Js
def PyJsHoisted_func4_(this, arguments, var=var):
    var = Scope({'this':this, 'arguments':arguments}, var)
    var.registers([])
    var.put('userTotal', var.get('var4'), '+')
    var.get('console').callprop('log', Js('Adding func4: '), var.get('var4'))
    var.put('logging_string', (Js('<br/>Adding func4: ')+var.get('var4')), '+')
PyJsHoisted_func4_.func_name = 'func4'
var.put('func4', PyJsHoisted_func4_)
@Js
def PyJsHoisted_func5_(param1, param2, this, arguments, var=var):
    var = Scope({'param1':param1, 'param2':param2, 'this':this, 'arguments':arguments}, var)
    var.registers(['param1', 'param2'])
    var.put('logging_string', (Js('<br/>Param1: ')+var.get('param1')), '+')
    var.put('logging_string', (Js('<br/>Param2: ')+var.get('param2')), '+')
    if (PyJsStrictEq(var.get('param1'),Js('1337')) and PyJsStrictEq(var.get('param2'),Js('0x8000000'))):
        var.put('userTotal', var.get('var5'), '+')
        var.put('logging_string', (Js('<br/>Adding func5: ')+var.get('var5')), '+')
        var.get('console').callprop('log', Js('Adding func5: '), var.get('var5'))
    else:
        var.get('console').callprop('log', Js('Missed func5 :('))
        var.put('logging_string', Js('<br/>Missed func5 :('), '+')
PyJsHoisted_func5_.func_name = 'func5'
var.put('func5', PyJsHoisted_func5_)
@Js
def PyJsHoisted_func6_(this, arguments, var=var):
    var = Scope({'this':this, 'arguments':arguments}, var)
    var.registers([])
    var.put('userTotal', var.get('var6'), '+')
    var.get('console').callprop('log', Js('Adding func6: '), var.get('var6'))
    var.put('logging_string', (Js('<br/>Adding func6: ')+var.get('var6')), '+')
PyJsHoisted_func6_.func_name = 'func6'
var.put('func6', PyJsHoisted_func6_)
@Js
def PyJsHoisted_func7_(this, arguments, var=var):
    var = Scope({'this':this, 'arguments':arguments}, var)
    var.registers([])
    var.put('userTotal', var.get('var7'), '+')
    var.get('console').callprop('log', Js('Adding func7: '), var.get('var7'))
    var.put('logging_string', (Js('<br/>Adding func7: ')+var.get('var7')), '+')
PyJsHoisted_func7_.func_name = 'func7'
var.put('func7', PyJsHoisted_func7_)
@Js
def PyJsHoisted_didWin_(this, arguments, var=var):
    var = Scope({'this':this, 'arguments':arguments}, var)
    var.registers([])
    if PyJsStrictEq(var.get('total'),var.get('userTotal')):
        return Js(True)
    return Js(False)
PyJsHoisted_didWin_.func_name = 'didWin'
var.put('didWin', PyJsHoisted_didWin_)
@Js
def PyJsHoisted_execute_(arr, this, arguments, var=var):
    var = Scope({'arr':arr, 'this':this, 'arguments':arguments}, var)
    var.registers(['arr', 'storage', 'elt', 'index'])
    var.put('storage', Js([]))
    #for JS loop
    var.put('index', Js(0.0))
    while (var.get('index')<var.get('arr').get('length')):
        var.put('elt', var.get('arr').get(var.get('index')))
        if (var.get('elt').callprop('startsWith', Js('func')) and (var.get('elt').get('length')==Js(5.0))):
            if PyJsStrictEq(var.get('storage').get('length'),Js(0.0)):
                var.get('eval')((var.get('elt')+Js('()')))
            else:
                if PyJsStrictEq(var.get('storage').get('length'),Js(1.0)):
                    (var.get('eval')(((var.get('elt')+Js('("'))+var.get('storage').get('0')))+Js('")'))
                else:
                    if PyJsStrictEq(var.get('storage').get('length'),Js(2.0)):
                        (((var.get('eval')(((var.get('elt')+Js('("'))+var.get('storage').get('1')))+Js('","'))+var.get('storage').get('0'))+Js('")'))
                        var.get('func')(var.get('storage').get('1'), var.get('storage').get('0'))
            var.put('storage', Js([]))
        else:
            var.get('storage').callprop('push', var.get('elt'))
        # update
        (var.put('index',Js(var.get('index').to_number())+Js(1))-Js(1))
    return var.get('didWin')()
PyJsHoisted_execute_.func_name = 'execute'
var.put('execute', PyJsHoisted_execute_)
@Js
def PyJsHoisted_callGlobal_(this, arguments, var=var):
    var = Scope({'this':this, 'arguments':arguments}, var)
    var.registers([])
    return var.get('global')
PyJsHoisted_callGlobal_.func_name = 'callGlobal'
var.put('callGlobal', PyJsHoisted_callGlobal_)
var.put('userTotal', Js(0.0))
var.put('total', Js(0.0))
pass
pass
pass
pass
pass
pass
pass
pass
pass
pass
pass
pass
pass
pass
pass
pass
pass
pass
pass
pass
pass
pass


# Add lib to the module scope
temp = var.to_python()