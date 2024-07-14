import requests
import time
import argparse

# IP adress of the camera
CAMERA_IP = "192.168.1.83"
CAPTURE_URL = f"http://{CAMERA_IP}/capture"
DETECT_PANNEL_URL = f"http://{CAMERA_IP}/detect_panel"

class TeddyFlight:
    def __init__(self, capture_interval:float = 3) -> None:
        # param capture_interval:: duration between each capture (in s)
        self.capture_interval = capture_interval
    
    def detect_pannel(self):
        # execute this function if u want to be sure the micasense pannel is detected prior to the images acquisition
        cresponse = self.capture_image(args={"detect_panel": True})
        if cresponse.get("status") == "error":
            print("Camera failed to detect a pannel\nRetrying in 3sRetrying in 3s............")
            time.sleep(3)
            self.detect_pannel()
        return
    
    def capture_image(self, args:dict = {}):
        # Abort any panel detection function running
        # param args : any arguments u would like to pass to the capture route 
        # (see micasense api doc here : https://micasense.github.io/rededge-api/api/http.html)
        presponse = requests.post(DETECT_PANNEL_URL, json={"abort_detect_panel": True})
        if presponse.status_code == 200:
            assert presponse.json().get("detect_panel") == False, "Failed to abort the pannel detection mode even though the request was successful\nProbably an internal error"
        else:
            print("Failed to abort the pannel detection mode")
            self.capture_image()
        if args == {}:
            response = requests.get(CAPTURE_URL)
        else:
            response = requests.post(CAPTURE_URL, json=args)
        if response.status_code == 200:
            print("Images captured successfully")
        else:
            print("Failed to capture images")
        return response.json()
    
    
    def launch(self, is_pannel_present : bool = False):
        # param is_pannel_present :: if the micasense pannel should be detected for calibration first
        if is_pannel_present: self.detect_pannel()
        while True:
            self.capture_image()
            time.sleep(self.capture_interval)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="This program launch the images acquisition script")
    parser.add_argument("-i", "--interval", type=float, help="duration between each capture (in s)")
    parser.add_argument("-p", "--pannel", type=bool, help="if the micasense pannel should be detected for calibration first")
    args = parser.parse_args()
    interval, is_pannel_present = (args.interval or 3), (args.pannel or False)
    print(f"Capture interval = {interval} and pannel present ? : {is_pannel_present}")
    f = TeddyFlight(interval)
    f.launch(is_pannel_present)

