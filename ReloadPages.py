from PagesGenerator import ReloadPages

import time

start_time = time.time()
x = ReloadPages()
print("Runtime: %s s" % (round(time.time() - start_time, 1)))
print("Pages Edited: %s" % x)

