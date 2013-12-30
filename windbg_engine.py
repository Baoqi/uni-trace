from pykd import *

def EnableChildProcessDebug():
    dbgCommand(".childdbg 1")   # enable child debug
    dbgCommand("sxi ibp")  # ignore initial break point
    dbgCommand("sxi epr")  # ignore process exit break point

def make_closure_bp_handler(tp):
    return lambda bpId: tp.Action()

gModuleNameSet = set([])

class UTraceEventHandler(eventHandler):
    def onModuleLoad(self, offset, name):
        if name in gModuleNameSet:
            gUTraceEngine._setup_all_trace_points(set([name]))
            return eventResult.Proceed
        return eventResult.NoChange

class UTraceEngine:
    def __init__(self):
        self.trace_function_enter_points = []
        self.trace_function_line_offset_points = []
        self.bpIds = set([])
        self.eh = UTraceEventHandler()

    def registerTraceFunctionEnter(self, tp):
        self.trace_function_enter_points.append(tp)
        gModuleNameSet.add(tp.module_name)

    def registerTraceFunctionLineOffset(self, tp):
        self.trace_function_line_offset_points.append(tp)
        gModuleNameSet.add(tp.module_name)

    def Action(self):
        if isWindbgExt():
            self._setup_all_trace_points(
                self._get_current_available_modules()
            )
            go()
            #dbgCommand("|0s")
            #for bpId in self.bpIds:
            #    removeBp(bpId)
    def _get_current_available_modules(self):
        available_modules = set([])
        for m in gModuleNameSet:
            try:
                module(m)
                available_modules.add(m)
            except BaseException:
                continue
        return available_modules

    def _setup_all_trace_points(self, module_set):
        self._setup_trace_function_enter_points(module_set)
        self._setup_trace_function_line_offset_points(module_set)

    def _setup_trace_function_enter_points(self, module_set):
        for tp in self.trace_function_enter_points:
            if tp.module_name in module_set:
                tp_module = module(tp.module_name)
                for (name, address) in  tp_module.enumSymbols(tp.function_name):
                    id = setBp(address, make_closure_bp_handler(tp))
                    dprintln(str.format("setting TraceFunctionEnter break point ({0} at: {1}", id, name))
                    self.bpIds.add(id)

    def _setup_trace_function_line_offset_points(self, module_set):
        for tp in self.trace_function_line_offset_points:
            if tp.module_name in module_set:
                tp_module = module(tp.module_name)
                for (name, address) in  tp_module.enumSymbols(tp.function_name):
                    source_file, source_file_line, _ = getSourceLine(address)
                    source_file_line += tp.function_line_offset
                    strBpExpression = str.format("@@masm(`{0}!{1}:{2}+`)", tp.module_name, source_file, source_file_line)
                    id = setBp(expr(strBpExpression), make_closure_bp_handler(tp))
                    dprintln(str.format("setting TraceFunctionLineOffset break point ({0} at: {1}", id, strBpExpression))
                    self.bpIds.add(id)

# global object
gUTraceEngine = UTraceEngine()
