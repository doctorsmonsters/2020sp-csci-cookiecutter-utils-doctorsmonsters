import os
from contextlib import contextmanager
from typing import ContextManager, Union
import tempfile as tmp


@contextmanager
def atomic_write(
    file: Union[str, os.PathLike], mode: str = "w", as_file: bool = True, **kwargs
) -> ContextManager:
    """ Open temporary file object that atomically moves to destination upon
    exiting.

    Allows reading and writing to and from the same filename.

    The file will not be moved to destination in case of an exception.

    Parameters
    ----------

    """

    with tempfile() as tmppath:
        if as_file:
            with open(tmppath, mode) as f:
                try:
                    yield f
                finally:
                    f.close()
            try:
                os.rename(tmppath, file)
            except:
                raise FileExistsError(
                    "File with the same name exists already, please choose a different name."
                )
        else:
            try:
                yield tmppath
            finally:
                os.rename(tmppath, file)


@contextmanager
def tempfile(suffix="", dir=None):
    """ Context for temporary file.

    Will find a free temporary filename upon entering
    and will try to delete the file on leaving, even in case of an exception.

    Parameters
    ----------
    suffix : string
        optional file suffix
    dir : string
        optional directory to save temporary file in
    """

    tf = tmp.NamedTemporaryFile(delete=False, suffix=suffix, dir=dir)
    tf.file.close()
    try:
        yield tf.name
    finally:
        try:
            os.remove(tf.name)
        except OSError as e:
            if e.errno == 2:
                pass
            else:
                raise


def get_full_path(source_filename):
    path = os.path.dirname(os.path.realpath(source_filename))
    dist_filename = (
        os.path.splitext(os.path.basename(os.path.abspath(source_filename)))[0]
        + ".parquet"
    )
    return path + "\\" + dist_filename
