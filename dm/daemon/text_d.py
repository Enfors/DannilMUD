# text_d.py by Dannil

import dm.daemon.daemon as daemon

NEWLINE="\n"

class TextD(daemon.Daemon):
    
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



if __name__ == "__main__":
    text_d = TextD()

    print(text_d.wrap("""How can you see into my eyes
like open doors?
Leading you down into my core
where I've become so numb.

Without a soul
my spirit sleeping somewhere cold
until you find it there and lead
it back home.""", 40, 4, 2))
