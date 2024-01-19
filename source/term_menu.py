from simple_term_menu import TerminalMenu


def show_menu(options):
    # settings for the single-choice menu
    terminal_menu = TerminalMenu(
        options, menu_cursor_style=("fg_green", "bold"),
        menu_highlight_style=("fg_green", "bold")
    )

    # show to menu and stores the user input to choice
    menu_entry_index = terminal_menu.show()
    choice = options[menu_entry_index]

    return choice
