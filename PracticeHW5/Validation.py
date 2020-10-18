
class Validation:
    @staticmethod
    def is_int(given):
        try:
            int(given)
            return True
        except ValueError:
            return False

    @staticmethod
    def validate_file(name):
        try:
            val_file = open(name, 'r')
            val_file.close()
            return True
        except FileNotFoundError:
            return False

    @staticmethod
    def validate_position(pos, l_list):
        if pos < 0 or pos > len(l_list):
            return False
        else:
            return True

    @staticmethod
    def validate_from_to(pos_from, pos_to, l_list):
        if Validation.validate_position(pos_from, l_list) and Validation.validate_position(pos_to, l_list):
            if pos_from < pos_to:
                return True
        return False

