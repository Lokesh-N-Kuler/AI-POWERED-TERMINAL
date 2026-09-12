import subprocess
import os
import platform


class TerminalSession:
    def __init__(self):
        self.cwd = os.getcwd()

    def execute(self, command: str, shell_type: str = "powershell"):

        if not command.strip():
            return {
                "command": command,
                "stdout": "",
                "stderr": "Command cannot be empty.",
                "exit_code": 1,
                "cwd": self.cwd,
                "shell": shell_type,
            }

        system = platform.system()

        try:
            # Windows
            if system == "Windows":

                if shell_type.lower() == "powershell":

                    args = [
                        "powershell.exe",
                        "-NoProfile",
                        "-Command",
                        command,
                    ]

                elif shell_type.lower() == "cmd":

                    args = [
                        "cmd.exe",
                        "/C",
                        command,
                    ]

                else:
                    return {
                        "command": command,
                        "stdout": "",
                        "stderr": f"Unsupported shell: {shell_type}",
                        "exit_code": 1,
                        "cwd": self.cwd,
                        "shell": shell_type,
                    }

            # Linux / macOS
            else:

                if shell_type.lower() == "bash":

                    args = [
                        "bash",
                        "-c",
                        command,
                    ]

                else:
                    return {
                        "command": command,
                        "stdout": "",
                        "stderr": f"Unsupported shell: {shell_type}",
                        "exit_code": 1,
                        "cwd": self.cwd,
                        "shell": shell_type,
                    }

            result = subprocess.run(
                args,
                cwd=self.cwd,
                capture_output=True,
                text=True,
                timeout=30,
            )

            # Detect directory changes
            if result.returncode == 0:

                self._update_directory(command, shell_type)

            return {
                "command": command,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "exit_code": result.returncode,
                "cwd": self.cwd,
                "shell": shell_type,
            }

        except subprocess.TimeoutExpired:

            return {
                "command": command,
                "stdout": "",
                "stderr": "Command execution timed out after 30 seconds.",
                "exit_code": 124,
                "cwd": self.cwd,
                "shell": shell_type,
            }

        except Exception as e:

            return {
                "command": command,
                "stdout": "",
                "stderr": str(e),
                "exit_code": 1,
                "cwd": self.cwd,
                "shell": shell_type,
            }

    def _update_directory(self, command: str, shell_type: str):

        command = command.strip()

        # PowerShell / CMD
        if shell_type.lower() in ["powershell", "cmd"]:

            lower_command = command.lower()

            if lower_command.startswith("cd "):

                path = command[3:].strip()

                # Remove quotes
                path = path.strip('"').strip("'")

                try:

                    new_path = os.path.abspath(
                        os.path.join(self.cwd, path)
                    )

                    if os.path.isdir(new_path):

                        self.cwd = new_path

                except Exception:
                    pass

            elif lower_command == "cd":

                if shell_type.lower() == "powershell":
                    self.cwd = os.path.expanduser("~")

        # Bash
        elif shell_type.lower() == "bash":

            if command.startswith("cd "):

                path = command[3:].strip()

                path = path.strip('"').strip("'")

                try:

                    new_path = os.path.abspath(
                        os.path.join(self.cwd, path)
                    )

                    if os.path.isdir(new_path):

                        self.cwd = new_path

                except Exception:
                    pass


session = TerminalSession()


def execute_command(
    command: str,
    shell_type: str = "powershell",
    cwd: str | None = None,
):

    if cwd:
        session.cwd = cwd

    return session.execute(
        command,
        shell_type,
    )