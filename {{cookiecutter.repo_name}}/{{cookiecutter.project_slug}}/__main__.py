from .io import atomic_write, get_full_path
from .hash_str import get_csci_salt, get_user_id, hash_str
import pandas as pd


def get_user_hash(username, salt=None):  # pragma: no cover
    """

    :param username: str
    :param salt: str
    :return:
    """
    salt = salt or get_csci_salt()
    return hash_str(username, salt=salt)


def excel_to_parquet(source_file, destination_file):
    """
    Function to write a .parquest file with the same name in the same location.

    :param source_file: str, path to the source .xlsx file.
    :param destination_file: str, path to the destination .parquet file.
    :return: None
    """
    df = pd.DataFrame(pd.read_excel(source_file))
    with atomic_write(destination_file, "w", False) as f:
        df.to_parquet(f)


def print_column_from_parquet(filename, column):
    """
    Function to read data from the .parquet file and print it out.

    :param filename: str, path of the file to be read.
    :param column: str, the column in the .parquet file that needs to be read.
    :return: None
    """
    print(pd.read_parquet(filename)[column])


if __name__ == "__main__":  # pragma: no cover

    for user in ["gorlins", "doctorsmonsters"]:
        print("Id for {}: {}".format(user, get_user_id(user)))

    data_source = "data/hashed.xlsx"
    data_destination = get_full_path(data_source)
    excel_to_parquet(data_source, data_destination)
    print_column_from_parquet(data_destination, "hashed_id")
