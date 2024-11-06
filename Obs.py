import obsws_python as obs
import time
import toml

class Obs:
    def __init__(self, host='localhost', port=4455, password=''):
        self.host = host
        self.port = port
        self.password = password
        self.client = None
        self.current_source_name = None
        self.config = toml.load("./config.toml")

    def connect(self):
        self.client = obs.ReqClient(host=self.host, port=self.port, password=self.password)
        print("Connected to OBS WebSocket server.")

    def disconnect(self):
        if self.client:
            self.client.disconnect()
            self.client = None
            print("Disconnected from OBS WebSocket server.")

    def start_streaming(self):
        if self.client:
            self.client.start_stream()
            

    def stop_streaming(self):
        try:
            if self.client:
                self.client.stop_stream()
                print("Stopped streaming.")
        except:
            print("stopring stream without starting")        

    def set_streaming_service(self, platform):
        try:
            if platform.lower() == "youtube":
                settings = {
                    "type": "rtmp_common",
                    "settings": {
                        "service": self.config['youtube']['service'],
                        "server": self.config['youtube']['server'],
                        "key": self.config['youtube']['key']
                    }
                }
            elif platform.lower() == "twitch":
                settings = {
                    "type": "rtmp_common",
                    "settings": {
                        "service": self.config['twitch']['service'],
                        "server": self.config['twitch']['server'],
                        "key": self.config['twitch']['key']
                    }
                }
            else:
                raise ValueError("Unsupported platform")

            self.client.set_stream_service_settings(settings['type'], settings['settings'])
            print(f"Streaming service set to {platform}.")
        except obs.error.OBSSDKRequestError as e:
            print(f"Error setting streaming service: {e}")


    def create_source(self, scene_name, source_name, source_kind, settings, scene_item_enabled=True):
        try:
            self.client.create_input(
                scene_name,
                source_name,
                source_kind,
                settings,
                scene_item_enabled
            )
            print(f"Created source {source_name}.")
        except obs.error.OBSSDKRequestError as e:
            print(f"Error creating source {source_name}: {e}")

    def set_fit_to_screen(self, source_name, scene_name='Scene'):
        try:
            items = self.client.get_scene_item_list(scene_name).scene_items
            item_id = next(item['sceneItemId'] for item in items if item['sourceName'] == source_name)

            # Transform settings to fit the screen
            self.client.set_scene_item_transform(
                scene_name,
                item_id,
                {
                    'alignment': 5,  # Center alignment
                    'boundsAlignment': 0,
                    'boundsHeight': 1080.0,
                    'boundsType': 'OBS_BOUNDS_SCALE_INNER',
                    'boundsWidth': 1920.0,
                    'cropBottom': 0,
                    'cropLeft': 0,
                    'cropRight': 0,
                    'cropTop': 0,
                    'height': 1080.0,
                    'positionX': 0.0,
                    'positionY': 0.0,
                    'rotation': 0.0,
                    'scaleX': 1.0,
                    'scaleY': 1.0,
                    'sourceHeight': 1080.0,
                    'sourceWidth': 1920.0,
                    'width': 1920.0
                }
            )
            print(f"Set {source_name} to fit the screen and centered it.")
        except StopIteration:
            print(f"Source name '{source_name}' not found in the current scene.")
        except obs.error.OBSSDKRequestError as e:
            print(f"Error fitting {source_name} to screen: {e}")

    def remove_current_source(self, scene_name='Scene'):
            try:
                items = self.client.get_scene_item_list(scene_name).scene_items
                if len(items):
                    item_id = next(item['sceneItemId'] for item in items if item['sourceName'] == "BrowserSource")
                    if item_id:
                        self.client.remove_scene_item(scene_name, item_id)
                    print(f"Removed source {self.current_source_name}.")
                self.current_source_name = None

            except StopIteration:
                print(f"Source name '{self.current_source_name}' not found in the current scene.")
            except obs.error.OBSSDKRequestError as e:
                print(f"Error removing source {self.current_source_name}: {e}")


            try:
                items = self.client.get_scene_item_list(scene_name).scene_items
                if len(items):
                    item_id = next(item['sceneItemId'] for item in items if item['sourceName'] == "MediaSource")
                    if item_id:
                        self.client.remove_scene_item(scene_name, item_id)
                    print(f"Removed source {self.current_source_name}.")
                self.current_source_name = None

            except StopIteration:
                print(f"Source name '{self.current_source_name}' not found in the current scene.")
            except obs.error.OBSSDKRequestError as e:
                print(f"Error removing source {self.current_source_name}: {e}")

    def set_video_with_link_in_view(self, link, source_name="BrowserSource", overlay=True):
        if self.client:
            self.remove_current_source()
            try:
                self.client.set_input_settings(
                    source_name,
                    {
                        "url": link,
                        "width": 1920,
                        "height": 1080
                    },
                    overlay
                )
                print(f"Set video link {link} in view on source {source_name}.")
            except obs.error.OBSSDKRequestError as e:
                if 'No source was found' in str(e):
                    print(f"Source {source_name} not found, creating it.")
                    self.create_source('Scene', source_name, "browser_source", {"url": link, "width": 1920, "height": 1080})
                    self.client.set_input_settings(
                        source_name,
                        {
                            "url": link,
                            "width": 1920,
                            "height": 1080
                        },
                        overlay
                    )
            self.set_fit_to_screen(source_name)
            self.current_source_name = source_name

    def set_video_with_path_in_view(self, video_path, source_name="MediaSource", overlay=True):
        if self.client:
            self.remove_current_source()
            try:
                self.client.set_input_settings(
                    source_name,
                    {
                        "local_file": video_path,
                        "width": 1920,
                        "height": 1080
                    },
                    overlay
                )
                print(f"Set video path {video_path} in view on source {source_name}.")
            except obs.error.OBSSDKRequestError as e:
                if 'No source was found' in str(e):
                    print(f"Source {source_name} not found, creating it.")
                    self.create_source('Scene', source_name, "ffmpeg_source", {"local_file": video_path, "width": 1920, "height": 1080})
                    self.client.set_input_settings(
                        source_name,
                        {
                            "local_file": video_path,
                            "width": 1920,
                            "height": 1080
                        },
                        overlay
                    )
            self.set_fit_to_screen(source_name)
            self.current_source_name = source_name

# ob = Obs("localhost", 4444, "password")

# ob.connect()

# ob.set_video_with_link_in_view("https://www.youtube.com/watch?v=wiiAl43U66M")
# ob.set_video_with_path_in_view("C:\\Users\\Mark Deman\\Downloads\\15921892-uhd_3840_2160_50fps.mp4")

# ob.set_streaming_service("Twitch")

# ob.start_streaming() 
