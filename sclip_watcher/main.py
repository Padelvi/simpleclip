from Xlib import display
from Xlib.ext import xfixes

def main() -> None:
    d = display.Display()
    screen = d.screen()

    window = screen.root.create_window(
        0,
        0,
        1,
        1,
        0,
        screen.root_depth,
    )

    clipboard = d.intern_atom("CLIPBOARD")

    xfixes.select_selection_input(
        d,
        window,
        clipboard,
        xfixes.XFixesSetSelectionOwnerNotifyMask,
    )

    d.flush()

    while True:
        event = d.next_event()

        print(event)


if __name__ == "__main__":
    main()