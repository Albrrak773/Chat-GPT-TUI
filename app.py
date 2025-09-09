from textual.app import App, ComposeResult
from textual.widgets import Input, Markdown, Button, Select
from textual.containers import VerticalScroll, Vertical, Grid, Container

DEFAULT_MODEL = "GPT-4o-mini"
DEFAULT_UESR_NAME = "user"

AVALIABLE_MODLES = [("ChatGPT-4o-mini", "gpt-4o-mini"), ("Gemini-2.5-flash", "gemini-2.5-flash")]

LOCKED_MODELS = [
    ("ChatGPT-4o", "gpt-4o"),
    ("Gemin-2.5-Pro", "2.5-pro")
]

# OPTIONS = AVALIBALE_MODELS.append(m for m in LOCKED_MODELS)

class User_message(Markdown):
    def __init__(self, markdown = None, *, name = None, id = None, classes = None, parser_factory = None, open_links = True, border_title: str = DEFAULT_UESR_NAME):
        self.BORDER_TITLE = border_title
        if not classes:
            classes = "message"
        super().__init__(markdown, name=name, id=id, classes=classes, parser_factory=parser_factory, open_links=open_links)


class AI_message(Markdown):
    def __init__(self, markdown = None, *, name = None, id = None, classes = None, parser_factory = None, open_links = True, border_title: str = DEFAULT_MODEL):
        self.BORDER_TITLE = border_title
        if not classes:
            classes = "message"
        super().__init__(markdown, name=name, id=id, classes=classes, parser_factory=parser_factory, open_links=open_links)


class Messages(VerticalScroll):
    def __init__(self, *children, name = None, id = None, classes = None, disabled = False, can_focus = None, can_focus_children = None, can_maximize = None):
        super().__init__(*children, name=name, id=id, classes=classes, disabled=disabled, can_focus=can_focus, can_focus_children=can_focus_children, can_maximize=can_maximize)

class AI_App(App):
    CSS_PATH = "style.tcss"
    def compose(self) -> ComposeResult:
        with Grid(id="main"):
            with Vertical(id="menu"):
                yield Button("☰")
                yield Button("+")
                yield Button("📌", id="pallet-btn")
            with VerticalScroll(id="conversation"):
                with Messages(can_focus=False):
                    for _ in range(5):
                        yield User_message("what is the capital of japan?")
                        yield AI_message("The capital of japan is Tokoy.")        
                with Container(id="input-container"):
                    with Grid(id="input-grid"):
                        yield Input(placeholder="ask anything...")
                        yield Button("⇑", compact=True) 
                        yield Select(AVALIABLE_MODLES, allow_blank=False, compact=True)
    def on_mount(self):
        self.theme = "catppuccin-mocha"


        

if __name__ == "__main__":
    AI_App().run()