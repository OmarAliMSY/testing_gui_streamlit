from utils.db_layout import *
from glob import glob


def get_unique_filename(name, date, data, i=0):
    filename = f"{name}{i}_{date}.{data}"
    if filename in glob(f"*.{str(data)}"):
        i += 1
        return get_unique_filename(name, date, data, i)  # Add 'return' to the recursive call
    return filename

def get_att(dbb_layout):
    """
    Process the database layout and extract attributes.

    Args:
    - dbb_layout: String representing the database layout.

    Returns:
    - Tuple containing two dictionaries:
        - db_dt: Dictionary mapping database numbers to their corresponding layout names.
        - db_dict: Dictionary mapping database numbers to their corresponding layout attributes.
    """
    item_list = [x.strip().split() for x in dbb_layout.split("\n") if x.strip()]
    db_dict = {int(float(row[0])): row[2] for row in item_list}
    db_dt = {row[0]: row[1] for row in item_list}
    param_datetype = {row[1]: row[2] for row in item_list}
    return db_dt, db_dict,param_datetype