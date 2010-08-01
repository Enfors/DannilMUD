# cmd_parser.py

import os

import dm.daemon.update_d as update_d

player_cmds_dir = "cmd/player"
wiz_cmds_dir    = "cmd/wiz"
admin_cmds_dir  = "cmd/admin"

class CmdParser:
    def __init__(self):
        self.player_cmds = [ ]
        self.wiz_cmds    = [ ]
        self.admin_cmds  = [ ]

        self.load_all_cmds()

    
    def parse(self, input):
        cmd_string = input.split(" ")[0]
        print("Cmd: " + cmd_string)
        
        if cmd_string in self.player_cmds:
            cmd = self.player_cmds[cmd_string]
        else:
            return

        if input in cmd.rules:
            print("Matching rule found.")
            eval("cmd.rule_%s()" % input)
        else:
            print("No matching rule.")


    def load_all_cmds(self):
        """Load all commands for players, wizards and admins."""
        self.player_cmds = self._load_cmds(player_cmds_dir)
        self.wiz_cmds    = self._load_cmds(wiz_cmds_dir)
        self.admin_cmds  = self._load_cmds(admin_cmds_dir)


    def _load_cmds(self, dir):
        cmd_dict = { }
        file_names = os.listdir(dir)

        dir = dir.replace("/", ".")

        for file_name in file_names:

            # Skip inheritable base files
            if file_name in [ "player_cmd.py", "wiz_cmd.py",
                              "admin_cmd.py", "__init__.py" ]:
                continue

            # Skip .pyc files
            if file_name[-4:] == ".pyc":
                continue
            
            file_name = file_name[:-3]

            cmd = update_d.update_d.request_obj("%s.%s" % (dir, file_name),
                                                "Cmd")
            print(cmd)
            cmd_dict[file_name] = cmd

        return cmd_dict
                     



if __name__ == "__main__":
    player_cmds_dir = "/home/chenf/work/dm/dm/cmd/player"
    wiz_cmds_dir = "/home/chenf/work/dm/dm/cmd/wiz"
    admin_cmds_dir = "/home/chenf/work/dm/dm/cmd/admin"
    cmd_parser = CmdParser()

    
