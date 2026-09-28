from datetime import datetime

from anthropic.types import ToolParam


def get_current_datetime(date_format="%Y-%m-%d %H:%M:%S"):
    if not date_format:
        raise ValueError("date_format cannot be empty")
    return datetime.now().strftime(date_format)


get_current_datetime_schema = ToolParam(
    {
        "name": "get_current_datetime",
        "description": "Returns the current date and time as a formatted string. Use this whenever the answer depends on the present moment: today's date, the current time, the day of the week, or calculating how long until or since an event. The value comes from the system clock of the machine running the tool and reflects its local timezone. The result carries no timezone information unless the format string asks for it (%Z or %z). The output format is controlled by a Python strftime format string. If no format is given, it returns 'YYYY-MM-DD HH:MM:SS' (e.g. '2026-09-27 14:40:05'). An empty format string is rejected with an error.",
        "input_schema": {
            "type": "object",
            "properties": {
                "date_format": {
                    "type": "string",
                    "description": "A Python strftime format string that controls the output. Common directives: %Y (4-digit year), %m (month 01-12), %d (day 01-31), %H (hour 00-23), %I (hour 01-12), %M (minute), %S (second), %p (AM/PM), %A (full weekday name), %B (full month name), %Z (timezone name), %z (UTC offset). Examples: '%Y-%m-%d' gives '2026-09-27'; '%A, %B %d, %Y' gives 'Sunday, September 27, 2026'; '%I:%M %p' gives '02:40 PM'. Must not be empty. Omit it to use the default.",
                    "default": "%Y-%m-%d %H:%M:%S",
                    "minLength": 1,
                }
            },
            "required": [],
        },
    }
)
