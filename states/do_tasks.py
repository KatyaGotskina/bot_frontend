from aiogram.fsm.state import State, StatesGroup


class TaskState(StatesGroup):
    task_worker = State()
    enter_task_name = State()
    conflict_task = State()
