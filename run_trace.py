import macropy.activate     # sets up macro import hooks
from pykd import isWindbgExt
if not isWindbgExt():
    from macropy.core.exporters import SaveExporter
    macropy.exporter = SaveExporter("macropy_exported", ".")
import utrace_sample1
from windbg_engine import gUTraceEngine

gUTraceEngine.Action()