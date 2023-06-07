from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from todo_app.logic.zone_distribution import get_distributed_entries
from todo_app.routers.category import get_all_categories, add_new_category, update_category, get_category, \
    delete_category
from todo_app.routers.task import get_all_tasks, get_tasks_by_cat, get_tasks_by_theme, add_new_task, update_task, \
    get_task, delete_task
from todo_app.routers.theme import get_all_themes, add_new_theme, update_theme, get_theme, delete_theme
from todo_app.routers.color import get_all_colors, add_new_color, delete_color
import starlette.status as status
from todo_app.auth.config import current_active_user

router = APIRouter(
    tags=["Pages"]
)

templates = Jinja2Templates(directory="todo_app/templates")


@router.get('/')
def login(request: Request):
    return templates.TemplateResponse('login.html', {'request': request})


@router.get('/edit')
def edit(request: Request, user=Depends(current_active_user)):
    return templates.TemplateResponse('edit.html', {'request': request, 'user': user})


@router.get('/register')
def register(request: Request, colors=Depends(get_all_colors)):
    return templates.TemplateResponse('register.html', {'request': request, 'colors': colors})


"""tasks"""


@router.get('/tasks')
def get_task_list(request: Request, tasks=Depends(get_all_tasks), cats=Depends(get_all_categories),
                  themes=Depends(get_all_themes), user=Depends(current_active_user)):
    distributed_entries: dict = get_distributed_entries(tasks)
    return templates.TemplateResponse("task_list.html",
                                      {'request': request,
                                       'todo_zone_tasks': distributed_entries['todo_zone_entries'],
                                       'middle_zone_tasks': distributed_entries['middle_zone_entries'],
                                       'done_zone_tasks': distributed_entries['done_zone_entries'],
                                       'cats': cats,
                                       'themes': themes,
                                       'user': user
                                       })


@router.get('/tasks/category/{cat_slug}')
def get_task_list_by_category(request: Request, tasks=Depends(get_tasks_by_cat), cats=Depends(get_all_categories),
                              themes=Depends(get_all_themes), user=Depends(current_active_user)):
    distributed_entries: dict = get_distributed_entries(tasks)
    return templates.TemplateResponse("task_list.html",
                                      {'request': request,
                                       'todo_zone_tasks': distributed_entries['todo_zone_entries'],
                                       'middle_zone_tasks': distributed_entries['middle_zone_entries'],
                                       'done_zone_tasks': distributed_entries['done_zone_entries'],
                                       'cats': cats,
                                       'themes': themes,
                                       'user': user
                                       })


@router.get('/tasks/theme/{theme_slug}')
def get_task_list_by_theme(request: Request, tasks=Depends(get_tasks_by_theme), cats=Depends(get_all_categories),
                           themes=Depends(get_all_themes), user=Depends(current_active_user)):
    distributed_entries: dict = get_distributed_entries(tasks)
    return templates.TemplateResponse("task_list.html",
                                      {'request': request,
                                       'todo_zone_tasks': distributed_entries['todo_zone_entries'],
                                       'middle_zone_tasks': distributed_entries['middle_zone_entries'],
                                       'done_zone_tasks': distributed_entries['done_zone_entries'],
                                       'cats': cats,
                                       'themes': themes,
                                       'user': user
                                       })


@router.get('/tasks/add')
def add_task(request: Request, themes=Depends(get_all_themes), user=Depends(current_active_user)):
    return templates.TemplateResponse("task_add.html", {'request': request, 'themes': themes, 'user': user})


@router.post('/tasks/add', dependencies=[Depends(add_new_task)])
def add_task(request: Request):
    return RedirectResponse('/tasks', status_code=status.HTTP_302_FOUND)


@router.get('/tasks/{task_slug}')
def get_task_detail(request: Request, task=Depends(get_task), themes=Depends(get_all_themes),
                    user=Depends(current_active_user)):
    return templates.TemplateResponse('task_detail.html',
                                      {'request': request, 'task': task, 'themes': themes, 'user': user})


