from copy import copy
import logging
import sys
from typing import Literal, Optional, Tuple, Union
import click
from config.config import settings

LEVEL_DATA = logging.INFO + 1
LEVEL_SUCCESS = logging.INFO + 2

class FormatColor(logging.Formatter):
    level_name_colors = { # type: ignore
        LEVEL_DATA: lambda level_name: click.style(str(level_name), fg="blue"), # type: ignore
        LEVEL_SUCCESS: lambda level_name: click.style(str(level_name), fg="magenta"), # type: ignore
        logging.DEBUG: lambda level_name: click.style(str(level_name), fg="cyan"), # type: ignore
        logging.INFO: lambda level_name: click.style(str(level_name), fg="green"), # type: ignore
        logging.WARNING: lambda level_name: click.style(str(level_name), fg="yellow"), # type: ignore
        logging.ERROR: lambda level_name: click.style(str(level_name), fg="red"), # type: ignore
        logging.CRITICAL: lambda level_name: click.style(str(level_name), fg="bright_red"), # type: ignore
    }

    def __init__(
        self,
        fmt: Optional[str] = None,
        datefmt: Optional[str] = None,
        style: Literal["%", "{", "$"] = "%", # loggin._STYLES
        use_colors: Optional[bool] = True,
    ):
        if use_colors in (True, False):
            self.use_colors = use_colors
        else:
            self.use_colors = sys.stdout.isatty()
        super().__init__(fmt=fmt, datefmt=datefmt, style=style)

    def color_level_name(self, level_name: str, level_no: int) -> str:
        def default(level_name: str) -> str:
            return str(level_name)

        func = self.level_name_colors.get(level_no, default) # type: ignore
        return func(level_name)

    def should_use_colors(self) -> bool:
        return True

    def formatMessage(self, record: logging.LogRecord) -> str:
        recordcopy = copy(record)
        levelname = recordcopy.levelname
        pad = " " * (8 - len(recordcopy.levelname))
        if self.use_colors:
            levelname = self.color_level_name(levelname, recordcopy.levelno)
            if "color_message" in recordcopy.__dict__:
                recordcopy.msg = recordcopy.__dict__["color_message"]
                recordcopy.__dict__["message"] = recordcopy.getMessage()

        recordcopy.levelname = levelname + ":" + pad
        return super().formatMessage(recordcopy)

