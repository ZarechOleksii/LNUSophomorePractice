
class Logger:
    file_name = 'Logs.txt'

    @staticmethod
    def changing_list_print(to_print):
        to_write = 'List before ' + to_print[3] + ': ' + str(to_print[0]) + '\n'
        to_write += to_print[3].capitalize() + ' position: ' + str(to_print[1]) + '\n'
        to_write += 'List after ' + to_print[3] + ': ' + str(to_print[2]) + '\n'
        to_write += '************************************************************************\n'
        writing = open(Logger.file_name, 'a')
        writing.write(to_write)
        writing.close()

    @staticmethod
    def main_list_method_print(to_print):
        to_write = 'List from: ' + str(to_print[0]) + '\n'
        to_write += 'List to: ' + str(to_print[1]) + '\n'
        to_write += 'Binary list: ' + str(to_print[2]) + '\n'
        to_write += 'Binary to decimal: ' + str(to_print[3]) + '\n'
        to_write += '************************************************************************\n'
        writing = open(Logger.file_name, 'a')
        writing.write(to_write)
        writing.close()
