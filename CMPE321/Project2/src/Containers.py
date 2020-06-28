from enum import Enum, auto
from pathlib import Path
from typing import NamedTuple, Optional, Set, List, Dict, Tuple
from Constraints import *

import attr
import cattr

class Type:
    name: str
    numberOfFields: int
    isDeleted: bool = False
    isExist: bool = True
    fieldNames: List[str]
    
class Record:
    name: str
    isDeleted: bool = False
    isExist: bool = True
    numberOfFields: int
    fieldValues: List[int]