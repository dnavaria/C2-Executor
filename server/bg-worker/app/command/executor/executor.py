import subprocess


class CommandExecutor:
    def __init__(self):
        # default values for subprocess.run
        self.stdout = subprocess.PIPE
        self.stderr = subprocess.PIPE
        self.shell = False
        self.text = True

    def execute(self, command: list):
        try:
            result = subprocess.run(
                command,
                stdout=self.stdout,
                stderr=self.stderr,
                shell=self.shell,
                text=self.text
            )
            if result.returncode == 0:
                return result.stdout
            return result.stderr
        except Exception as e:
            print(f"execute_command :: error occurred :: {e}")
            return None
