from src.gui import App

# TODO: A combination containing a diaeresis or subscript will ignore 
# the symbol if another more highly-ranked symbol follows it. BUT, if we
# attempt to add a diaeresis or subscript to an impossible vowel, it is
# getting converted to a grave (it should simply be ignored in this case).
# E.g. a+ returns a\ and i| returns i\


if __name__ == "__main__":
    x: App = App()
    x.mainloop() #type:ignore

