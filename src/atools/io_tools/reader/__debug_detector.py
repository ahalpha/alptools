import sys


class DebugDetector:
    _debugger_present = None

    @classmethod
    def is_hover_eval(cls) -> bool:
        if not cls.__is_debugger_present():
            return False
        return cls.__check_eval_frame()

    @classmethod
    def __is_debugger_present(cls) -> bool:
        if cls._debugger_present is None:
            cls._debugger_present = any(mod in sys.modules for mod in ("debugpy", "pydevd", "_pydevd_bundle"))
        return cls._debugger_present

    @staticmethod
    def __check_eval_frame() -> bool:
        try:
            frame = sys._getframe(1)
            while frame is not None:
                filename = frame.f_code.co_filename
                if "pydevd_resolver" in filename:
                    return True
                if "pydevd_comm" in filename and "get_variable" in frame.f_code.co_name:
                    return True
                frame = frame.f_back
        except (ValueError, AttributeError):
            pass
        return False
