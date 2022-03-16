import os
for i in range(1989,2022):
    newpath = str(i)
    if not os.path.exists(newpath):
        os.makedirs(newpath)
