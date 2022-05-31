import pandas as pd
import numpy as np
import util.Data as data_util

def check_path(path, extension):
    if not path.exists() or path.suffix != extension:
        return False
    else:
        # print(path)
        return True
