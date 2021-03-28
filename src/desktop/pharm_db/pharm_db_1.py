from pharm_model.pharm_model  import *

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
_category         = Pharm_Model_Category()
_category.name    = "biologie"
PHARM_CATEGORY_1 = _category

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
_question       = Pharm_Model_Question("Meteorologia este:")
_category.questions.append(_question)
_question.answers.append(Pharm_Model_Answer(True,  "stiinta care se ocupa cu studiul atmosferei si a fenomenelor din atmosfera"))
_question.answers.append(Pharm_Model_Answer(False, "disciplina care se ocupa cu studiul prognozei meteorologice"))
_question.answers.append(Pharm_Model_Answer(False, "stiinta care se ocupa cu predictia vremii"))

