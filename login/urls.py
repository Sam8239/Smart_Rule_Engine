from django.contrib import admin
from django.urls import path
from . import views
import home


urlpatterns = [
    path("homepage", home.views.homepage, name="homepage"),
    path("logout", views.logout, name="logout"),
    path("char-mapping", views.char_mapping, name="char_mapping"),
    path("", views.login, name="login"),
    path("ruledef", views.rule_def, name="rule_def"),
    path("ruledef/edit/<int:cid>", views.rule_def_edit, name="rule_def_edit"),
    path(
        "ruledef/edit/<int:cid>/<int:chid>",
        views.rule_def_edit_edit,
        name="rule_def_edit_edit",
    ),
    path("saverule", views.save_rule, name="save_rule"),
    path("ruleexe", views.rule_exe, name="rule_exe"),
    path("chardef", views.list_param, name="chardef"),
    path("rolemaster", views.role_master, name="role_master"),
    path("paramdef", views.paramdef, name="paramdef"),
    path("paramdef/insert_param", views.paramdef, name="add_paramdef"),
    path("paramdef/del_param/<int:id>/", views.del_param, name="del_paramdef"),
    path("refresh", views.list_param, name="refresh"),
    path("add_user", views.add_user, name="add_user"),
    path("add_parameters", views.add_parameters, name="add_parameters"),
    path("parameters", views.list_parameters, name="list_parameters"),
    path(
        "parameters/del_parameter/<int:param_id>/",
        views.del_parameter,
        name="del_parameter",
    ),
    path("charmapedit", views.char_map_edit, name="charmapedit"),
    path("asschardef", views.asschardef, name="asschardef"),
    path("charmap", views.char_mapping, name="char_mapping"),
    path("charmap/edit/<int:id>", views.char_mapping_edit, name="char_mapping_edit"),
    path(
        "charmap/edit/<int:id>/<int:paramid>", views.deleteRecord, name="deleteRecord"
    ),
    path("charmap/<int:id>", views.deletesgmc, name="deletesgmc"),
    path("del_sg", views.del_sg, name="del_sg"),
    path("del_g", views.del_g, name="del_g"),
    path("del_m", views.del_m, name="del_m"),
    path("savejson", views.save_json, name="save_json"),
    path("ruleexe/<int:cid>", views.rule_exe_edit, name="rule_exe_edit"),
    path("saveinput", views.saveinput, name="saveinput"),
    path("save_ruledef", views.save_ruledef, name="save_ruledef"),
    path("save_pclass", views.save_pclass, name="save_pclass"),
    path("del_rule_type", views.del_rule_type, name="del_rule_type"),
    path("update_rule_type", views.update_rule_type, name="update_rule_type"),
    path("abcd", views.abcd, name="abcd"),
]
