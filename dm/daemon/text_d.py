# text_d.py by Dannil

import dm.daemon.base_daemon as base_daemon

import dm.daemon.update_d    as update_d

NEWLINE="\n"

class TextD(base_daemon.Daemon):
    
    def wrap(self, text, width = 78, indent1 = 0, indent2 = 0):
        """Wrap text to the specified width.

The first line is indented with indent1 number of spaces, and
the consequtive lines are indented with indent2 number of spaces.
A wrapped copy of the text is returned. The original text is not
affected."""
        
        new_text = ""

        current_line = ""
        current_line += " " * indent1

        text = text.replace("\n", " ")
        
        words = text.split(" ")

        for word in words:
            if len(word) == 0:
                continue

            if len(current_line) + len(word) <= width:
                if len(current_line):
                    current_line += " " + word
                else:
                    current_line = word
            else:
                new_text += current_line + NEWLINE
                current_line = " " * indent2 + word

        if len(current_line):
            new_text += current_line

        return new_text

    def split_with_tags(self, text):
        word = ""
        words = [ ]

        i = 0

        for i in range(0, len(text)):
            if text[i] == " ":
                if len(word):
                    words.append(word)
                    word = ""
                continue
                
            if text[i] == "<":
                if len(word):
                    words.append(word)
                word = "<"
                continue

            if text[i] == ">":
                word += ">"
                words.append(word)
                word = ""
                continue

            word += text[i]

        if len(word):
            words.append(word)

        return words
            

    def convert_tag_text(self, text, body = None, prefs = None, width = 0,
                         indent1 = 0, indent2 = 0, leading_nl = False):
        if leading_nl:
            disp = "\n"
        else:
            disp = ""
        disp += " " * indent1
        line_len = indent1
        space_needed = False

        color_d = update_d.update_d.request_obj("daemon.color_d",
                                                "ColorD")

        kind, part, text = self._get_token(text)

        while kind is not None:
            if kind == "tag":
                disp += color_d.query_tag_code(part)
            else:
                parts = part.strip(" ").split(" ")

                for part in parts:

                    if width and line_len + len(part) > width:
                        disp += "\n" + " " * indent2
                        space_needed = False
                        line_len = indent2

                    if space_needed and part[0] != "\n":
                        disp += " "
                        line_len += 1

                    disp += part
                    if part[-1:] == "\n":
                        space_needed = False
                        line_len = indent2
                    else:
                        space_needed = True

                    line_len += len(part)

            kind, part, text = self._get_token(text)

        return disp


    def _get_token(self, text):
        if not text:
            return None, None, None

        open_pos = text.find("<")

        # If we find a < in position 0, then start is a tag.
        if open_pos == -1:
            return "plain", text, None
        elif open_pos == 0:
            close_pos = text.find(">")

            if close_pos == -1:
                # todo: raise exception
                return None, None

            part = text[1:close_pos]
            text = text[close_pos + 1:]
            
            return "tag", part, text

        # Start is NOT a tag.
        part = text[:open_pos]
        text = text[open_pos:]

        return "plain", part, text



if __name__ == "__main__":
    text_d = TextD()

    print(text_d.convert_tag_text("<say>Dannil says</> Foo."))


    print(text_d.split_with_tags("<say>Dannil says</> Foo."))
