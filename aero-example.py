import requests
import sys
import time

from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics

options = RGBMatrixOptions()
options.rows = 64
options.cols = 64
options.chain_length = 2
options.parallel = 1
options.gpio_slowdown = 4
options.hardware_mapping = 'adafruit-hat'

matrix = RGBMatrix(options = options)
font = graphics.Font()
font.LoadFont("./rpi-rgb-led-matrix/fonts/7x13.bdf")
textColor = graphics.Color(255, 255, 0)

headers = {
    'Accept': 'application/json; charset=UTF-8',
    'x-apikey': open("api-key").read()
}
KDCA_WIDE_BOX = (38.7507906128, -77.1946776845, 38.9609310495, -76.8983901478)
KDCA_VIEWABLE_BOX = (38.8559679944, -77.0502465088, 38.8748807876, -77.028703006)

def get_itinerary(flight_data):
    try:
        origin = flight_data['origin']['code']
    except:
        origin = None

    try:
        dest = flight_data['destination']['code']
    except:
        dest = None

    return (origin, dest)

def get_flights(bounding_box):
    response = requests.get(
        f"https://aeroapi.flightaware.com/aeroapi/flights/search?query=-latlong+%22{bounding_box[0]}+{bounding_box[1]}+{bounding_box[2]}+{bounding_box[3]}%22",
        headers=headers)
    try:
        return response.json()['flights']
    except:
        return []

def monitor_viewable():
    while True:
        viewable_flights = get_flights(KDCA_VIEWABLE_BOX)
        print("viewable!:", list(f['ident'] for f in viewable_flights))
        if not viewable_flights:
            break
        graphics.DrawText(matrix, font, 2, 30, graphics.Color(0, 255, 255), "viewable:")
        graphics.DrawText(matrix, font, 2, 40, graphics.Color(0, 255, 255), f"{viewable_flights[0]['ident']} ({viewable_flights[0]['aircraft_type']})")
        time.sleep(5)
        matrix.Clear()


while True:
    matrix.Clear()
    candidate_flights = get_flights(KDCA_WIDE_BOX)
    print("candidates:", list(f['ident'] for f in candidate_flights))
    graphics.DrawText(matrix, font, 2, 10, graphics.Color(0, 0, 255), "nearby:")
    graphics.DrawText(matrix, font, 2, 20, graphics.Color(0, 0, 255), " ".join(list(f['ident'] for f in candidate_flights)))
    potentially_viewable_flights = [f for f in candidate_flights if ('KDCA' in get_itinerary(f))]
    print("viewable?:", list(f['ident'] for f in potentially_viewable_flights))
    if potentially_viewable_flights:
        monitor_viewable()
        print("no longer viewing...")
    time.sleep(10)

