#!/usr/bin/env python
# ed.py by Dannil

MODE_EDIT = 1

class Ed:
    def __init__(self,
                 output_func : "The function output is sent to.",
                 end_func    : "Called when the editor exits."
                 ):
        # The first line, line 0, is always empty and never shown.
        # That's because it's just a placeholder, so that the actual
        # first line will have index 1 to match being line number
        # 1. Otherwise, line number one would have index 0 and there
        # would be conversions all over the place.

        self.output_func  = output_func
        self.end_func     = end_func
        self.lines        = [ "" ]
        self.cur_line_num = 0
        self.mode         = MODE_EDIT


    def start(self):
        self.enter_append_mode()
        self.output_func("""Enter text. End with "." when you're done.
======================================================================
""")


    def enter_append_mode(self):
        self.cur_line_num += 1
        

    def user_input(self, text : "The text the user entered."):
        if text == ".":
            self.end_func(self.lines[1:])
            return

        if text == '"."':
            self.output_func("You're not supposed to include the double "
                             "quotes, but I'll let that slide for now.\n")
            self.end_func(self.lines[1:])


        self.lines.append(text)
        self.cur_line_num += 1
        

def output_func(line):
    print(line, end = "")


def end_func(lines):
    for line in lines:
        print(line)

    raise SystemExit


if __name__ == "__main__":
    ed = Ed(output_func, end_func)
    ed.start()

    while True:
        line = input()
        ed.user_input(line)
