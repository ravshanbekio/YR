from datetime import datetime, time, date, timedelta
from zoneinfo import ZoneInfo
from utils.db_query import create_arrival, check_attendance, create_leave

class AttendanceService:
    EARLY_TIME = time(5, 0)
    WORK_START = time(9, 0)
    WORK_END = time(18, 0)
    
    def __init__(self):
        self.rules = [
            (self.is_early_arrival, self.handle_early_arrival),
            (self.is_late_arrival, self.handle_late_arrival),
            (self.is_leave, self.handle_leave),
        ]
        
    async def process(self, chat_id: int, now=None):
        now = now or datetime.now(ZoneInfo("Asia/Tashkent")).time()
        for condition, action in self.rules:
            if await condition(now):
                await action(chat_id, now)
                
    # Conditions
    async def is_early_arrival(self, time):
        return self.EARLY_TIME <= time < self.WORK_START
    
    async def is_late_arrival(self, time):
        return self.WORK_START <= time < self.WORK_END
    
    async def is_leave(self, time):
        return self.WORK_END <= time
    
    # Actions
    async def handle_early_arrival(self, chat_id: int, time: time):
        attendance = await check_attendance(chat_id=chat_id, day=datetime.today().date())
        if not attendance:
            early_minutes = (self.WORK_START.hour * 60 + self.WORK_START.minute) - (time.hour * 60 + time.minute)
            await create_arrival(chat_id=chat_id, arrival_time=time, early_minutes=early_minutes)

    async def handle_late_arrival(self, chat_id: int, time: time):
        attendance = await check_attendance(chat_id=chat_id, day=datetime.today().date())
        if not attendance:
            delayed_minutes = (time.hour * 60 + time.minute) - (self.WORK_START.hour * 60 + self.WORK_START.minute)
            await create_arrival(chat_id=chat_id, arrival_time=time, late_minutes=delayed_minutes)
        
    async def handle_leave(self, chat_id: int, time: time):
        attendance = await check_attendance(chat_id=chat_id, day=datetime.today().date())
        if attendance:
            await create_leave(chat_id=chat_id, leave_time=time, day=datetime.today().date())


DUTY_LIST = [
    "@Millajanov",
    "@Akbarjon5669",
    "@Salarfer",
    "@sabr_lik",
    "@khakimov_yas",
    "@shokkirovfx",
    "@Inomjon77777",
    "@sherin_fergana",
    "@IDkozim",
    "@Sarafroz300",
    "@flutter_developer_boy",
    "@Prosecutor_1007",
    "@TM_SHerin"
]

START_DATE = date(2025, 11, 4)  # first Monday

def get_workday_index(start_date, today):
    """Count total working days (Mon–Sat, skip Sunday) since start_date."""
    days = 0
    current = start_date
    while current < today:
        if current.weekday() != 6:
            days += 1
        current += timedelta(days=1)
    return days

def get_tomorrow_duty(start_date: datetime.date):
    """Return tomorrow’s duty person name."""
    tomorrow = date.today() + timedelta(days=1)
    if tomorrow.weekday() == 6:
        return None  # Skip Sunday
    index = get_workday_index(start_date, tomorrow) % len(DUTY_LIST)
    return DUTY_LIST[index]