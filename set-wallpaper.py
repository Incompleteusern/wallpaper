import gi, subprocess, time, random, os, requests
gi.require_version('Geoclue', '2.0')
from gi.repository import Geoclue
from pathlib import Path

source_dir = Path(__file__).resolve().parent

def lat_long():
    clue = Geoclue.Simple.new_sync('something',Geoclue.AccuracyLevel.EXACT, None)

    location = clue.get_location()
    return location.get_property('latitude'), location.get_property('longitude')

def conditions(x):
    sunrise = x.get("sys").get("sunrise")
    sunset = x.get("sys").get("sunset")
    div1 = (sunrise * 4 + sunset) // 5 # LMAO
    div2 = (sunrise + sunset * 4) // 5
    now = time.time()

    weather = x.get("weather")[0].get("main")

    match weather:
        case "Drizzle" | "Thunderstorm" | "Rain":
            weather = "Rain"
        case "Atmosphere" | "Clouds":
            weather = "Clouds"
        case _:
            pass

    if now < sunrise or now > sunset:
        when = "Night"
    elif now < div1:
        when = "Morning"
    elif now > div2:
        when = "Evening"
    else:
        when = "Noon"

    return weather, when

def check_new(weather, when):
    result = f"{weather} {when}"

    print (f"Conditions are {result}")

    if os.path.isfile('/tmp/last_wallpaper_conditions'):    
        with open('/tmp/last_wallpaper_conditions', 'r') as f:
            old_result = f.read()

            if (old_result == result):
                print (f"Conditions remain the same since last checked")
                return False
            else:
                print (f"Old conditions were {old_result}")

    with open('/tmp/last_wallpaper_conditions', 'w') as f:
        f.write(result)
        print (f"Writing result to file")
    
    return True


def choose_img_file(dir):
    if not os.path.isdir(dir):
        print (f"Directory {dir} does not exist, using default wall paper")
        return None

    n = 0
    file = None
    for root, dirs, files in os.walk(dir):
        for name in files:
            if name.endswith(tuple([".jpg", ".png", ".webp"])):
                n += 1
                if random.uniform(0, n) < 1:
                    file = os.path.join(root, name)

    return file

def find_file():
    default_file = os.path.join(source_dir, "wallpapers", "default.png")
    lat, lon = lat_long()

    OWM_API_KEY = os.getenv("OWM_API_KEY")
    if OWM_API_KEY == None:
        print("Could not find api key, using default wallpaper")
        return default_file

    x = requests.get(f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OWM_API_KEY}')
    if x.status_code != 200:
        print("Failed to fetch weather information, using default wallpaper")
        return default_file

    weather, when = conditions(x.json())

    if not check_new(weather, when):
        print("Conditions have not changed since last check, keeping wall paper the same")
        return None

    # choose random file
    chosen = choose_img_file(os.path.join(source_dir, "wallpapers", weather, when))
    
    return chosen or default_file


img_file = find_file()

if img_file != None: # hacky way to not change :)
    subprocess.run(
        [
            "swww",
            "img",
            "--transition-type",
            "center",
            str(img_file),
        ],
        check=True,
    )
