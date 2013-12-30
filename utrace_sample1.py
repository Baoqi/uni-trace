from utrace_macros import macros, TraceFunctionEnter, TraceFunctionLineOffset
from pykd import *
from windbg_engine import *

EnableChildProcessDebug()

with TraceFunctionEnter('M8DbCon3', 'MDb::PhysicalConnectionFactory::Create*', 'Test1'):
    dprintln(dbgCommand("k 5"))
    dprintln(dbgCommand("dv /i /v"))
    dprintln("Trace Function Begin for MDb::PhysicalConnectionFactory::Create*")

with TraceFunctionLineOffset('M8DbCon3', 'MDb::PhysicalConnectionFactory::Create*', 341, 'Test2'):
    dprintln("Enter Line Offset Trace")
    dprintln("Enter Line Offset Trace 2")
    dprintln(dbgCommand("k 1"))
    dprintln(dbgCommand("dv /i /v"))
    dprintln(dbgCommand("dt /b /r lRunnerPtr"))

# child process 1 debug
with TraceFunctionEnter('M8DbOd35', 'MDb::Odbc35::OdbcConnection::Connect', 'Test3'):
    dprintln(str.format("Enter M8DbOd35 Trace at Process ({0}), Thread ({1})", getCurrentProcessId(), getCurrentThreadId()))
    dprintln(dbgCommand("k 10"))
    dprintln(dbgCommand("dv /i /v"))


with TraceFunctionEnter('M8DbJdbc2', 'CreateConnection', 'Test JDBC child process 1'):
    dprintln(str.format("Enter M8DbJdbc2 Trace at Process ({0}), Thread ({1})", getCurrentProcessId(), getCurrentThreadId()))
    dprintln(dbgCommand("k 3"))
    dprintln(dbgCommand("dv /i /v"))