@router.post('/tasks/{task_slug}', dependencies=[Depends(update_task)])
def task_update(request: Request):
    return RedirectResponse('/tasks', status_code=status.HTTP_302_FOUND)


@router.get('/tasks/{task_slug}/delete', dependencies=[Depends(delete_task)])
def task_delete(request: Request):
    return RedirectResponse('/tasks')


"""categories"""


@router.get('/categories')
def get_category_list(request: Request, cats=Depends(get_all_categories), colors=Depends(get_all_colors),
                      user=Depends(current_active_user)):
    return templates.TemplateResponse("category_list.html",
                                      {"request": request, "cats": cats, 'colors': colors, 'flag': 'add', 'user': user})


@router.post('/categories/add', dependencies=[Depends(add_new_category)])
def add_categories(request: Request, cats=Depends(get_all_categories), colors=Depends(get_all_colors),
                   user=Depends(current_active_user)):
    return templates.TemplateResponse("category_list.html",
                                      {"request": request, "cats": cats, 'colors': colors, 'flag': 'add', 'user': user})


@router.get('/categories/{cat_slug}')
def get_category_detail(request: Request, cats=Depends(get_all_categories), update_cat=Depends(get_category),
                        colors=Depends(get_all_colors), user=Depends(current_active_user)):
    return templates.TemplateResponse('category_list.html',
                                      {'request': request, 'cats': cats, 'colors': colors, 'update_cat': update_cat,
                                       'flag': 'update', 'user': user})


@router.post('/categories/{cat_slug}/update', dependencies=[Depends(update_category)])
def category_update(request: Request):
    return RedirectResponse('/categories', status_code=status.HTTP_302_FOUND)


@router.get('/categories/{cat_slug}/delete', dependencies=[Depends(delete_category)])
def category_delete(request: Request):
    return RedirectResponse('/categories')


"""themes"""


@router.get('/themes')
def get_theme_list(request: Request, themes=Depends(get_all_themes), colors=Depends(get_all_colors),
                   cats=Depends(get_all_categories), user=Depends(current_active_user)):
    return templates.TemplateResponse("theme_list.html",
                                      {"request": request, "themes": themes, 'colors': colors, 'cats': cats,
                                       'flag': 'add', 'user': user})


@router.post('/themes/add', dependencies=[Depends(add_new_theme)])
def add_theme(request: Request, themes=Depends(get_all_themes), colors=Depends(get_all_colors),
              cats=Depends(get_all_categories), user=Depends(current_active_user)):
    return templates.TemplateResponse("theme_list.html",
                                      {"request": request, "themes": themes, 'colors': colors, 'cats': cats,
                                       'flag': 'add', 'user': user})


@router.get('/themes/{theme_slug}')
def get_theme_detail(request: Request, themes=Depends(get_all_themes), update_theme=Depends(get_theme),
                     colors=Depends(get_all_colors), cats=Depends(get_all_categories),
                     user=Depends(current_active_user)):
    return templates.TemplateResponse('theme_list.html',
                                      {'request': request, 'themes': themes, 'update_theme': update_theme,
                                       'colors': colors, 'cats': cats, 'flag': 'update', 'user': user})


@router.post('/themes/{theme_slug}/update', dependencies=[Depends(update_theme)])
def theme_update(request: Request):
    return RedirectResponse('/themes', status_code=status.HTTP_302_FOUND)


@router.get('/themes/{theme_slug}/delete', dependencies=[Depends(delete_theme)])
def theme_delete(request: Request):
    return RedirectResponse('/themes')


"""colors"""


@router.get('/colors/{color_id}/delete', dependencies=[Depends(delete_color)])
def task_delete(request: Request):
    return RedirectResponse('/colors')


@router.get('/colors')
def get_color_list(request: Request, colors=Depends(get_all_colors), user=Depends(current_active_user)):
    return templates.TemplateResponse("color_list.html", {"request": request, "colors": colors, 'user': user})


@router.post('/colors/add', dependencies=[Depends(add_new_color)])
def add_color(request: Request):
    return RedirectResponse('/colors', status_code=status.HTTP_302_FOUND)
