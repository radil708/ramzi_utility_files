"""
Variety of classes of functions I use when playing around with python
or testing small programs.
Designed, Written, and Tested By Ramzi Reilly Adil.
"""

from os import listdir, path, rename
from time import time,ctime
from datetime import datetime
from tkinter import filedialog
from shutil import copy,move

class custom_exception(Exception):
    """
    Class used to make custom exceptions/errors. Place your custom error message in the parameter for
        constructor when instantiating a new custom_exception instance.
    """
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class ramzi_timer():
    """
        Timer class useful for testing time it takes to run a function.
        This does not help with calculating O(n), just actual physical run time of a function
        or functions. Time calculated for functions will vary on a machine machine basis.

        General Usage:
        r_timer = ramzi_timer()
        r_timer.start()
        
        function_to_test #replace this function with function you want to test

        r_timer.timer_end()
        print(get_time_elapsed_string()) #this will print length of time it took to run a function

        r_timer.reset_timer() #OPTIONAL, resets the timer if you want to use it again for a different function
    """
    def __init__(self):
        self.start_time_epoch_sec = None
        self.end_time_epoch_sec = None
        self.start_datetime = None
        self.end_datetime = None
        self.seconds_in_a_day = 86400
        self.seconds_in_an_hour = 3600
        self.seconds_in_a_minute = 60
        self.print_out_dict = {
            "Days": None,
            "Hours": None,
            "Minutes": None,
            "Seconds": None
        }

    def timer_start(self):
        """
        This function should be run right before running the function you want to time.
            Sets the start_time attribute to the current time; the value of which is
            the number of seconds passed since epoch. Epoch start time may differ between os.
            For example, for Unix OS the epoch is January 1, 1970, 00:00:00 at UTC is epoch
        :return: @None
        """
        self.start_datetime = datetime.now()
        self.start_time_epoch_sec = time()

    def timer_end(self):
        """
        This function should be run right after running the function you want to time.
            Sets the end_time attribute to current time;  the value of which is
            the number of seconds passed since epoch. May differ between os.
            For example, for Unix OS the epoch is January 1, 1970, 00:00:00 at UTC is epoch
        :return: @None
        """
        self.end_time_epoch_sec = time()
        self.end_datetime = datetime.now()

    def reset_timer(self):
        """
        Resets the attributes of this class. Must be run before running the
            ramzi_object a second time to time the subsequent function.
        :return: @None
        """
        self.start_time_epoch_sec = None
        self.end_time_epoch_sec = None
        self.start_datetime = None
        self.end_datetime = None
        self.print_out_dict = {
            "Days": None,
            "Hours": None,
            "Minutes": None,
            "Seconds": None
        }

    def check_attributes(self) -> None:
        """
        Used to raise an error before other functions are run
        :return: @None
        """
        if self.start_time_epoch_sec is None:
            raise Exception("ERROR: 'timer_start' function has not been run or not called after 'reset_timer' function")
        elif self.end_time_epoch_sec is None:
            raise Exception("ERROR: 'timer_end' function has not been run or not called after 'reset_timer' function")

    def get_time_diff_epoch(self) -> int:
        """
        Helper function to get_time_elapsed function
        :return: @float time difference in seconds between end_time_epoch_sec attribute
            and start_time_epoch_sec attribute in seconds.
        """
        self.check_attributes()
        return int(self.end_time_epoch_sec - self.start_time_epoch_sec)

    def get_time_elapsed_string(self) -> str:
        """
        Returns time elapsed in the representation of a string
            in the format of W days, X hours, Y Minutes, Z seconds
        :return: @str time elapsed in the format of in the format of W days, X hours, Y Minutes, Z seconds
        """
        self.check_attributes()

        time_left_to_calculate_in_sec = self.get_time_diff_epoch()

        ############################### Calculate Days elapsed ##################################
        elapsed_days_lst = divmod(time_left_to_calculate_in_sec, self.seconds_in_a_day)
        self.print_out_dict["Days"] = elapsed_days_lst[0]

        if elapsed_days_lst[0] == 0:
            time_left_to_calculate_in_sec = elapsed_days_lst[1]
        else:
            time_left_to_calculate_in_sec = time_left_to_calculate_in_sec - (
                        elapsed_days_lst[0] * self.seconds_in_a_day)

        ############################### Calculate Hours elapsed ##################################
        elapsed_hours_lst = divmod(time_left_to_calculate_in_sec, self.seconds_in_an_hour)
        self.print_out_dict["Hours"] = elapsed_hours_lst[0]

        if elapsed_hours_lst[0] == 0:
            time_left_to_calculate_in_sec = elapsed_hours_lst[1]
        else:
            time_left_to_calculate_in_sec = time_left_to_calculate_in_sec - (
                        elapsed_hours_lst[0] * self.seconds_in_an_hour)

        ############################### Calculate Minutes & Seconds elapsed ##################################
        elapsed_minutes_lst = divmod(time_left_to_calculate_in_sec, self.seconds_in_a_minute)
        self.print_out_dict["Minutes"] = elapsed_minutes_lst[0]

        if elapsed_minutes_lst == 0:
            time_left_to_calculate_in_sec = elapsed_minutes_lst[1]
        else:
            time_left_to_calculate_in_sec = time_left_to_calculate_in_sec - (
                        elapsed_minutes_lst[0] * self.seconds_in_a_minute)

        self.print_out_dict["Seconds"] = time_left_to_calculate_in_sec
        ############################### Get string representing time elapsed ##################################

        time_elapsed_lst = []

        for key, value in self.print_out_dict.items():
            if value != 0:
                time_elapsed_lst.append(f"{value} {key}")
            elif key == "Seconds" and value == 0:
                time_elapsed_lst.append("0 Seconds")

        return ','.join(time_elapsed_lst)

