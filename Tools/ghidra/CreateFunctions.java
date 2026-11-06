// Ghidra headless post-script: creates a function at every address listed in Notes\inventory.csv
// (first column "va", e.g. 0x401000) that Ghidra did not find itself - mostly virtual methods that
// are reachable only through vtables. Usage: -postScript CreateFunctions.java <inventory.csv>
// @category ZooTycoon
import ghidra.app.script.GhidraScript;
import ghidra.app.cmd.function.CreateFunctionCmd;
import ghidra.app.cmd.disassemble.DisassembleCommand;
import ghidra.program.model.address.Address;
import ghidra.program.model.address.AddressSet;
import java.io.BufferedReader;
import java.io.FileReader;
import ghidra.program.model.listing.Function;

public class CreateFunctions extends GhidraScript {
    @Override
    public void run() throws Exception {
        String[] args = getScriptArgs();
        int made = 0, had = 0, failed = 0;
        try (BufferedReader r = new BufferedReader(new FileReader(args[0]))) {
            String line = r.readLine();                         // header
            while ((line = r.readLine()) != null && !monitor.isCancelled()) {
                String va = line.split(",", 2)[0].trim();
                if (!va.startsWith("0x")) continue;
                Address a = toAddr(Long.parseLong(va.substring(2), 16));
                if (getFunctionAt(a) != null) { had++; continue; }
                if (getInstructionAt(a) == null) {
                    DisassembleCommand d = new DisassembleCommand(a, null, true);
                    d.applyTo(currentProgram, monitor);
                }
                Function f = getFunctionContaining(a);
                if (f != null && !f.getEntryPoint().equals(a)) {
                    // inside a function Ghidra built wrongly: let the new entry win
                }
                CreateFunctionCmd c = new CreateFunctionCmd(a);
                if (c.applyTo(currentProgram, monitor)) made++; else failed++;
            }
        }
        println("CreateFunctions: " + made + " created, " + had + " already existed, " + failed + " failed");
    }
}
