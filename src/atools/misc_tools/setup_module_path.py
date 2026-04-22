import sys
import inspect
from pathlib import Path


def setup_module_path():
    caller_frame = inspect.currentframe().f_back
    caller_file = caller_frame.f_code.co_filename
    project_root = Path(caller_file).parent.parent.resolve()
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
    return
