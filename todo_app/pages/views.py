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

router = APIRouter(
    tags=["Pages"]
)

templates = Jinja2Templates(directory="todo_app/templates")

@router.get('/base')
def get_base(request: Request):
    return templates.TemplateResponse('base.html', {'request': request})


@router.get('/tasks')
def get_task_list(request: Request, tasks=Depends(get_all_tasks)):
    distributed_entries: dict = get_distributed_entries(tasks)
    return templates.TemplateResponse("task_list.html",
                                      {'request': request,
                                       'todo_zone_tasks': distributed_entries['todo_zone_entries'],
                                       'middle_zone_tasks': distributed_entries['middle_zone_entries'],
                                       'done_zone_tasks': distributed_entries['done_zone_entries']
                                       })


@router.get('/tasks/category/{cat_slug}')
def get_task_list_by_category(request: Request, tasks=Depends(get_tasks_by_cat)):
    distributed_entries: dict = get_distributed_entries(tasks)
    return templates.TemplateResponse("task_list.html",
                                      {'request': request,
                                       'todo_zone_tasks': distributed_entries['todo_zone_entries'],
                                       'middle_zone_tasks': distributed_entries['middle_zone_entries'],
                                       'done_zone_tasks': distributed_entries['done_zone_entries']
                                       })


@router.get('/tasks/theme/{theme_slug}')
def get_task_list_by_theme(request: Request, tasks=Depends(get_tasks_by_theme)):
    distributed_entries: dict = get_distributed_entries(tasks)
    return templates.TemplateResponse("task_list.html",
                                      {'request': request,
                                       'todo_zone_tasks': distributed_entries['todo_zone_entries'],
                                       'middle_zone_tasks': distributed_entries['middle_zone_entries'],
                                       'done_zone_tasks': distributed_entries['done_zone_entries']
                                       })


@router.get('/categories')
def get_category_list(request: Request, cats=Depends(get_all_categories)):
    return templates.TemplateResponse("category_list.html", {"request": request, "cats": cats})


@router.get('/themes')
def get_theme_list(request: Request, themes=Depends(get_all_themes)):
    return templates.TemplateResponse("theme_list.html", {"request": request, "themes": themes})


@router.get('/colors')
def get_color_list(request: Request, colors=Depends(get_all_colors)):
    return templates.TemplateResponse("color_list.html", {"request": request, "colors": colors})


@router.get('/category/add')
def add_category(request: Request):
    return templates.TemplateResponse("category_add.html", {'request': request})


@router.post('/category/add')
def add_category(request: Request, new_cat=Depends(add_new_category)):
    return templates.TemplateResponse("category_add.html", {'request': request, 'cat': new_cat})


@router.get('/theme/add')
def add_theme(request: Request):
    return templates.TemplateResponse("theme_add.html", {'request': request})


@router.post('/theme/add')
def add_theme(request: Request, new_theme=Depends(add_new_theme)):
    return templates.TemplateResponse("theme_add.html", {'request': request, 'theme': new_theme})


@router.get('/task/add')
def add_task(request: Request):
    return templates.TemplateResponse("task_add.html", {'request': request})


@router.post('/task/add')
def add_task(request: Request, new_task=Depends(add_new_task)):
    return templates.TemplateResponse("task_add.html", {'request': request, 'task': new_task})


@router.get('/color/add')
def add_color(request: Request):
    return templates.TemplateResponse("color_add.html", {'request': request})


@router.post('/color/add')
def add_color(request: Request, new_color=Depends(add_new_color)):
    return templates.TemplateResponse("color_add.html", {'request': request, 'color': new_color})


####################

@router.get('/category/{cat_slug}')
def get_category_detail(request: Request, cat=Depends(get_category)):
    return templates.TemplateResponse('category_detail.html', {'request': request, 'cat': cat})


@router.post('/category/{cat_slug}/update')
def category_update(request: Request, update_cat=Depends(update_category)):
    return templates.TemplateResponse('category_detail.html', {'request': request, 'cat': update_cat})


@router.get('/category/{cat_slug}/delete', dependencies=[Depends(delete_category)])
def category_delete(request: Request):
    return RedirectResponse('/categories')


@router.get('/theme/{theme_slug}')
def get_theme_detail(request: Request, theme=Depends(get_theme)):
    return templates.TemplateResponse('theme_detail.html', {'request': request, 'theme': theme})


@router.post('/theme/{theme_slug}/update')
def theme_update(request: Request, ud_theme=Depends(update_theme)):
    return templates.TemplateResponse('theme_detail.html', {'request': request, 'theme': ud_theme})


@router.get('/theme/{theme_slug}/delete', dependencies=[Depends(delete_theme)])
def theme_delete(request: Request):
    return RedirectResponse('/themes')


@router.get('/task/{task_slug}')
def get_task_detail(request: Request, task=Depends(get_task)):
    return templates.TemplateResponse('task_detail.html', {'request': request, 'task': task})


@router.post('/task/{task_slug}/update')
def task_update(request: Request, ud_task=Depends(update_task)):
    return templates.TemplateResponse('task_detail.html', {'request': request, 'task': ud_task})


@router.get('/task/{task_slug}/delete', dependencies=[Depends(delete_task)])
def task_delete(request: Request):
    return RedirectResponse('/tasks')


@router.get('/color/{color_id}/delete', dependencies=[Depends(delete_color)])
def task_delete(request: Request):
    return RedirectResponse('/colors')

# this is correct
# @router.post('/add')
# async def add_new_category(request: Request, new_category: CategoryCreate = Depends(CategoryCreate.as_form),
#                            session: AsyncSession = Depends(get_async_session)):
#     statement = insert(Category).values(**new_category.dict()).returning(Category)
#     result = await session.execute(statement)
#     await session.commit()
#     cat = result.scalars().first()
#     return templates.TemplateResponse("category_add.html", {'request': request, 'cat': cat})
