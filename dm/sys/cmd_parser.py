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

        self.load_all_cmd_lists()


    def parse(self, input, user):
        words = input.split(" ")
        cmd_name = words[0]

        cmd_path = self.find_cmd_path(cmd_name, user)
        
        if not cmd_path:
            user.recv_text("What?\n")
            return False

        cmd = update_d.update_d.request_obj(cmd_path, "Cmd")

        if len(words) > 1:
            rule = "%s STR" % cmd_name
            if rule in cmd.rules:
                str = " ".join(words[1:]).replace("'", "\\'")
                eval("cmd.rule_%s(user, '%s')" % (rule.replace(" ", "_"),
                                                  str))
                return

        if input in cmd.rules:
            eval("cmd.rule_%s(user)" % input)
            return
        else:
            user.recv_text("What?\n")


    def find_cmd_path(self, cmd_name, user):
        cmd_lists = [ self.player_cmds ]

        if user.query("is_wiz"):
            cmd_lists.append(self.wiz_cmds)

        if user.query("is_admin"):
            cmd_lists.append(self.admin_cmds)

        for cmd_list in cmd_lists:
            if cmd_name in cmd_list:
                cmd_path = cmd_list[cmd_name] + "." + cmd_name
                return cmd_path 

        return None


    def load_all_cmd_lists(self):
        """Load all commands for players, wizards and admins."""
        self.player_cmds = self._load_cmd_list(player_cmds_dir)
        self.wiz_cmds    = self._load_cmd_list(wiz_cmds_dir)
        self.admin_cmds  = self._load_cmd_list(admin_cmds_dir)


    def _load_cmd_list(self, dir):
        cmd_list = { }
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

            cmd_list[file_name] = dir

        return cmd_list
                     



if __name__ == "__main__":
    player_cmds_dir = "/home/chenf/work/dm/dm/cmd/player"
    wiz_cmds_dir = "/home/chenf/work/dm/dm/cmd/wiz"
    admin_cmds_dir = "/home/chenf/work/dm/dm/cmd/admin"
    cmd_parser = CmdParser()

    
