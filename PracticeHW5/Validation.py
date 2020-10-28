
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
    
    @staticmethod
    def decorator_is_int(given_func):
        def int_validator(l_list, g_input):
            try:
                int(g_input)
                return given_func(l_list, int(g_input))
            except ValueError:
                print('Wrong input, not integer')
                return False
        return int_validator

    @staticmethod
    def decorator_position_delete(given_func):
        def pos_validator(l_list, g_input):
            if g_input < 0 or g_input >= len(l_list):
                print('Wrong input, no such element')
                return False
            else:
                return given_func(l_list, g_input)
        return pos_validator

    @staticmethod
    def decorator_position_insert(given_func):
        def pos_validator(l_list, g_input):
            if g_input < 0 or g_input > len(l_list):
                print('Wrong input, no such position')
                return False
            else:
                return given_func(l_list, g_input)
        return pos_validator

    @staticmethod
    def decorator_are_int(given_func):
        def int_validator(l_list, g_input1, g_input2):
            try:
                int(g_input1)
                int(g_input2)
                return given_func(l_list, int(g_input1), int(g_input2))
            except ValueError:
                print('Wrong input, not integers')
                return False
        return int_validator

    @staticmethod
    def decorator_positions_delete(given_func):
        def pos_validator(l_list, g_input1, g_input2):
            if g_input1 < 0 or g_input2 < 0 or g_input2 >= len(l_list) or g_input1 >= len(l_list):
                print('Wrong input, out of range')
            elif g_input1 > g_input2:
                print('Wrong input, cannot delete from larger position to smaller')
            else:
                return given_func(l_list, g_input1, g_input2)
            return False
        return pos_validator

    @staticmethod
    def decorator_context(given_func):
        def context_validator(obj, l_list, g_pos, g_param):
            try:
                pos = int(g_pos)
                if pos < 0 or pos > len(l_list):
                    print('Wrong input, no such position')
                    return False
                return given_func(obj, l_list, pos, g_param)
            except ValueError:
                print('Wrong input, position not integer')
                return False
        return context_validator

    @staticmethod
    def decorator_amount(given_func):
        def amount_validator(obj, l_list, g_pos, g_param):
            try:
                param = int(g_param)
                if param < 1:
                    print('Wrong input, amount has to be positive')
                    return False
                return given_func(obj, l_list, g_pos, param)
            except ValueError:
                print('Wrong input, amount not integer')
                return False
        return amount_validator

    @staticmethod
    def decorator_file(given_func):
        def file_validator(obj, l_list, g_pos, g_param):
            try:
                test = open(g_param, 'r')
                test.close()
                return given_func(obj, l_list, g_pos, g_param)
            except FileNotFoundError:
                print('Wrong input, no such file')
                return False
        return file_validator
