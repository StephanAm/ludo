import ludomain
import os
# ludomain.main(('init',))
# ludomain.main(('list',))
# ludomain.main('status peterpan'.split())
# ludomain.main(('edit','peterpan'))
# ludomain.main(('status','peterpan'))

def create():
    ludomain.main(('create','scooter'))
def update():
    ludomain.main(('update','scooter','-w','dosbox','-v','1.0.0','-s','/home/Games/scooter.zip','-f',"Scooter's Magic Castle"))

def importResource():
    os.chdir('scooter')
    ludomain.main(('import','-f'))

# create()
# update()
importResource()