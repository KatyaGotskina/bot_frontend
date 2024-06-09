from bot_frontend.core.buttons import during_the_task_keyboard, get_main_keyboard
from bot_frontend.states.do_tasks import TaskState
from bot_frontend.states.general import MainState

previous_states = {
    'TaskState:conflict_task': TaskState.enter_task_name,
    'TaskState:enter_task_name': TaskState.task_worker,
    'TaskState:task_worker': MainState.start_menu,
    'TaskState:complete_task': TaskState.task_worker,
    'TaskState:show_tasks': TaskState.task_worker,
}

state_to_keyboard = {
    TaskState.enter_task_name: during_the_task_keyboard(),
    TaskState.task_worker: during_the_task_keyboard(),
    MainState.start_menu: get_main_keyboard(),
}

state_to_massage = {
    TaskState.enter_task_name: 'Вернулись к созданию нового дела',
    TaskState.task_worker: 'Вернулись в меню задач',
    MainState.start_menu: 'Вернулись в главное меню',
}
