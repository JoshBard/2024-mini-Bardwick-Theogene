"""
Response time - single-threaded
"""

from machine import Pin
import time
import random
import json
import urequests  # For cloud upload
import ujson  # For JSON encoding in Firebase Realtime Database


N: int = 10  # Changed to 10 flashes
sample_ms = 10.0
on_ms = 500


def random_time_interval(tmin: float, tmax: float) -> float:
    """return a random time interval between max and min"""
    return random.uniform(tmin, tmax)


def blinker(N: int, led: Pin) -> None:
    # %% let user know game started / is over

    for _ in range(N):
        led.high()
        time.sleep(0.1)
        led.low()
        time.sleep(0.1)


def write_json(json_filename: str, data: dict) -> None:
    """Writes data to a JSON file.

    Parameters
    ----------

    json_filename: str
        The name of the file to write to. This will overwrite any existing file.

    data: dict
        Dictionary data to write to the file.
    """

    with open(json_filename, "w") as f:
        json.dump(data, f)


def scorer(t: list[int | None]) -> None:
    # %% collate results
    misses = t.count(None)
    print(f"You missed the light {misses} / {len(t)} times")

    t_good = [x for x in t if x is not None]

    # Calculate statistics
    avg_time = sum(t_good) / len(t_good) if t_good else None
    min_time = min(t_good) if t_good else None
    max_time = max(t_good) if t_good else None
    score = len(t_good) / len(t)

     # add key, value to this dict to store the minimum, maximum, average response time
    # and score (non-misses / total flashes) i.e. the score a floating point number
    # is in range [0..1]

    data = {
        "average_time": avg_time,
        "min_time": min_time,
        "max_time": max_time,
        "score": score,
        "misses": misses,
        "total_flashes": len(t)
    }

    # %% make dynamic filename and write JSON

    now: tuple[int] = time.localtime()

    now_str = "-".join(map(str, now[:3])) + "T" + "_".join(map(str, now[3:6]))
    filename = f"score-{now_str}.json"

    print("write", filename)

    write_json(filename, data)

    # Upload data to cloud
    upload_to_cloud(data)

# """Upload data to a cloud service."""

def upload_to_cloud(data: dict) -> None:
    """Upload data to Firebase Realtime Database."""
    # Firebase project URL
    firebase_url = "https://seniordesigni-musicproj-default-rtdb.firebaseio.com"
    # Firebase database secret
    auth_token = "GjuQq5SBEKPPKE4Gme2Q2vbNurEjhj0dmTliPwnS"
    
    # Create a unique key for this data entry (you can use a timestamp)
    timestamp = str(time.time())
    
    url = f"{firebase_url}/response_times/{timestamp}.json?auth={auth_token}"
    
    print(f"Uploading data: {data}")
    try:
        response = urequests.put(url, data=ujson.dumps(data))
        print(f"Response status code: {response.status_code}")
        print(f"Response content: {response.text}")
        print("Upload successful" if response.status_code == 200 else "Upload failed")
    except Exception as e:
        print(f"Upload error: {e}")


if __name__ == "__main__":
    # using "if __name__" allows us to reuse functions in other script files

    led = Pin("LED", Pin.OUT)
    button = Pin(16, Pin.IN, Pin.PULL_UP)

    t: list[int | None] = []

    blinker(3, led)

    for i in range(N):
        time.sleep(random_time_interval(0.5, 5.0))

        led.high()

        tic = time.ticks_ms()
        t0 = None
        while time.ticks_diff(time.ticks_ms(), tic) < on_ms:
            if button.value() == 0:
                t0 = time.ticks_diff(time.ticks_ms(), tic)
                led.low()
                break
        t.append(t0)

        led.low()

    blinker(5, led)

    scorer(t)
