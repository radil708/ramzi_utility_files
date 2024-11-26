"""
Variety of classes of functions I use when playing around with python
or testing small programs.
Designed, Written, and Tested By Ramzi Reilly Adil.
"""

from os import listdir, path
from time import time
from datetime import datetime
from tkinter import filedialog

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
        print(get_time_elapsed_string()) #this will print lenght of time it took to run a function

        r_timer.reset_timer() #OPTIONAL, resets the timer if you want to use it again for a diff function
    """
    def __init__(self):
        self.start_time_epoch_sec = None
        self.end_time_epoch_sec = None
        self.start_datetime = None
        self.end_datetime = None
        self.seconds_in_a_day = 86400
        self.seconds_in_an_hour = 3600
        self.seconds_in_a_minute = 60

    def timer_start(self):
        """
        This function should be run right before running the function you want to time.
            Sets the start_time attribute to current time in value which is
            the number of seconds passed since epoch. May differ between os.
            For example, for Unix OS the epoch is January 1, 1970, 00:00:00 at UTC is epoch
        :return: @None
        """
        self.start_datetime = datetime.now()
        self.start_time_epoch_sec = time()

    def timer_end(self):
        """
        This function should be run right after running the function you want to time.
            Sets the end_time attribute to current time in value which is
            the number of seconds passed since epoch. May differ between os.
            For example, for Unix OS the epoch is January 1, 1970, 00:00:00 at UTC is epoch
        :return: @None
        """
        self.end_time_epoch_sec = time()
        self.end_datetime = datetime.now()

    def reset_timer(self):
        """
        Resets the attributes of this class. Optionally can be run.
        :return: @None
        """
        self.start_time_epoch_sec = None
        self.end_time_epoch_sec = None
        self.start_datetime = None
        self.end_datetime = None

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

        print_out_dict = {
            "Days": None,
            "Hours": None,
            "Minutes": None,
            "Seconds": None}

        time_left_to_calculate_in_sec = self.get_time_diff_epoch()

        ############################### Calculate Days elapsed ##################################
        elapsed_days_lst = divmod(time_left_to_calculate_in_sec, self.seconds_in_a_day)
        print_out_dict["Days"] = elapsed_days_lst[0]

        if elapsed_days_lst[0] == 0:
            time_left_to_calculate_in_sec = elapsed_days_lst[1]
        else:
            time_left_to_calculate_in_sec = time_left_to_calculate_in_sec - (
                        elapsed_days_lst[0] * self.seconds_in_a_day)

        ############################### Calculate Hours elapsed ##################################
        elapsed_hours_lst = divmod(time_left_to_calculate_in_sec, self.seconds_in_an_hour)
        print_out_dict["Hours"] = elapsed_hours_lst[0]

        if elapsed_hours_lst[0] == 0:
            time_left_to_calculate_in_sec = elapsed_hours_lst[1]
        else:
            time_left_to_calculate_in_sec = time_left_to_calculate_in_sec - (
                        elapsed_hours_lst[0] * self.seconds_in_an_hour)

        ############################### Calculate Minutes & Seconds elapsed ##################################
        elapsed_minutes_lst = divmod(time_left_to_calculate_in_sec, self.seconds_in_a_minute)
        print_out_dict["Minutes"] = elapsed_minutes_lst[0]

        if elapsed_minutes_lst == 0:
            time_left_to_calculate_in_sec = elapsed_minutes_lst[1]
        else:
            time_left_to_calculate_in_sec = time_left_to_calculate_in_sec - (
                        elapsed_minutes_lst[0] * self.seconds_in_a_minute)

        print_out_dict["Seconds"] = time_left_to_calculate_in_sec
        ############################### Calculate Seconds elapsed ##################################

        time_elapsed_lst = []

        for key, value in print_out_dict.items():
            if value != 0:
                time_elapsed_lst.append(f"{value} {key}")
            elif key == "Seconds" and value == 0:
                time_elapsed_lst.append("0 Seconds")

        return ','.join(time_elapsed_lst)

def get_all_filenames_from_directory(directory_path: str) -> list:
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


def fix_dir_strings(filepath_in: str) -> str:
    """
        Helper function to make the path correct by replace '/' with '\'
            idea is to use this to make filepaths taken from filedialog  easily useable
            for with open fxn.
        :param filepath_in: @str filepath to a directory
        :return: @str filepath where '/' is replaced by '\'
    """
    filepath = filepath_in
    return filepath.replace('/', '\\')


def user_select_directory() -> str:
    """
     Opens a window for user to select directory.
        Idea is to use this in conjuntion with get_all_filenames_from_directory fxn
        and fix_dir_strings fxn to have full filepaths to files from a user
        selected directory ready to go for use with the "with open" command
     :return: @str the full path to the directory with '/' replaced with '\\'
    """

    directory_path = filedialog.askdirectory()
    directory_path_edited = fix_dir_strings(directory_path)
    return directory_path_edited


def clear_line_new_print(print_string) -> None:
    """
    This function will clear the current line printed and then print a new line.
        Used to help make loading prints.
    :param print_string: @str string to print, generally will be in format of "X of N"
    :return: @None this prints to the terminal, it does not return a string
    """
    print('\r' + f"{print_string}", end='')



# Designed, Written, and Tested By Ramzi Reilly Adil.
