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
import itertools

class TagMatchPlugin(geany.Plugin):

    __plugin_name__ = "XML/HTML Tag Match Highlight"
    __plugin_version__ = "0.01"
    __plugin_description__ = "Highlight matching tag in XML/HTML/PHP"
    __plugin_author__ = "Sagar Chalise <chalisesagar@gmail.com>"
    sci = None # ScintillaObject
    file_types = ('HTML', 'PHP', 'XML')

    def __init__(self):
        super(geany.Plugin, self).__init__()
        geany.signals.connect("editor-notify", self.on_editor_notify)

    @classmethod
    def check_filetype(cls):
        cur_file_type = geany.document.get_current().file_type.name 
        if cur_file_type in cls.file_types:
            return True
        return False
   
    @staticmethod
    def set_indicator(editor, indicators, ranges):
        for indicator in indicators:
            for key,value in ranges.items():
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
    
    def on_editor_notify(self, g_obj, editor, nt):
        if self.check_filetype():
            self.sci = editor.scintilla
            if nt.nmhdr.code in (geany.scintilla.UPDATE_UI, geany.scintilla.KEY):
                content = self.sci.get_contents(self.sci.get_length()+1)
                indicators = (geany.editor.INDICATOR_SEARCH, 1)
                for indicator in indicators:
                    editor.indicator_clear(indicator)
                current_pos = self.sci.get_current_position()
                open_tag, close_tag = self.do_tag_matching(content, current_pos)
                if close_tag:
                    tag_positions = {'begin': (open_tag.start, open_tag.end),
                                    'end': (close_tag.start, close_tag.end)} 
                    check_position_range = itertools.chain(xrange(*tag_positions['begin']), xrange(*tag_positions['end']))
                    if current_pos in check_position_range:
                        self.set_indicator(editor, indicators, tag_positions)


def main():
    return 0

if __name__ == '__main__':
    main()