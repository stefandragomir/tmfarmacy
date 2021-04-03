import os
import re
import cv2
import io
from subprocess    import Popen
from subprocess    import PIPE
from subprocess    import STARTUPINFO
from subprocess    import STARTF_USESHOWWINDOW
from subprocess    import SW_HIDE
from pprint        import pprint

OCR_DPI = 72

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
MODEL_TEMPLATE = '''
_question       = Pharm_Model_Question("%s")
_category.questions.append(_question)
_question.answers.append(Pharm_Model_Answer(False, "%s"))
_question.answers.append(Pharm_Model_Answer(False, "%s"))
_question.answers.append(Pharm_Model_Answer(False, "%s"))
_question.answers.append(Pharm_Model_Answer(False, "%s"))
_question.answers.append(Pharm_Model_Answer(False, "%s"))
'''

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
class Pharm_Digitize(object):

    def __init__(self,path_images,path_tesseract,extension=".jpg",th=100):

        self.path_images    = path_images
        self.path_tesseract = path_tesseract
        self.extension      = extension
        self.th             = th

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
                            r"%s  %s %s -l ron --oem 3 --dpi %s" % (
                                                            self.path_tesseract,
                                                            path_image,
                                                            path_output,
                                                            OCR_DPI),
                            cwd=os.path.split(path_image)[0])

    def prepare_image(self,path_image,input_dir):

        _img           = cv2.imread(path_image, 2)
        _ret, _bin_img = cv2.threshold(_img, self.th, 255, cv2.THRESH_BINARY)
        _path          = os.path.join(input_dir,os.path.split(path_image)[1])
        cv2.imwrite(_path, _bin_img) 

        return _path

    def image_to_text_file(self,input_path,output_path):

        _text_files = []

        for _file in os.listdir(self.path_images):

            if os.path.splitext(_file)[1] == self.extension:

                _file = os.path.join(self.path_images,_file)

                print("converting file %s to output %s" % (_file,input_path))

                _file_prep = self.prepare_image(_file,input_path)

                _output = os.path.join(output_path, "%s" % (os.path.splitext(os.path.split(_file)[1])[0]))

                print("converting file %s to output %s" % (_file,_output))

                self.ocr(_file_prep,_output)

                _text_files.append(_output)

        return _text_files

    def get_text_lines(self,file):

        _data = ""

        with io.open("%s.txt" % (file,),'r',encoding='utf-8') as _file:

            _data = _file.read()

        _lines = [_line.strip() for _line in _data.split("\n") if _line.strip() != ""]

        return _lines

    def is_answer_a(self,text):

        return None != re.match(r"^A\.\s.+$",text)

    def is_answer_b(self,text):

        return None != re.match(r"^B\.\s.+$",text)

    def is_answer_c(self,text):

        return None != re.match(r"^C\.\s.+$",text)

    def is_answer_d(self,text):

        return None != re.match(r"^D\.\s.+$",text)

    def is_answer_e(self,text):

        return None != re.match(r"^E\.\s.+$",text)

    def is_answer(self,text):

        return self.is_answer_a(text) or self.is_answer_b(text) or self.is_answer_c(text) or self.is_answer_d(text) or self.is_answer_e(text)

    def text_files_to_model_text(self,text_files):

        _STATE_QUESTION = 1
        _STATE_ANSWER_A = 2
        _STATE_ANSWER_B = 3
        _STATE_ANSWER_C = 4
        _STATE_ANSWER_D = 5
        _STATE_ANSWER_E = 6

        _model_text = ""

        for _text_file in text_files:

            _lines = self.get_text_lines(_text_file)

            _state          = _STATE_QUESTION
            _text_question  = ""
            _text_answer_a  = ""
            _text_answer_b  = ""
            _text_answer_c  = ""
            _text_answer_d  = ""
            _text_answer_e  = ""

            for _line in _lines:

                if _state == _STATE_QUESTION:

                    if self.is_answer(_line):
                        if self.is_answer_a(_line):
                            _text_answer_a += _line
                            _state          = _STATE_ANSWER_A
                        else:
                            print("error: expecting question or answer a got other answer [%s]" % (_line,))
                    else:
                        _text_question += _line

                elif _state == _STATE_ANSWER_A:

                    if self.is_answer(_line):
                        if self.is_answer_b(_line):
                            _text_answer_b += _line
                            _state          = _STATE_ANSWER_B
                        else:
                            print("error: expecting answer a or b got other answer [%s]" % (_line,))
                    else:
                        _text_answer_a += _line

                elif _state == _STATE_ANSWER_B:

                    if self.is_answer(_line):
                        if self.is_answer_c(_line):
                            _text_answer_c += _line
                            _state          = _STATE_ANSWER_C
                        else:
                            print("error: expecting answer b or c got other answer [%s]" % (_line,))
                    else:
                        _text_answer_b += _line

                elif _state == _STATE_ANSWER_C:

                    if self.is_answer(_line):
                        if self.is_answer_d(_line):
                            _text_answer_d += _line
                            _state          = _STATE_ANSWER_D
                        else:
                            print("error: expecting answer c or d got other answer [%s]" % (_line,))
                    else:
                        _text_answer_c += _line

                elif _state == _STATE_ANSWER_D:

                    if self.is_answer(_line):
                        if self.is_answer_e(_line):
                            _text_answer_e += _line
                            _state          = _STATE_ANSWER_E
                        else:
                            print("error: expecting answer d or e got other answer [%s]" % (_line,))
                    else:
                        _text_answer_e += _line

                elif _state == _STATE_ANSWER_E:

                    _state = _STATE_QUESTION

                    print("QUESTION -> [%s]" % (_text_question))
                    print("       A -> [%s]" % (_text_answer_a))
                    print("       B -> [%s]" % (_text_answer_b))
                    print("       C -> [%s]" % (_text_answer_c))
                    print("       D -> [%s]" % (_text_answer_d))
                    print("       E -> [%s]" % (_text_answer_e))
                    print("-------------------------------------------")

                    _model_text += MODEL_TEMPLATE % (   _text_question,
                                                        _text_answer_a,
                                                        _text_answer_b,
                                                        _text_answer_c,
                                                        _text_answer_d,
                                                        _text_answer_e )

                    _text_question  = _line
                    _text_answer_a  = ""
                    _text_answer_b  = ""
                    _text_answer_c  = ""
                    _text_answer_d  = ""
                    _text_answer_e  = ""

        return _model_text

    def run(self):
        
        _dir        = os.path.split(self.path_images)[0]
        _output_dir = os.path.join(_dir, "output")
        _db_dir     = os.path.join(_dir, "db")
        _input_dir  = os.path.join(_dir, "input")

        if not os.path.exists(_output_dir):

            os.mkdir(_output_dir)

        if not os.path.exists(_input_dir):

            os.mkdir(_input_dir)

        if not os.path.exists(_db_dir):

            os.mkdir(_db_dir)

        _text_files = self.image_to_text_file(_input_dir,_output_dir)

        _model_text = self.text_files_to_model_text(_text_files)

        with io.open(os.path.join(_db_dir,"db.py"),'w+',encoding='utf-8') as _db:

            _db.write(_model_text)

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
if __name__ == "__main__":

    _path_images    = r"d:\temp\raw"
    _path_tesseract = r"d:\toolbox\tesseract\tesseract.exe"

    Pharm_Digitize(_path_images,_path_tesseract,th=150).run()