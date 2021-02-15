
class Logger:
    file_name = 'Logs.txt'

    @staticmethod
    def changing_list_print(to_print):
        writing = open(Logger.file_name, 'a')
        writing.write('List before ' + to_print[3] + ': ' + str(to_print[0]) + '\n')
        writing.write(to_print[3].capitalize() + ' position: ' + str(to_print[1]) + '\n')
        writing.write('List after ' + to_print[3] + ': ' + str(to_print[2]) + '\n')
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
