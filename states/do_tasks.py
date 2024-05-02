from aiogram.fsm.state import State, StatesGroup


class TaskState(StatesGroup):
    enter_task_name = State()
