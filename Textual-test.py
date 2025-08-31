from textual import log, events
import time
from textual.app import App, ComposeResult
from textual.containers import VerticalGroup, VerticalScroll, ScrollableContainer, Vertical
from textual.widgets import Static, Header, Footer, Collapsible, Button, Label, Input, Markdown

from textual.widget import Widget
from textual.reactive import reactive
from main import conversation, Chat, DIRCTORY_NAME


class Sidebar(Widget):
    def compose(self) -> ComposeResult:
        yield Label("History", id="History_label")
        with VerticalScroll(id="History_Scroll"):
            yield Button("New Chat", variant="default", id="new_chat_button")

    def add_history_button(self, Title:str, id:str) -> None: # the id here will always start with id so the id= idxxxxxxxxxxx (this because the id paramter can't contain ONLY number!?)
        history_scroll =  self.get_child_by_id("History_Scroll")
        button = Button(Title, variant="default", classes="history_button", id=id)
        log(f"adding {button}, to {history_scroll}")
        history_scroll.mount(button)

class AI_Message(Static):
    BORDER_TITLE = "gpt-mini-4o"  

    def __init__(self, message:str):
        self.message = message
        super().__init__()

    def render(self):
        return self.message
    
class User_message(Static):
    BORDER_TITLE = "albrrak"
    def __init__(self, message:str):
        self.message = message
        super().__init__()

    def render(self):
        return self.message
    
class Messages(VerticalScroll):

    def init_messages(self,  messages_list:list = []):
        for child in list(self.children):
            child.remove()

        for message in messages_list:
            if message['role'] == 'user':
                self.Add_user_message(message['content'])
            if message['role'] == 'assistant':
                self.Add_AI_message(message['content'])

    def Add_user_message(self, text:str):
        self.mount(User_message(text))

    def Add_AI_message(self, text:str):
        self.mount(AI_Message(text))

class CustomApp(App):

    CSS_PATH = "TUI.tcss"
    TITLE = "gpt-4o-mini"
    BINDINGS = [("s", "toggle_sidebar", "Toggle Sidebar"), ("S", "toggle_sidebar", "Toggle Sidebar")]
    show_sidebar = reactive(False)

    def __init__(self):
        self.chat = Chat()
        self.sideBar = Sidebar()

        self.input = Input(placeholder="Enter a prompt (hit 's' to see history)", tooltip="is this what a tooltip is?")
        self.messages = Messages()
        self.current_conversaton = self.chat.get_latest_conversation()
        self.messages_list = self.current_conversaton.get_messsages()
        super().__init__()

    
    def compose(self) -> ComposeResult:
        yield self.input
        yield self.sideBar

    def on_mount(self):
        self.mount(self.messages)
        self.messages.init_messages(self.messages_list)
        for conversation in self.chat.get_conversation_names():
            self.sideBar.add_history_button(conversation[0], "id" + str(conversation[1])) # the id here will always start with id so the id= idxxxxxxxxxxx (this because the id paramter can't contain ONLY number!?)

    def on_input_submitted(self):
        user_input = self.input.value
        self.messages.Add_user_message(user_input)
        self.input.clear()
        self.input.disabled = True
        self.messages.Add_AI_message(self.current_conversaton.get_AI_answer(user_input))
        self.input.disabled = False
        # self.sideBar.add_history_button(self.current_conversaton.title, self.current_conversaton.id)
        self.messages.anchor()


    def on_button_pressed(self, event: Button.Pressed):
        print(f"The button {event.button.label} was pressed")
        print(f"the id is: {event.button.id}")
        if event.button.id == "new_chat_button":
            self.current_conversaton = self.chat.create_conversation()
            self.messages.init_messages()
        else:
            self.current_conversaton = self.chat.get_conversation_by_id(int(event.button.id.split('id')[1]))
            self.messages.init_messages(self.current_conversaton.get_messsages())

    def on_key(self, event: events.Key):
        if event.key == "escape":  # Check if ESC was pressed
            print("THE Escape key was pressed!")
            print(f"Is Messages() focusable? '{self.messages.focusable}'")
            print(f"Is Messages() anchrable? '{self.messages.is_anchored}'")
            self.set_focus(self.messages, True)
            print(f"the currently focused thing is: {self.focused}")




    def action_toggle_sidebar(self) -> None:
        """Toggle the sidebar visibility."""
        self.show_sidebar = not self.show_sidebar
        self.input.disabled = False

    def watch_show_sidebar(self, show_sidebar: bool) -> None:
        """Set or unset visible class when reactive changes."""
        self.query_one(Sidebar).set_class(show_sidebar, "-visible")




if __name__ == "__main__":
    app = CustomApp()
    app.run()