class MSLoggerClass:
    def __init__(self) -> None:
        self.logger = logging.getLogger("msINFO")
        self.logger.setLevel(logging.DEBUG)
        self.use_colors=settings.project.logging_use_colors

        __streamHandlerInfo = logging.StreamHandler()
        __streamHandlerInfo.setLevel(logging.DEBUG)
        __formater_info = FormatColor(
            '%(levelname)s %(asctime)s %(message)s',
            use_colors=self.use_colors
        )
        __streamHandlerInfo.setFormatter(__formater_info)
        self.logger.addHandler(__streamHandlerInfo)
        self.logger.propagate = False

    def info(
        self,
        msg: str,
        *,
        foreground: Optional[Union[int, Tuple[int, int, int], str]] = None,
        background: Optional[Union[int, Tuple[int, int, int], str]] = None,
        bold: bool = False,
        underline: bool = False,
        italic: bool = False
    ):
        if self.use_colors:
            s = "{}".format(click.style(msg, fg=foreground, bg=background, bold=bold, underline=underline, italic=italic))
        else:
            s = msg
        self.logger.info(s, extra={"color_message": s})

    def data(
        self,
        msg: str,
        *,
        foreground: Optional[Union[int, Tuple[int, int, int], str]] = "bright_blue",
        background: Optional[Union[int, Tuple[int, int, int], str]] = None,
        bold: bool = False,
        underline: bool = False,
        italic: bool = False
    ):
        if self.use_colors:
            s = "{}".format(click.style(msg, fg=foreground, bg=background, bold=bold, underline=underline, italic=italic))
        else:
            s = msg
        self.logger.log(LEVEL_DATA, s, extra={"color_message": s})

    def success(
        self,
        msg: str,
        *,
        foreground: Optional[Union[int, Tuple[int, int, int], str]] = "green",
        background: Optional[Union[int, Tuple[int, int, int], str]] = None,
        bold: bool = False,
        underline: bool = False,
        italic: bool = False
    ):
        if self.use_colors:
            s = "{}".format(click.style(msg, fg=foreground, bg=background, bold=bold, underline=underline, italic=italic))
        else:
            s = msg
        self.logger.log(LEVEL_SUCCESS, s, extra={"color_message": s})

    def warning(
        self,
        msg: str,
        *,
        foreground: Optional[Union[int, Tuple[int, int, int], str]] = "yellow",
        background: Optional[Union[int, Tuple[int, int, int], str]] = None,
        bold: bool = False,
        underline: bool = False,
        italic: bool = False
    ):
        if self.use_colors:
            s = "{}".format(click.style(msg, fg=foreground, bg=background, bold=bold, underline=underline, italic=italic))
        else:
            s = msg
        self.logger.warning(s, extra={"color_message": s})

    def debug(
        self,
        msg: str,
        *,
        foreground: Optional[Union[int, Tuple[int, int, int], str]] = "bright_blue",
        background: Optional[Union[int, Tuple[int, int, int], str]] = None,
        bold: bool = False,
        underline: bool = False,
        italic: bool = False
    ):
        if self.use_colors:
            s = "{}".format(click.style(msg, fg=foreground, bg=background, bold=bold, underline=underline, italic=italic))
        else:
            s = msg
        self.logger.debug(s, extra={"color_message": s})

    def error(
        self,
        msg: str,
        exc: BaseException | None = None,
        stack_info: bool = False,
        stacklevel: int = 3,
        *,
        foreground: Optional[Union[int, Tuple[int, int, int], str]] = "bright_red",
        background: Optional[Union[int, Tuple[int, int, int], str]] = None,
        bold: bool = False,
        underline: bool = False,
        italic: bool = False
    ):
        if self.use_colors:
            s = "{}".format(click.style(msg, fg=foreground, bg=background, bold=bold, underline=underline, italic=italic))
        else:
            s = msg
        if exc is not None:
            self.logger.error(s, exc_info=exc, stack_info=stack_info, stacklevel=stacklevel, extra={"color_message": s})
        else:
            self.logger.error(s, extra={"color_message": s})

    def critical(
        self,
        msg: str,
        exc: BaseException | None = None,
        stack_info: bool = False,
        stacklevel: int = 3,
        *,
        foreground: Optional[Union[int, Tuple[int, int, int], str]] = "red",
        background: Optional[Union[int, Tuple[int, int, int], str]] = None,
        bold: bool = False,
        underline: bool = False,
        italic: bool = False
    ):
        if self.use_colors:
            s = "{}".format(click.style(msg, fg=foreground, bg=background, bold=bold, underline=underline, italic=italic))
        else:
            s = msg
        if exc is not None:
            self.logger.critical(s, exc_info=exc, stack_info=stack_info, stacklevel=stacklevel, extra={"color_message": s})
        else:
            self.logger.critical(s, extra={"color_message": s})
            
    def exception(
        self,
        msg: str,
        exc: BaseException | None = None,
        stack_info: bool = False,
        stacklevel: int = 3,
        *,
        foreground: Optional[Union[int, Tuple[int, int, int], str]] = "red",
        background: Optional[Union[int, Tuple[int, int, int], str]] = None,
        bold: bool = False,
        underline: bool = False,
        italic: bool = False
    ):
        if self.use_colors:
            s = "{}".format(click.style(msg, fg=foreground, bg=background, bold=bold, underline=underline, italic=italic))
        else:
            s = msg
        if exc is not None:
            self.logger.exception(s, exc_info=exc, stack_info=stack_info, stacklevel=stacklevel)
        else:
            self.logger.exception(s, stacklevel=stacklevel)

logging.addLevelName(LEVEL_DATA, "DATA")
logging.addLevelName(LEVEL_SUCCESS, "SUCCESS")

msLogger = MSLoggerClass()