#!/usr/bin/env python3

import urwid

class TextEdit(urwid.Widget):
    """
    A multiline text edit widget with a fixed text wrap which doesn't make the
    line shift to the right when the line is full and the cursor is at the end
    of the line.
    """
    _sizing = frozenset(['box'])
    _selectable = True

    def __init__(self):
        self.edit = urwid.Edit(multiline=True)
        # The view's offset (in lines)
        self.offset = 0
        # The position of the view (0 is at the top, 1 at the bottom)
        self.scroll_position = 0.0

    def keypress(self, size, key):
        return self.edit.keypress((size[0],), key)

    def render(self, size, focus=False):
        """
        Render the edit field with one blank column to the right where the
        cursor can be displayed.
        """
        width, height = size
        canvas = urwid.CompositeCanvas(self.edit.render((width-1,), False))
        canvas.pad_trim_left_right(0, 1)
        # Get the text layout structure
        line_translation = urwid.Text.get_line_translation(self.edit,
                                                           width-1, None)
        # Calculate the position. Note that the x coordinate is NOT clipped,
        # which means that the cursor will end up in the rightmost column when
        # the line is full instead of staying on the column just to the left
        # of it.
        x,y = urwid.text_layout.calc_coords(self.edit.text,
                                            line_translation,
                                            self.edit.edit_pos)
        canvas.cursor = (x,y)
        if y < self.offset:
            self.offset = y
        elif y >= self.offset + height:
            self.offset = y - height + 1
        # Only bother calculating scroll position if scrolling is possible
        if canvas.rows() > height:
            self.scroll_position = self.offset / (canvas.rows() - height)
        else:
            self.scroll_position = 0.0
        urwid.emit_signal(self, 'scroll_change', str(self.scroll_position))
        canvas.pad_trim_top_bottom(-self.offset, (self.offset + height) - canvas.rows())
        return canvas


def main():
    edit = TextEdit()
    status = urwid.Text('')
    urwid.register_signal(TextEdit, ['scroll_change'])
    urwid.connect_signal(edit, 'scroll_change', status.set_text)
    frame = urwid.Frame(edit, footer=status)
    loop = urwid.MainLoop(frame)
    loop.run()


if __name__ == '__main__':
    main()