class ramzi_file_handler():
    """
    This class will contain shortcut functions relevant to obtaining file paths and other
        file "handling" related functions.
    """
    def get_all_filenames_from_directory(self,directory_path: str) -> list:
        """
        This function will return a list containing the filenames in a directory
            excluding other folders/directories
        :param directory_path: @str string representation of directory path where \\ should be
                                    ussed to separated inner folders
        :return: @list list of filenames
        """

        all_items = listdir(directory_path)
        all_files = [x for x in all_items if path.isfile(path.join(directory_path, x))]
        return all_files


    def fix_dir_strings(self,filepath_in: str) -> str:
        """
            Helper function to make the path correct by replace '/' with '\'
                idea is to use this to make filepaths taken from filedialog  easily useable
                for with open fxn.
            :param filepath_in: @str filepath to a directory
            :return: @str filepath where '/' is replaced by '\'
        """
        filepath = filepath_in
        return filepath.replace('/', '\\')


    def user_select_directory(self,window_title:str = 'Select A Directory') -> str:
        """
         Opens a window for user to select directory.
            Idea is to use this in conjunction with get_all_filenames_from_directory fxn
            and fix_dir_strings fxn to have full filepaths to files from a user
            selected directory ready to go for use with the "with open" command
         :param: @str the title that appears on the top bar of the window
                        - Default value is: 'Select A Directory'
         :return: @str the full path to the directory with '/' replaced with '\\'
        """

        directory_path = filedialog.askdirectory(title=window_title)
        directory_path_edited = self.fix_dir_strings(directory_path)
        return directory_path_edited

    def user_select_files(self, window_title: str = 'Select One Or More Files') -> list:
        """
            Opens a window for a user to select file(s). File(s) must all exist in the same directory.
                The "/" will be replaced with "\\" for easier use in conjunction with the
                with open command
            :param: @str the title that appears on the top bar of the window
                        - Default value is: 'Select One Or More Files'
            :return: @list the file paths of the files the user has selected
        """
        file_paths = filedialog.askopenfilenames(title=window_title)
        output_lst = []
        for each in file_paths:
            edited_path = self.fix_dir_strings(each)
            output_lst.append(edited_path)
        return output_lst

    def get_file_creation_timestamp(self,filepath: str) -> str:
        """
            Returns a string representing the date and time that a file was created
            :param filepath: @str the filepath to a file
            :return @str a timestamp with info regarding the creation date of a file
        """
        creation_time_epoch = path.getctime(filepath)
        creation_time_timestamp = ctime(creation_time_epoch)
        return creation_time_timestamp

    def get_file_creation_datetime(self,filepath: str) -> datetime:
        """
            Returns a datetime object representing the date and time that a file was created.
                This is useful for comparing file creation datetimes
            :param filepath: @str the filepath to a file
            :return @datetime a datetime with info regarding the creation date of a file
        """
        timestamp_str = self.get_file_creation_timestamp(filepath)
        creation_date_dt = datetime.strptime(timestamp_str, "%a %b %d %H:%M:%S %Y")
        return creation_date_dt

    def copy_file_to_new_destination(self,file_to_copy_filepath: str, new_destination_directory: str) -> None:
        """
            Makes a copy of a file. The file will be stored at a different destination.
                Will throw an error if the new destination is the same as the file to copy's
                current destination.
                Idea is to be able to use this in conjunction with user_select fxn's
            :param file_to_copy_filepath: @str the filepath to the file you want to copy
            :param new_destination_directory: @str the path to the directory where you want to copy the file
            :return @None
        """
        if not path.isfile(file_to_copy_filepath):
            not_a_file_exception = custom_exception(f"Error: {file_to_copy_filepath} does NOT represent a file, please check that file_to_copy_filepath is not a directory")
            raise not_a_file_exception
        elif not path.isdir(new_destination_directory):
            not_a_directory_exception = custom_exception(f"Error: {new_destination_directory} does NOT represent a directory, please check that new_destination_directory is NOT a file. ")
            raise not_a_directory_exception

        filename = file_to_copy_filepath.split("\\")[-1]
        filepath_of_copy = new_destination_directory + '\\' + filename

        copy(file_to_copy_filepath, filepath_of_copy) #already has built in sameFileError so no need to make that

    def move_file_to_new_destination(self,file_to_move_filepath: str, new_destination_directory: str) -> None:
        """
            Moves a file from one directory to another. Pretty much the same as move from shutil library, but
                I personally think the name of this fxn is more clear.
            :param file_to_move_filepath: @str the filepath to the file you want to move
            :param new_destination_directory: @str the path to the directory where you want to move the file to
            :return @None
        """
        if not path.isfile(file_to_move_filepath):
            not_a_file_exception = custom_exception(f"Error: {file_to_move_filepath} does NOT represent a file, please check that file_to_move_filepath is not a directory")
            raise not_a_file_exception
        elif not path.isdir(new_destination_directory):
            not_a_directory_exception = custom_exception(f"Error: {new_destination_directory} does NOT represent a directory, please check that new_destination_directory is NOT a file. ")
            raise not_a_directory_exception

        move(file_to_move_filepath,new_destination_directory)

    def rename_file(self,file_to_rename_filepath: str,new_file_name: str) -> None:
        """
            Renames a file. More helpful than rename from os because it will maintain the extension
                of a file during the rename process.
            :param file_to_rename_filepath: @str the filepath to the file you want to rename
            :param new_file_name: @str the new name of the file
            :return @None
        """
        if not path.isfile(file_to_rename_filepath):
            not_a_file_exception = custom_exception(f"Error: {file_to_rename_filepath} does NOT represent a file, please check that file_to_rename_filepath is not a directory")
            raise not_a_file_exception

        current_directory_list = file_to_rename_filepath.split("\\")
        filename = current_directory_list.pop() #remove old filename retain elements pointing to directory

        filename_extensions_list = filename.split('.') #some extensions consist of multiple dots tike .tar.gz
        filename_extensions_list.pop(0) #remove old name, keep extensions
        file_extension = '.'.join(filename_extensions_list)

        current_directory_filepath = '\\'.join(current_directory_list)
        new_file_path = current_directory_filepath + '\\' + new_file_name + '.' + file_extension #need this to keep file extension in name

        rename(file_to_rename_filepath,new_file_path)

