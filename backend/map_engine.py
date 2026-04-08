from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.graphics.texture import Texture
import io
from PIL import Image as PILImage

from backend.map_engine import load_tile
from backend.overlay import get_stop_markers, get_live_bus_markers

class MapViewer(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Example tile (zoom=12, x=2100, y=1450)
        tile_data = load_tile(12, 2100, 1450)
        if tile_data:
            pil_img = PILImage.open(io.BytesIO(tile_data))
            tex = Texture.create(size=pil_img.size)
            tex.blit_buffer(pil_img.tobytes(), colorfmt='rgb', bufferfmt='ubyte')
            tex.flip_vertical()
            self.add_widget(Image(texture=tex, size_hint=(1,1)))

        # Overlay stops
        for m in get_stop_markers():
            self.add_widget(Label(text="📍"+m["label"], pos_hint={"x":0.5,"y":0.5}))

        # Overlay live buses
        for b in get_live_bus_markers():
            self.add_widget(Label(text="🚌"+b["label"], pos_hint={"x":0.6,"y":0.6}))

class MapApp(App):
    def build(self):
        return MapViewer()

if __name__ == "__main__":
    MapApp().run()
