import ctypes
import eel
from pyowm import OWM
from pyowm.commons.exceptions import NotFoundError, InvalidSSLCertificateError
from pyowm.utils.config import get_default_config


API = 'e75e3a2afcba4a9487fb61700de220f0'
HPA_TO_MMRTST = 0.75


def hideConsole():
    whnd = ctypes.windll.kernel32.GetConsoleWindow()
    if whnd != 0:
        ctypes.windll.user32.ShowWindow(whnd, 0)


@eel.expose
def send_data(data):
    if data:
        try:
            City = data.capitalize()
            place = City + ',RU'
            config_dict = get_default_config()
            config_dict['language'] = 'ru'
            response = OWM(
                API, config_dict
            ).weather_manager().weather_at_place(place)
            weather = response.weather
            temp = weather.temperature('celsius')['temp']
            status = weather.detailed_status.capitalize()
            pressure = weather.barometric_pressure()['press'] * HPA_TO_MMRTST
            temp = f'В городе {City} сейчас {temp:.1f} ℃',
            details = f'{status}, давление — {pressure:.1f} мм. рт. ст'
        except NotFoundError:
            temp = f'Город {City} не найден в России',
            details = 'Проверьте ввод на наличие ошибок'
        except InvalidSSLCertificateError:
            temp = 'Не удалось установить связь с сервером погоды',
            details = 'Проверьте подключение к сети'
    else:
        temp = 'Укажите город'
        details = ''
    package = {
        'temp': temp,
        'details': details
    }
    return package


hideConsole()
eel.init("web_ui")
eel.start("index.html", size=(470, 270))
