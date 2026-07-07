import logging
from datetime import datetime as _datetime


class LoggerFormatter(logging.Formatter):
    _datetime = _datetime
    COLORS = {
        logging.DEBUG: "\033[0m",
        logging.INFO: "\033[32m",
        logging.WARNING: "\033[33m",
        logging.ERROR: "\033[31m",
        logging.CRITICAL: "\033[31m",
    }
    LEVEL_NAMES = {
        logging.DEBUG: "DBG",
        logging.INFO: "INF",
        logging.WARNING: "WRN",
        logging.ERROR: "ERR",
        logging.CRITICAL: "CRT",
    }

    def format(self, record):
        try:
            now = self._datetime.fromtimestamp(record.created)
            time_text = f"[\033[90m" f"{now.strftime('%Y-%m-%d %H:%M:%S')}.{int(record.msecs):03d}" f"\033[0m]"
            color = self.COLORS.get(record.levelno, "\033[0m")
            level_name = self.LEVEL_NAMES.get(record.levelno, record.levelname)
            if record.levelno == logging.DEBUG:
                typ = f"[{level_name}]"
            else:
                typ = f"{color}[{level_name}]\033[0m"
            message = record.getMessage()
            log_text = f" {time_text} {typ} {message}"
            if record.exc_info:
                log_text += "\n" + self.formatException(record.exc_info)
            if record.stack_info:
                log_text += "\n" + self.formatStack(record.stack_info)
            return log_text
        except Exception:
            try:
                return record.getMessage()
            except Exception:
                return "<logging format error>"


def setup_logger_style(level: logging._Level = logging.INFO):
    handler = logging.StreamHandler()
    handler.setFormatter(LoggerFormatter())
    logging.basicConfig(handlers=[handler], force=True, level=level)
