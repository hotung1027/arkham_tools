import jq 
import requests
import json
from rich.segment import Segment
from textual.app import App , ComposeResult 
from textual.containers import VerticalScroll
from textual.geometry import Size
from textual.strip import Strip
from textual.widgets import Static, Button, Checkbox
from textual.scroll_view import ScrollView
from textual.widget import Widget
# ArkhamDB API Endpoint
api_endpoint = "https://arkhamdb.com/api/public/cards"
# Get the response from ArkhamDB API
response = requests.get(api_endpoint)
response_json = response.json() if response is not None else Exception("No response from ArkhamDB API")

collections_jq = 'map(select(.type_code=="investigator"))|[ .[] | {pack_name : .pack_name, pack_code: .pack_code, investigator: .name, faction: .factor_code }]|unique_by(.pack_name)'
investigators_jq = 'map(select(.type_code=="investigator"))|[ .[] | {pack_name : .pack_name, pack_code: .pack_code}]|unique_by(.pack_name)'

collections = jq.compile(collections_jq).input_value(response_json).first()
class Cards_Update(Static):
    pass

class Collections(Widget):

    CSS_PATH = "collections.tcss"

    COLLECTIONS = [Checkbox(pack["pack_name"], id=pack["pack_code"]) for pack in collections] 

    def __init__(self) -> None:
        super().__init__()
        # Each square is 4 rows and 8 columns
        self.virtual_size = Size(len(self.COLLECTIONS), 1)

    # def render_line(self,y:int)->Strip:
    #     # segment = [Segment(self.COLLECTIONS[y])]
    #     strip = Strip(self.COLLECTIONS,len(self.COLLECTIONS))
    #     return strip

    def compose(self) -> ComposeResult:
        with VerticalScroll():
            for pack in self.COLLECTIONS:
                yield pack


    # def on_mount(self):    


class Arkham_Roles(App):
    TITLE = "Arkham Roles"
    CSS_PATH = "layout.tcss"

    def compose(self) -> ComposeResult:
        yield Collections()





if __name__ == "__main__":
    app = Arkham_Roles(    )
    app.run()


