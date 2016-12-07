import _thread as thread

from hermite_bezier import main_hermite
from ui import start

try:
    thread.start_new_thread(main_hermite, ())
    start()
except KeyboardInterrupt:
    thread.exit()