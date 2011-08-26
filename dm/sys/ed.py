#!/usr/bin/env python
# ed.py by Dannil

import re
import dm.sys.edit as edit

MODE_COMMAND = 2

class Ed(edit.Edit):
    """The full line-based editor."""
    
    def __init__(self,
                 output_func : "The function output is sent to.",
                 end_func    : "Called when the editor exits."
                 ):
        edit.Edit.__init__(self, output_func, end_func)
        self._edit_lines = [ ]


    def start(self):
        self.output_func("ed.py [new file]\n")
        self._enter_command_mode()
        

    def _enter_command_mode(self):
        self.mode = MODE_COMMAND
        self._show_command_prompt()


    def _enter_edit_mode(self):
        self.mode        = edit.MODE_EDIT
        self._edit_lines = [ ]


    def _set_cur_line_num(self, cur_line_num):
        num_lines = len(self.lines) - 1

        if cur_line_num < 1:
            cur_line_num = 1
        elif cur_line_num > num_lines:
            cur_line_num = num_lines

        self._cur_line_num = cur_line_num


    def _show_command_prompt(self):
        self.output_func("{0}:".format(self._cur_line_num))


    def _command_quit(self):
        self.output_func("[Leaving ed]")
        self.end_func()


    def user_input(self, text : "The text the user entered."):
        """This function is called when the user has entered input."""
        if self.mode == edit.MODE_EDIT:
            self._edit_input(text)
        else:
            self._command_input(text)


    def _edit_input(self, text : "The text the user entered."):
        """This function is called by user_input() when input has
        arrived and we're in edit mode."""
        
        if text == ".":
            edit_end_func = self._command.query_edit_end_func()
            edit_end_func()
            self._enter_command_mode()
            return

        self._edit_lines.append(text)


    def _command_input(self, text : "The text the user entered."):
        """This function is called by user_input() when input has
        arrived and we're in command mode."""
        self._parse_command_input(text.strip())

        if self.mode == MODE_COMMAND:
            self._show_command_prompt()


    def _parse_command_input(self, text):
        start, end, text = self._parse_address(text)
        cmd,        text = self._parse_cmd(text)
        args,       text = self._parse_args(text)

        self._command = Command(start, end, cmd, args)

        print("{0},{1}: {2} {3}".format(start, end, cmd, args))

        if cmd == "a":
            self._command_append(start, end)
        elif cmd == "p":
            self._command_print(start, end)
        elif cmd == "q":
            self._command_quit()

        self._cur_line_num = self._command.query_start()


    def _command_append(self, start, end):
        start = self._command.query_start()
        end   = self._command.query_end()

        if end:
            self.output_func("[Can't use range with append.]\n")
            return
        
        self._command.set_edit_end_func(self._command_append_end)
        self._enter_edit_mode()


    def _command_print(self, start, end):
        for num, line in enumerate(self.lines[start:end + 1]):
            self.output_func("{0:4d}: {1}\n".format(start + num, line))


    def _command_append_end(self):
        num_lines_added = len(self._edit_lines)

        self.append_lines(self._command.query_start(),
                          self._edit_lines)

        self.output_func("[Lines added: {0}.]\n".format(num_lines_added))
        self._set_cur_line_num(self._cur_line_num + num_lines_added)


    def _command_quit(self):
        self.output_func("[Leaving ed.]\n")
        self.end_func()


    def _parse_address(self, text):
        # Match number comma number, like "2,5":
        match = re.search(r"^(\d+)?,?(\d+)?", text)

        start = end = None

        if match.group(1):
            start = int(match.group(1))

        if match.group(2):
            end   = int(match.group(2))

        text  = text[len(match.group(0)):]

        if not start:
            start = self._cur_line_num

        return start, end, text

    
    def _parse_cmd(self, text):
        text = text.lstrip()
        
        if not text:
            return "p", ""
        else:
            return text[:1], text[1:]


    def _parse_args(self, text):
        return None, ""



class Command:
    def __init__(self, start, end, command, args):
        self._start         = start
        self._end           = end
        self._command       = command
        self._args          = args
        self._edit_end_func = None


    def set_edit_end_func(self, func):
        self._edit_end_func = func


    def query_start(self):
        return self._start
    

    def query_end(self):
        return self._end


    def query_command(self):
        return self._command


    def query_args(self):
        return self._args


    def query_edit_end_func(self):
        return self._edit_end_func



def output_func(line):
    print(line, end = "")


def end_func():
    raise SystemExit


if __name__ == "__main__":
    ed = Ed(output_func, end_func)
    ed.start()

    while True:
        line = input()
        ed.user_input(line)
