from .enums import Timespan

timespan_map: dict[str, int] = {
    Timespan.DAY: 1,
    Timespan.WEEK: 7,
    Timespan.MONTH: 30,
    Timespan.YEAR: 365
}
