# type: ignore
from tkinter import Event
from customtkinter import (CTk,
                           CTkTextbox,
                           CTkFrame,
                           CTkOptionMenu)

from .betacode import BetacodeTokenizer
from .tokenizer import Tokenizer

options = ["GREEK", "LATIN"]


class App(CTk):

    def __init__(self):
        super().__init__()
        self.tokenizers: dict[str, type[Tokenizer]] = {"GREEK": BetacodeTokenizer}
        self.current_state: str = list(self.tokenizers)[0]

        self.option_menu: CTkOptionMenu = CTkOptionMenu(self,
                                                        values=list(self.tokenizers),
                                                        command=self.change_state)
    
        self.option_menu.grid(column=0, row=0)

        self.top_block: CTkFrame = CTkFrame(self, width=300)
        self.input: CTkTextbox = CTkTextbox(self.top_block, width=300)
        self.input.bind("<KeyRelease>", self.update_text)
        self.input.grid()
        self.top_block.grid(column=1, row=0)

        self.bottom_block: CTkFrame = CTkFrame(self, width=300)
        self.output: CTkTextbox = CTkTextbox(self.bottom_block, wrap="word", width=300)
        self.output.grid()
        self.bottom_block.grid(column=1, row=1)
        

    def change_state(self, state_name: str) -> None:
        self.current_state = state_name
    

    def update_text(self, event: Event) -> None:
        tokenizer: type[Tokenizer] = self.tokenizers[self.current_state]
        text: str = self.input.get("1.0", "end")
        conversion: str = str(tokenizer(text))
        self.output.delete("0.0", "end")
        self.output.insert("0.0", conversion)
