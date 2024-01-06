# type: ignore
from tkinter import ttk
from customtkinter import (CTk,
                           CTkTextbox,
                           CTkOptionMenu)
from typing import TYPE_CHECKING

from .greek.betacode import BetacodeTokenizer

if TYPE_CHECKING:
    from .tokenizer import Tokenizer

options = ["GREEK", "LATIN"]


class App(CTk):
    """Basic GUI for text entry and conversion."""

    def __init__(self):
        super().__init__()
        self.tokenizers: dict[str, type[Tokenizer]] = {"GREEK": BetacodeTokenizer}
        self.selected_tokenizer: str = list(self.tokenizers)[0]

        # Dropdown menu (left)
        self.option_menu: CTkOptionMenu = CTkOptionMenu(self,
                                                        values=list(self.tokenizers),
                                                        command=self.change_state)
    
        self.option_menu.grid(column=0, row=0, rowspan=3, sticky='N')

        # Top box (right)
        self.input: CTkTextbox = CTkTextbox(self, width=600)
        self.input.bind("<KeyRelease>", self.update_text)
        self.input.configure(font=("times new roman", 26))
        self.input.grid(column=1, row=0)

        # Line
        self.sep: ttk.Separator = ttk.Separator(self)
        self.sep.grid(column=1, row=1, sticky="NSEW")

        # Bottom box (right)
        self.output: CTkTextbox = CTkTextbox(self, wrap="word", width=600)
        self.output.configure(font=("times new roman", 26))
        self.output.grid(column=1, row=2) 

    def change_state(self, tokenizer_name: str) -> None:
        """Change which tokenizer to use."""
        self.selected_tokenizer = tokenizer_name

    def update_text(self, *args) -> None:
        """Replace the current text with a newly parsed conversion."""
        tokenizer: type[Tokenizer] = self.tokenizers[self.selected_tokenizer]
        text: str = self.input.get("1.0", "end")
        conversion: str = str(tokenizer(text))
        self.output.delete("0.0", "end")
        self.output.insert("0.0", conversion)
