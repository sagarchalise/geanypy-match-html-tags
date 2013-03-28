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

class TagMatchPlugin(geany.Plugin):

    __plugin_name__ = "XML/HTML Tag Match Highlight"
    __plugin_version__ = "0.01"
    __plugin_description__ = "Highlight matching tag in XML/HTML/PHP"
    __plugin_author__ = "Sagar Chalise <chalisesagar@gmail.com>"
    sci = None # ScintillaObject
    file_types = ('HTML', 'PHP', 'XML')

    def __init__(self):
        geany.Plugin.__init__(self)
        geany.signals.connect("editor-notify", self.onEditorNotify)

    def onEditorNotify(self, obj, editor, nt):
        if geany.document.get_current().file_type.name in self.file_types:
            self.sci = editor.scintilla
            if nt.nmhdr.code == geany.scintilla.UPDATE_UI or nt.nmhdr.code == geany.scintilla.KEY:
                content = self.sci.get_contents(self.sci.get_length()+1)
                editor.indicator_clear(geany.editor.INDICATOR_SEARCH)
                editor.indicator_clear(1)
                current_pos = self.sci.get_current_position()
                import html_matcher
                tags = html_matcher.get_tags(content, current_pos)
                if tags and tags[0]:
                    open_tag, close_tag = tags
                    if close_tag:
                        import itertools
                        if current_pos in itertools.chain(xrange(open_tag.start, open_tag.end), xrange(close_tag.start, close_tag.end)):
                            editor.indicator_set_on_range(geany.editor.INDICATOR_SEARCH, open_tag.start, open_tag.end)
                            editor.indicator_set_on_range(1, open_tag.start, open_tag.end)
                            editor.indicator_set_on_range(geany.editor.INDICATOR_SEARCH, close_tag.start, close_tag.end)
                            editor.indicator_set_on_range(1, close_tag.start, close_tag.end)

def main():
    return 0

if __name__ == '__main__':
    main()