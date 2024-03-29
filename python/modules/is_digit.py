# Source: https://github.com/FunAndHelpfulDragon/python-Functions/


def is_digit(var: str):
    """Checks if var is a `real` number

    Args:
        var (str): The string to check

    Raises:
        AttributeError: If recieved None as the input

    Returns:
        bool: Is it a sutiable real number
    """

    # Skips the check if None is inputted
    if var is None:
        raise AttributeError("'NoneType' object has no attribute 'isdigit'")

    # returns true if interger
    if isinstance(var, int):
        return True

    var = str(var)  # make sure it's a string if the int check failed

    # Checks to see if negative or not
    try:
        # Removes negative
        var = var.replace("-", "")

        # gets where the decimal is
        decimal_location = False

        # 2 items on split
        if len(var.split(".")) == 2:
            decimal_location = var.index(".")

        # 1 item on split
        if len(var.split(".")) == 1:
            return var.isdigit()

        # Too many items on split (not 1 or 2)
        if decimal_location is False:
            print("Too many decimals found!")
            return False

        # Final thing to return (if contains decimal)
        var1 = var[:decimal_location].isdigit()
        decimal_location_1 = decimal_location + 1
        var2 = var[decimal_location_1:].isdigit()
        return var1 and var2
    except IndexError as i_e:  # if error, return false
        print(f"IndexError: {i_e}")
        return False