def clear_line_new_print(print_string) -> None:
    """
    This function will clear the current line printed and then print a new line.
        Used to help make loading prints to terminal.
    :param print_string: @str string to print, generally will be in format of "X of N"
    :return: @None this prints to the terminal, it does not return a string
    """
    print('\r' + f"{print_string}", end='')

def print_list(list_in: list, print_with_numbers: bool = False) -> None:
    """
    Prints each element in a list on a new line on the terminal.
        Optionally will add numbering sequence.
    :param list_in @list the list containing elements you want to print to the terminal
    :param print_with_numbers @bool If True, will print with a number sequence prior to printing the element
                                    Optional parameter, set to False by default
    :return: @None
    """
    for i in range(len(list_in)):
        print_statement = list_in[i]

        if print_with_numbers is True:
            print_statement = f"{i+1}.) {print_statement}"

        print(print_statement)

def print_dict(dict_in: dict,print_with_numbers: bool = False) -> None:
    """
    Prints out each key, value pair in a new line on the terminal.
        Optionally will add numbering sequence.
    :param dict_in @dict the dictionary containing key value pairs you want to print to the terminal
    :param print_with_numbers @bool If True, will print with a number sequence prior to printing the element
                                    Optional parameter, set to False by default
    :return: @None
    """
    counter = 1

    for k,v in dict_in.items():
        print_statement = f"KEY:{k}\tVALUE:{v}"

        if print_with_numbers is True:
            print_statement = f"{counter}.) " + print_statement

        counter += 1

# Designed, Written, and Tested By Ramzi Reilly Adil.
