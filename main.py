import _thread as thread

from hermite_bezier import main_hermite
# from ui import start
from mundo import main

try:
    thread.start_new_thread(main_hermite, ())
    main()
except KeyboardInterrupt:
    thread.exit()


# while(True):
#     pass
