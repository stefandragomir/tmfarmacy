import os
from PIL           import Image
from subprocess    import Popen
from subprocess    import PIPE
from subprocess    import STARTUPINFO
from subprocess    import STARTF_USESHOWWINDOW
from subprocess    import SW_HIDE

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
class Pharm_Digitize(object):

    def __init__(self,path_images,path_tesseract,extension=".jpg",rotate_angle=270):

        self.path_images    = path_images
        self.path_tesseract = path_tesseract
        self.extension      = extension
        self.rotate_angle   = rotate_angle

    def call(self,command,cwd="",log=True):

        _error = False
        _std_out = ""
        _std_err = ""

        startupinfo = STARTUPINFO()
        startupinfo.dwFlags |= STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = SW_HIDE


        _arguments = dict(
                            stdout      = PIPE,
                            stderr      = PIPE,
                            startupinfo = startupinfo,
                            )

        if cwd != "":
            _arguments.update({"cwd":cwd})
        try:
            _proc = Popen(command,**_arguments)
            _std_out, _std_err = _proc.communicate()
            _std_out =  _std_out.decode('utf8','ignore')   
            _std_err =  _std_err.decode('utf8','ignore') 
        except:
            _error = True  

        if log:
            print("--> %s" % (str(command),))
            print("--> %s" % (str(_std_out + _std_err),))

        return _error

    def ocr(self,path_image,path_output):

        _error = self.call(
                            r"%s  %s %s -l ron --oem 3 --dpi 72" % (
                                                            self.path_tesseract,
                                                            path_image,
                                                            path_output),
                            cwd=os.path.split(path_image)[0])

    def prepare_image(self,path_image,input_dir):

        _img        = Image.open(path_image)
        _rotate_img = _img.rotate(self.rotate_angle,expand=True)
        _path       = os.path.join(input_dir,os.path.split(path_image)[1])
        _rotate_img.save(_path)

        return _path

    def run(self):

        _files      = []
        _dir        = os.path.split(self.path_images)[0]
        _output_dir = os.path.join(_dir, "output")
        _input_dir  = os.path.join(_dir, "input")

        if not os.path.exists(_output_dir):

            os.mkdir(_output_dir)

        if not os.path.exists(_input_dir):

            os.mkdir(_input_dir)

        for _file in os.listdir(self.path_images):

            if os.path.splitext(_file)[1] == self.extension:

                _files.append(os.path.join(self.path_images,_file))

        for _file in _files:

            print("converting file %s to output %s" % (_file,_input_dir))

            _file_prep = self.prepare_image(_file,_input_dir)

            _output = os.path.join(_output_dir, "%s.txt" % (os.path.splitext(os.path.split(_file)[1])[0]))

            print("converting file %s to output %s" % (_file,_output))

            self.ocr(_file_prep,_output)

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
if __name__ == "__main__":

    _path_images    = r"d:\temp\raw"
    _path_tesseract = r"d:\toolbox\tesseract\tesseract.exe"

    Pharm_Digitize(_path_images,_path_tesseract).run()