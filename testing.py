from enum import Enum
from datetime import date
class Weekday(Enum):
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 7
    FRIDAY = 5
    SATURDAY = 6
    SUNDAY = 4
    @classmethod
    def today(cls):
        print('today is %s' % cls(date.today().isoweekday()).name)

print(dir(Weekday.SATURDAY))
print(Weekday.SATURDAY.name)
print(Weekday.__call__('SUNDAY'))
print(Weekday.__getitem__('SUNDAY'))
