class CommandBuilder:
    def __init__(self):
        pass

    def build(self, command_text: str):
        try:
            command_chunks = command_text.split(" ")
            return command_chunks
        except Exception as e:
            print(f"build :: error occurred :: {e}")
            return []
