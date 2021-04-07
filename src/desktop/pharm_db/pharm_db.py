from pharm_model.pharm_model  import *
from pharm_db.pharm_db_1      import PHARM_CATEGORY_1
from pharm_db.pharm_db_2      import PHARM_CATEGORY_2
from pharm_db.pharm_db_3      import PHARM_CATEGORY_3

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
PHARM_CATEGORY_0         = Pharm_Model_Category()
PHARM_CATEGORY_0.name    = "biologie"

PHARM_CATEGORY_0.questions += PHARM_CATEGORY_1.questions
PHARM_CATEGORY_0.questions += PHARM_CATEGORY_2.questions
PHARM_CATEGORY_0.questions += PHARM_CATEGORY_3.questions

PHARM_DB = [
				PHARM_CATEGORY_0,
				PHARM_CATEGORY_1,
				PHARM_CATEGORY_2,
				PHARM_CATEGORY_3,
			]