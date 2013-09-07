#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  xml_tag_match.py
#  
#  Copyright 2013 Sagar Chalise <sagar@nepways>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#
import geany
from geanypy import Document, status_message, bind_key
import itertools

class TagMatchPlugin(geany.Plugin):

    __plugin_name__ = "XML/HTML Tag Match Highlight"
    __plugin_version__ = "0.01"
    __plugin_description__ = "Highlight matching tag in XML/HTML/PHP"
    __plugin_author__ = "Sagar Chalise <chalisesagar@gmail.com>"
    
    sci = None # ScintillaObject
    file_types = ('HTML', 'PHP', 'XML')
    indicators = (geany.editor.INDICATOR_SEARCH, 1)
    
    def __init__(self):
        super(geany.Plugin, self).__init__()
        try:
            bind_key("XML Matcher", "Go to match", self.go_to_tag_match)
        except AttributeError:
            status_message("GeanyPy was not compiled with keybindings support.")
        geany.signals.connect("editor-notify", self.on_editor_notify)

    @classmethod
    def check_filetype(cls):
        cur_file_type = Document.current().filetype 
        if cur_file_type in cls.file_types:
            return True
        return False
    
    def set_indicator(self, editor, ranges):
        for indicator in self.indicators:
            for key, value in ranges.items():
                if indicator == 1:
                    new_val = [value[0]+1, value[1]-1]
                    if key == 'end':
                        new_val[0] += 1 
                    editor.indicator_set_on_range(indicator, *new_val)
                else:
                    editor.indicator_set_on_range(indicator, *value)
    
    @staticmethod
    def do_tag_matching(content, pos):
        import html_matcher
        tags = html_matcher.get_tags(content, pos)
        if tags and tags[0]:
            return tags
        else:
            return (None, None)

    def get_positions(self):
        content = self.sci.get_contents(self.sci.get_length()+1)
        current_pos = self.sci.get_current_position()
        open_tag, close_tag = self.do_tag_matching(content, current_pos)
        tag_positions = {}
        if close_tag:
            tag_positions = {'begin': (open_tag.start, open_tag.end),
                           'end': (close_tag.start, close_tag.end)} 
            check_position_range = itertools.chain(xrange(*tag_positions['begin']), xrange(tag_positions['end'][0]+1, tag_positions['end'][1]))
            if current_pos in check_position_range:
                return (True, current_pos, tag_positions)
        return (False, current_pos, tag_positions)

    def go_to_tag_match(self, key_id):
        if self.check_filetype():
            valid, cur_pos, tag_pos = self.get_positions()
            if valid:
                if cur_pos in xrange(*tag_pos['begin']):
                    self.sci.set_current_position(tag_pos['end'][0], True)
                elif cur_pos in xrange(*tag_pos['end']):
                    self.sci.set_current_position(tag_pos['begin'][0], True)
        
    def on_editor_notify(self, g_obj, editor, nt):
        if self.check_filetype():
            self.sci = editor.scintilla
            notification_codes = (geany.scintilla.UPDATE_UI, geany.scintilla.KEY)
            if nt.nmhdr.code in notification_codes:
                for indicator in self.indicators:
                    editor.indicator_clear(indicator)
                valid, cur_pos, tag_pos = self.get_positions()
                if valid:
                    self.set_indicator(editor, tag_pos)


def main():
    return 0

if __name__ == '__main__':
    main()