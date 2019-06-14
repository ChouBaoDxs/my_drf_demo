import xadmin
from xadmin import views


class BaseSettings(object):
    enable_themes = True
    use_bootswatch = True


class CommSettings(object):
    site_title = "标题"
    site_footer = "底部标题"
    # menu_style = "accordion"  # 侧边栏可折叠
    global_search_models = []


xadmin.site.register(views.BaseAdminView, BaseSettings)
xadmin.site.register(views.CommAdminView, CommSettings)
