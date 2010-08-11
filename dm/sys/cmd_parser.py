# cmd_parser.py

import os

import dm.daemon.update_d as update_d
import dm.sys.error       as error

player_cmds_dir = "cmd/player"
wiz_cmds_dir    = "cmd/wiz"
admin_cmds_dir  = "cmd/admin"

valid_dirs = {
    "north",
    "south",
    "east",
    "west",
    "up",
    "down"
    }

class ParseError(error.Error):
    pass


class ParseWrongRule(error.Error):
    pass


class IncorrectInput(error.Error):
    pass


class CmdParser:
    def __init__(self):
        self.player_cmds = [ ]
        self.wiz_cmds    = [ ]
        self.admin_cmds  = [ ]

        self.load_all_cmd_lists()


    def parse(self, orig_input, body):
        match_found      = False
        orig_input       = orig_input.split()
        cmd_name         = orig_input[0]
        fail_explanation = "then it went downhill from there."

        cmd_path = self.find_cmd_path(cmd_name, body)
        
        try:
            if not cmd_path:
                raise ParseError("I have no idea what \"%s\" means.\n" %
                                 cmd_name)

            cmd = update_d.update_d.request_obj(cmd_path, "Cmd")

            if len(cmd.rules) == 0:
                # todo: raise exception
                print("[cmd_parser] The %s command has no rules." % cmd_name)

            for orig_rule in cmd.rules:
                input = orig_input[:]
                rule  = orig_rule[:]
                #print("\nChecking rule %s..." % rule)
                try:
                    args = self.match_input_to_rule(input, rule, body)

                    #if match:
                    #print("This rule matches. All done.")
                    func_name = "cmd.rule_%s(body, args)" % \
                        "_".join(orig_rule)
                    try:
                        return eval(func_name)
                    except error.CmdFailed as e:
                        body.recv_tag_text(str(e))
                #else:
                    #print("This rule does not match.")
                    #pass
                except ParseWrongRule:
                    continue
                except IncorrectInput as e:
                    fail_explanation = str(e)

            raise ParseError("I understood \"%s\", but %s" %
                             (cmd_name, fail_explanation))
        except ParseError as e:
            body.recv_tag_text(str(e))
            return False, None


    def match_input_to_rule(self, input, rule, body):
        args = [ ]

        while len(rule):
            #print("+-Checking token %s..." % rule[0])
            if not rule[0].isupper():
                input, rule, args = self.match_plain_word(input, rule, 
                                                          args)
            
            elif rule[0] == "STR":
                input, rule, args = self.match_STR(input, rule, args)

            elif rule[0] == "LIV":
                input, rule, args = self.match_LIV(input, rule, args, body)

            elif rule[0] == "OBJ":  # Objects in room AND inv
                input, rule, args = self.match_OBJ(input, rule, args, body,
                                                   check_room = True,
                                                   check_inv  = True)

            elif rule[0] == "ROBJ": # Objects in room only
                input, rule, args = self.match_OBJ(input, rule, args, body,
                                                   check_room = True)

            elif rule[0] == "IOBJ": # Objects in inv only
                input, rule, args = self.match_OBJ(input, rule, args, body,
                                                   check_inv  = True)

            elif rule[0] == "DIR":
                input, rule, args = self.match_DIR(input, rule, args)

            elif rule[0] == "PATH":
                input, rule, args = self.match_PATH(input, rule, args)

            elif rule[0] == "WORD":
                input, rule, args = self.match_WORD(input, rule, args)

            #print("+-Done with this token. Remaining input: %s" % input)

        if len(input):
            raise IncorrectInput("I didn't understand the last part.\n")
        else:
            return args


    def match_plain_word(self, input, rule, args):
        #print("+---Matching plain word '%s'..." % rule[0])
        #word = rule.pop()
        rule_word, rule = self._pop_first(rule)

        if len(input) == 0:
            raise IncorrectInput("I was expecting a \"%s\" somewhere "
                                 "in there.\n" % word)

        #input.pop(0)
        entered_word, input = self._pop_first(input)
        
        if entered_word != rule_word:
            raise IncorrectInput("I was expecting a \"%s\" somewhere "
                                 "in there.\n" % rule_word)            

        return input, rule, args


    def match_STR(self, input, rule, args):
        #print("+---Matching string '%s'..." % " ".join(input))
        #rule.pop()
        tmp, rule = self._pop_first(rule)

        if len(input) == 0:
            raise IncorrectInput("I was expecting more.\n")

        args.append(" ".join(input))
        input = [ ]
    
        return input, rule, args


    def match_LIV(self, input, rule, args, body):
        raise ParseError("LIV parsing rules not implemented.")


    def match_OBJ(self, input, rule, args, body, liv_only = False,
                  check_inv = False, check_room = False):
        found_objs = [ ]
        adjectives = [ ]
        
        tmp, rule = self._pop_first(rule)

        if len(input) == 0:
            raise IncorrectInput("I was execting an object too.\n")

        id, input = self._pop_first(input)

        if check_room:
            found_objs += self.find_room_objs(body, id, liv_only)
        if check_inv:
            found_objs += self.find_objs(body, id, liv_only)

        if len(found_objs) == 0:
            raise IncorrectInput("I do not see any \"%ss\" here.\n" % id)

        print("Found %d objects." % len(found_objs))

        args += [ found_objs[0] ]

        return input, rule, args


    def match_DIR(self, input, rule, args):
        #print("+---Matching DIR...")
        if len(input) == 0:
            raise IncorrectInput("I was expecting a direction too.\n")

        dir, input = self._pop_first(input)
        tmp, rule  = self._pop_first(rule)

        if dir in valid_dirs:
            args.append(dir)
            return input, rule, args
        else:
            raise IncorrectInput("\"%s\" is not a proper direction.\n" % 
                                 dir.lower())


    def match_PATH(self, input, rule, args):
        #print("+---Matching PATH...")

        if len(input) == 0:
            raise IncorrectInput("I was expecting a path too.\n")

        path, input = self._pop_first(input)
        tmp,  rule  = self._pop_first(rule)

        args.append(path)

        return input, rule, args


    def match_WORD(self, input, rule, args):
        #print("+---Matching WORD...")

        if len(input) == 0:
            raise IncorrectInput("I was expecting an additional word.\n")

        word, input = self._pop_first(input)
        tmp,  rule  = self._pop_first(rule)

        args.append(word)

        return input, rule, args


    def find_objs(self, container, id, adjectives = [ ], liv_only = False):
        """Returns a list of objects in the container that match the
        specified criteria."""
        
        found_objs = [ ]

        for obj in container.query_contents():
            print("Checking %s..." % obj.query("short"))

            if id in obj.query("ids"):
                found_objs.append(obj)

        return found_objs

    
    def find_room_objs(self, body, id, adjectives = [ ], liv_only = False):
        room = body.query_env()

        if not room:
            return [ ]
        else:
            return self.find_objs(room, id, adjectives, liv_only)


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
                     

    def _pop_first(self, entries):
        if len(entries) == 0:
            return None, [ ]
        elif len(entries) == 1:
            return entries[0], [ ]
        else:
            return entries[0], entries[1:]
    


if __name__ == "__main__":
    player_cmds_dir = "/home/chenf/work/dm/dm/cmd/player"
    wiz_cmds_dir = "/home/chenf/work/dm/dm/cmd/wiz"
    admin_cmds_dir = "/home/chenf/work/dm/dm/cmd/admin"
    cmd_parser = CmdParser()

    
