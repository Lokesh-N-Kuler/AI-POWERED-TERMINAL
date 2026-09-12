import { useEffect, useRef, useState } from "react";
import { Terminal as XTerminal } from "@xterm/xterm";
import { FitAddon } from "@xterm/addon-fit";

import "@xterm/xterm/css/xterm.css";

import { executeCommand } from "../../services/terminalService";

function Terminal() {
  const terminalRef = useRef(null);
  const xtermRef = useRef(null);
  const fitAddonRef = useRef(null);

  const [shell, setShell] = useState("powershell");
  const [currentDirectory, setCurrentDirectory] = useState(null);

  useEffect(() => {
    const terminal = new XTerminal({
      cursorBlink: true,
      fontSize: 15,
      fontFamily: "Consolas, monospace",
      scrollback: 5000,
    });

    const fitAddon = new FitAddon();

    terminal.loadAddon(fitAddon);

    terminal.open(terminalRef.current);

    fitAddon.fit();

    xtermRef.current = terminal;
    fitAddonRef.current = fitAddon;

    terminal.write("AI-Powered Terminal\r\n");
    terminal.write("Type a command and press Enter.\r\n\r\n");

    terminal.write("PS> ");

    let command = "";

    const handleData = async (data) => {
      if (data === "\r") {
        terminal.write("\r\n");

        const enteredCommand = command.trim();

        if (!enteredCommand) {
          terminal.write("PS> ");
          return;
        }

        try {
          const result = await executeCommand(
            enteredCommand,
            shell,
            currentDirectory
          );

          if (result.stdout) {
            terminal.write(result.stdout.replace(/\n/g, "\r\n"));
          }

          if (result.stderr) {
            terminal.write(`\r\n${result.stderr.replace(/\n/g, "\r\n")}`);
          }

          if (result.cwd) {
            setCurrentDirectory(result.cwd);
          }

          terminal.write("\r\n");

          terminal.write(
            result.exit_code === 0
              ? "PS> "
              : `[Exit Code: ${result.exit_code}]\r\nPS> `
          );
        } catch (error) {
          terminal.write(
            `\r\nBackend connection error: ${error.message}\r\nPS> `
          );
        }

        command = "";
        return;
      }

      if (data === "\u007F") {
        if (command.length > 0) {
          command = command.slice(0, -1);
          terminal.write("\b \b");
        }

        return;
      }

      if (data === "\u0003") {
        command = "";
        terminal.write("^C\r\nPS> ");
        return;
      }

      if (data >= " " && data <= "~") {
        command += data;
        terminal.write(data);
      }
    };

    terminal.onData(handleData);

    const handleResize = () => {
      fitAddon.fit();
    };

    window.addEventListener("resize", handleResize);

    return () => {
      window.removeEventListener("resize", handleResize);
      terminal.dispose();
    };
  }, [shell]);

  return (
    <div className="terminal-wrapper">
      <div className="terminal-header">
        <div>
          <strong>Terminal</strong>
        </div>

        <select
          value={shell}
          onChange={(e) => {
            setShell(e.target.value);
            setCurrentDirectory(null);
          }}
        >
          <option value="powershell">PowerShell</option>
          <option value="cmd">CMD</option>
          <option value="bash">Bash</option>
        </select>
      </div>

      <div
        ref={terminalRef}
        className="terminal-container"
      />
    </div>
  );
}

export default Terminal;