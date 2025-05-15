import os
import json
import base64
from glob import glob


class FileInterface:
    def __init__(self):
        os.chdir('files/')

    def list(self,params=[]):
        try:
            filelist = glob('*.*')
            return dict(status='OK',data=filelist)
        except Exception as e:
            return dict(status='ERROR',data=str(e))

    def hapus(self,params=[]):
        try:
            filename = params[0]
            if os.path.exists(filename):
                os.remove(filename)
                return dict(status='OK', data=f'{filename} berhasil dihapus')
            else:
                return dict(status='ERROR', data='File not found')
        except Exception as e:
             return dict(status='ERROR',data=str(e))  

    def upload(self, params=[]):
        try:
           filename = params[0]
           if os.path.exists(filename):
               return dict(status='OK', data=f'{filename} file sudah ada')
           filedata_64 = " ".join(params[1:])
           filedata = base64.b64encode(filedata_64.encode()).decode()

           with open(filename, 'w') as f:
               f.write(filedata)

           return dict(status='OK', data=f'File {filename} berhasil upload')
        
        except Exception as e:
           return dict(status='ERROR', data=str(e))    

    def get(self,params=[]):
        try:
            filename = params[0]
            if (filename == ''):
                return None
            fp = open(f"{filename}",'rb')
            isifile = base64.b64encode(fp.read()).decode()
            #fp = open(filename,'wb+')
            #fp.write(isifile)
            #fp.cloe()
            return dict(status='OK',data_namafile=filename,data_file=isifile)
        except Exception as e:
            return dict(status='ERROR',data=str(e))



if __name__=='__main__':
    f = FileInterface()
    print(f.list())
    print(f.get(['pokijan.jpg']))
