from macropy.core.macros import *
from macropy.core.quotes import macros, q
from macropy.core.hquotes import macros, u, hq, unhygienic
from windbg_engine import *
macros = Macros()

##
## This is the macro to trace function begin
##
@macros.block
def TraceFunctionEnter(tree, gen_sym, **kw):
    result_statements = []

    ##  get from arguments
    module_name = ""
    function_name = ""
    trace_name = ""
    if kw.has_key("args"):
        temp_args = kw["args"]
        if temp_args:
            # TODO, check whether those args are string type
            if len(temp_args) > 2:
                trace_name = temp_args[2].s
            else:
                trace_name = gen_sym("trace_temp_0")
            if len(temp_args) > 1:
                module_name = temp_args[0].s
                function_name = temp_args[1].s


    with q as inner_defined_statements:
        class FakeName:
            def __init__(self):
                self.trace_name = u[trace_name]
                self.module_name = u[module_name]
                self.function_name = u[function_name]
            def Action(self):
                pass

        gUTraceEngine.registerTraceFunctionEnter(FakeName())

    trace_class_name = "TraceFunctionEnterClass_" + trace_name
    # rename class name
    inner_defined_statements[0].name = trace_class_name
    # rename the object creation call's class name
    inner_defined_statements[1].value.args[0].func.id = trace_class_name

    # add all tree.body into the class object init function
    action_func = inner_defined_statements[0].body[1]
    action_func.body = tree

    result_statements += inner_defined_statements
    return result_statements

##
## This is the macro to trace function + line_offset
##
@macros.block
def TraceFunctionLineOffset(tree, gen_sym, **kw):
    result_statements = []

    ##  get from arguments
    module_name = ""
    function_name = ""
    function_line_offset = 0
    trace_name = ""
    if kw.has_key("args"):
        temp_args = kw["args"]
        if temp_args:
            # TODO, check whether those args are string type, and offset is number
            if len(temp_args) > 3:
                trace_name = temp_args[3].s
            else:
                trace_name = gen_sym("trace_temp_0")
            if len(temp_args) > 2:
                module_name = temp_args[0].s
                function_name = temp_args[1].s
                function_line_offset = temp_args[2].n


    with q as inner_defined_statements:
        class FakeName:
            def __init__(self):
                self.trace_name = u[trace_name]
                self.module_name = u[module_name]
                self.function_name = u[function_name]
                self.function_line_offset = u[function_line_offset]
            def Action(self):
                pass

        gUTraceEngine.registerTraceFunctionLineOffset(FakeName())

    trace_class_name = "TraceFunctionLineOffsetClass_" + trace_name
    # rename class name
    inner_defined_statements[0].name = trace_class_name
    # rename the object creation call's class name
    inner_defined_statements[1].value.args[0].func.id = trace_class_name

    # add all tree.body into the class object init function
    action_func = inner_defined_statements[0].body[1]
    action_func.body = tree

    result_statements += inner_defined_statements
    return result_statements