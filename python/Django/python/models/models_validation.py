import re

def is_name_valid(name: str) -> bool:
    """returns true if only alphabethic chars are found (excluding white space).

    - name can't start with space
    - name can't have have two consecutive spaces
    - names can't have a space between 2 individual alphabethic chars.
    """
    try:
        name.lstrip().rstrip()
        if len(name) >= 2:
            # if not alphabethic char or whitespace char found
            if bool(re.search(r'[^A-Za-z|\s]', name)) == False:
                # if name doesn't start with a single char followed by a space
                if bool(re.search(r'^[A-Za-z]{1}\s', name)) == False:
                    # if name doesn't start with space
                    if bool(re.search(r'\s{1,}[A-Za-z]{1}\s+', name)) == False:
                        # if name doesn't contain two consecutive spaces
                        if bool(re.search(r'\s{2,}', name)) == False:
                            return True
        return False
    except:
        return False


def is_password_valid(pw: str) -> bool:
    """ checks to see if a password conforms to the following guidelines:
        
    - length between 8 and 20 chars
    - password must have one of the following:
            - upper char
            - lower char,
            - digit.

    passwords can contain special chars that are within SPECIAL_CHARS string variable:
    - !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~ """
    try:
        SPECIAL_CHARS = "!\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"
        pw = pw.rstrip().lstrip()
        if (' ' in pw) == False:
            if len(pw) >= 8 and len(pw) <= 20:
                if pw.isascii():
                    # upper alpha char check
                    if bool(re.match(r'\w*[A-Z]\w*', pw)):
                        # lower alpha char check
                        if bool(re.match(r'\w*[a-z]\w*', pw)):
                            # digit check
                            if re.search(r'\d', pw) is not None:
                                # unpermitted char check
                                if special_char_checker(pw, SPECIAL_CHARS):
                                    return True              
        return False
    except:
        return False          


def special_char_checker(string, permitted_chars: str) -> bool:
    """function to test for special chars and whether they're permitted.
    
    returns True if no non-permittable chars are found, else False.

    permittable chars:
    - alphabethic
    - numeric
    - chars within permitted_chars"""
    try:
        for c in string:
            if c.isalpha() == False and c.isdigit() == False:
                if c not in permitted_chars:
                    return False
        return True
    except:
        return False


def is_email_address_valid(email: str, valid_domains:list= []) -> bool:
    """function to validate emails addresses """
    try:
        email_regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$' 
        if re.fullmatch(email_regex, email):
            if valid_domains:
                domain = email[email.rindex("@"):]
                if domain not in valid_domains: 
                    return False
            
            return True
    except:
        return False
    



