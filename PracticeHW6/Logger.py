
class Logger:
    file_name = 'Logs.txt'

    @staticmethod
    def adding_to_list_print(to_print):
        writing = open(Logger.file_name, 'a')
        writing.write('List before addition: ' + str(to_print[0]) + '\n')
        writing.write('Adding position: ' + str(to_print[1]) + '\n')
        writing.write('List after addition: ' + str(to_print[2]) + '\n')
        writing.write('************************************************************************\n')
        writing.close()

    @staticmethod
    def deleting_from_list_print(to_print):
        writing = open(Logger.file_name, 'a')
        writing.write('List before deletion: ' + str(to_print[0]) + '\n')
        writing.write('Deleting position(s): ' + str(to_print[1]) + '\n')
        writing.write('List after addition: ' + str(to_print[2]) + '\n')
        writing.write('************************************************************************\n')
        writing.close()

    @staticmethod
    def main_list_method_print(to_print):
        writing = open(Logger.file_name, 'a')
        writing.write('List 1: ' + str(to_print[0]) + '\n')
        writing.write('List 2: ' + str(to_print[1]) + '\n')
        writing.write('Binary list: ' + str(to_print[2]) + '\n')
        writing.write('Binary to decimal: ' + str(to_print[3]) + '\n')
        writing.write('************************************************************************\n')
        writing.close()
