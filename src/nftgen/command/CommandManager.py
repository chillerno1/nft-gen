from nftgen.command.Command import Command


class CommandManager:
    def __init__(self):
        self.command_dict = {}

    def register(self, command: Command):
        self.command_dict[command.name] = command
        for alias in command.aliases:
            self.command_dict[alias] = command

    def execute(self, cmd: str, *args):
        command = self.command_dict.get(cmd)
        if command is not None:
            command.execute(*args)
