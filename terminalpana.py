#!/usr/bin/env python3

import urwid

class TextEdit(urwid.Widget):
    """
    A multiline text edit widget with a fixed text wrap which doesn't make the
    line shift to the right when the line is full and the cursor is at the end
    of the line.
    """
    # TODO: scrolling
    _sizing = frozenset(['flow'])
    _selectable = True

    def __init__(self):
        self.edit = urwid.Edit(multiline=True)

    def keypress(self, size, key):
        return self.edit.keypress(size, key)

    def rows(self, size, focus=False):
        return self.edit.rows((size[0]-1,), False)

    def render(self, size, focus=False):
        """
        Render the edit field with one blank column to the right where the
        cursor can be displayed.
        """
        canvas = urwid.CompositeCanvas(self.edit.render((size[0]-1,), False))
        canvas.pad_trim_left_right(0, 1)
        # Get the text layout structure
        line_translation = urwid.Text.get_line_translation(self.edit,
                                                           size[0]-1, None)
        # Calculate the position. Note that the x coordinate is NOT clipped,
        # which means that the cursor will end up in the rightmost column when
        # the line is full instead of staying on the column just to the left
        # of it.
        canvas.cursor = urwid.text_layout.calc_coords(self.edit.text,
                                                      line_translation,
                                                      self.edit.edit_pos)
        return canvas

def main():
    edit = TextEdit()
    # temp shit deluxe
    filler = urwid.Filler(edit, valign='top')
    frame = urwid.Frame(filler)
    loop = urwid.MainLoop(frame)
    loop.run()


if __name__ == '__main__':
    main()
