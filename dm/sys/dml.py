#!/usr/bin/env python
# dml.py - Dannil Markup Language - by Dannil

"""Handle Dannil Markup Language files."""

import re # Regular expressions module

# Define exceptions
# pass

open_tag_pattern  = re.compile("^<[^/][^>]+>")
close_tag_pattern = re.compile("^</.*>")
word_pattern      = re.compile("^[^ \t\r\n<]+")

#
# Class DmlDoc
#

class DmlDoc:
    #
    # Public functions
    #
    def __init__(self, name, dir):
        self.name = name
        self.dir  = dir
        self.tree = []
        self._buffer = ""
        self._indent = 0


    def load(self):
        file = open("%s/%s.dml" % (self.dir, self.name), 'r')
        text = file.read()
        file.close()
        self._parse(text.strip())

        
    #
    # Private functions
    #
    def _parse(self, text):
        while text:
            if text[0] == "<":
                token = self._parse_tag(text)
            else:
                token = self._parse_word(text)
            text = text[len(token):].lstrip()
        

    def _parse_tag(self, text):
        match = open_tag_pattern.match(text)

        if match:
            tag = match.string[match.start():match.end()]
            self._flush()
            print "%s%s" % (self._indent * "  ", tag)
            self._indent += 1
            return tag
        
        match = close_tag_pattern.match(text)

        if match:
            self._flush()
            tag = match.string[match.start():match.end()]
            self._indent -= 1
            print "%s%s" % ("  " * self._indent, tag)
            return tag


    def _parse_word(self, text):
        match = word_pattern.match(text)

        if match:
            word = match.string[match.start():match.end()]
            self._buffer += word + " "
            return word

    
    def _flush(self):
        if not self._buffer:
            return

        print "%s%s" % ("  " * self._indent, self._buffer.rstrip())
        self._buffer = ""
            
        


if __name__ == "__main__":
    doc = DmlDoc("test", ".")
    doc.load()
    
