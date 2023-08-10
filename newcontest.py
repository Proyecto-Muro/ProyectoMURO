import os

def NewContest(name, year, problemnum = 6):

    # Create files in concursos
    newpath = 'concursos/%s/%s'%(name, str(year))
    if not os.path.exists(newpath):
        os.makedirs(newpath)
        os.makedirs(newpath + '/enunciados')
        os.makedirs(newpath + '/soluciones')

    # Create folders in concursostex
    newpath = 'concursostex/%s/%s'%(name, str(year))
    if not os.path.exists(newpath):
        os.makedirs(newpath)
        os.makedirs(newpath + '/enunciados')
        os.makedirs(newpath + '/soluciones')

    newpath = 'ProyectoMURO/public_html/%s/%s'%(name, str(year))
    if not os.path.exists(newpath):
        os.makedirs(newpath)
        f = open(newpath + '/index.html', 'w')
        f.write('')
        f.close


    for p in range(1, problemnum+1):

        # Create tex files
        for x in ['', 'tex']:
            for y in ['enunciados', 'soluciones']:
                path = 'concursos' + x + '/%s/%s/'%(name, str(year)) + y + '/%s.tex'%(str(p))
                if not os.path.exists(path):
                    f = open(path, 'w')
                    f.write('')
                    f.close


        # Create html files
        path = 'ProyectoMURO/public_html/%s/%s/p%s.html'%(name, str(year), str(p))
        if not os.path.exists(path):
            f = open(path, 'w')
            f.write('')
            f.close
        path = 'ProyectoMURO/public_html/%s/%s/sol%s.html'%(name, str(year), str(p))
        if not os.path.exists(path):
            f = open(path, 'w')
            f.write('')
            f.close

NewContest('PAGMO', 2023)
