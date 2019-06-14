import xadmin

from .models import Student

@xadmin.sites.register(Student)  # 注册方式一
class StudentAdmin(object):
    list_display = ['id', 'name', 'age', 'gender', 'is_delete']
    list_display_links = ['id', 'name']
    # list_quick_filter = [{"field": "name", "limit": 10}]
    search_fields = ['name']
    # raw_id_fields = []
    # relfield_style = "fk-select"
    # reversion_enable = True
    list_filter = ['gender', 'age']
    # readonly_fields = []
    # model_icon = 'fa fa-file-text'
    # list_editable = []
    # show_detail_fields =[]
    # refresh_times = [5, 10, 30]
    # actions = []
    # aggregate_fields = {"user_count": "sum", "view_count": "sum"}
    list_export = []  # 禁用数据导出功能


# xadmin.site.register(Robot, RobotAdmin)   # 注册方式二