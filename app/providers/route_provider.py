from routes.api import api_router


def boot(app):
    try:
        # 注册api路由[routes/api.py]
        app.include_router(api_router, prefix="/api")

        # 打印路由
        if app.debug:
            for route in app.routes:
                print(route)
    except Exception as e:
        print(e)
        raise e
