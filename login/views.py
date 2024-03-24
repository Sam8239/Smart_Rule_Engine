from django.contrib import messages
from django.db.models.query_utils import Q
from django.http import HttpResponse, HttpRequest, request
from django.http.response import HttpResponseBadRequest, JsonResponse
from django.shortcuts import redirect, render
from login.models import (
    AssChar,
    CharDetails,
    Country,
    ParamDetails,
    Userdetails,
    CharMaster,
    pSupergroup,
    pGroup,
    pModule,
    pClass,
)
import json
from pathlib import Path
import re


# AUTHENTICATION STARTS
def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        country = request.POST.get("country")

        # Validation Starts
        user = Userdetails.objects.filter(Username=username).first()

        if user is None:
            messages.success(request, "Username Does Not Exist")
        elif user.Password != password:
            messages.success(request, "Password is Invalid")
        elif user.CountryCode != country:
            messages.success(request, "Country is Invalid")
        else:
            # Set cookies to store user information
            response = redirect("home")
            response.set_cookie("username", username)
            response.set_cookie("country", country)
            return response

        return redirect("/")
        # Validation Ends

    # Render country list into dropdown menu on login page
    with open("static/types.json", "r") as file:
        file_data = json.load(file)
        country = file_data["country"]

    return render(request, "index.html", {"country": country})


def logout(request):
    # Clear cookies to remove user information
    response = redirect("login")
    response.delete_cookie("username")
    response.delete_cookie("country")
    return response


# AUTHENTICATION ENDS


# ROLE MASTER STARTS
def role_master(request):
    users = Userdetails.objects.all()
    with open("static/types.json", "r") as file:
        file_data = json.load(file)
        country = file_data["country"]
    return render(request, "role_master.html", {"users": users, "country": country})


def add_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        country = request.POST["country"]
        x = Userdetails(Username=username, Password=password, CountryCode=country)
        x.save()
        return redirect("/role_master")


def del_user(request, username):
    user_to_delete = Userdetails.objects.get(username=username)
    user_to_delete.delete()
    return redirect("/role_master")


# ROLE MASTER ENDS


# RULE DEFINITION PAGE
def rule_def(request):
    try:  # Rule Definition Page
        print("in the try block")
        results = pClass.objects.all()
        supergroup = pSupergroup.objects.all().distinct("supergroup")
        group = pGroup.objects.all().distinct("group")
        module = pModule.objects.all().distinct("module")
        pclass = pClass.objects.all()
        # assignedChar = CharDetails.objects.all().distinct('CharName')
        if request.method == "POST":
            print("in the try in the if ")
            pclassselected = request.POST.get("pclass")
            # pclassid = pClass.objects.filter(mid_id=pclassselected).values('id')
            # assignedChar = CharDetails.objects.filter(
            #     Charmaster_fk_id=pclassid).values('CharName').first().get('CharName')
            if pclassselected != None:
                return redirect("ruledef/edit/" + str(pclassselected))
            elif pclassselected == None:
                messages.success(
                    request, "Select Appropriate SuperGroup, Group, Module, Class."
                )
                return render(
                    request,
                    "ruledef.html",
                    {
                        "results": results,
                        "supergroup": supergroup,
                        "group": group,
                        "module": module,
                        "pclass": pclass,
                    },
                )
    except:
        pass
    # json.loads(data)
    return render(
        request,
        "ruledef.html",
        {
            "results": results,
            "supergroup": supergroup,
            "group": group,
            "module": module,
            "pclass": pclass,
        },
    )


# RULE DEF EDIT PAGE
def rule_def_edit(request, cid):
    try:
        editrec = pClass.objects.get(id=cid)
        results = CharDetails.objects.filter(Charmaster_fk=cid)
        supergroup = pSupergroup.objects.all()
        group = pGroup.objects.all()
        module = pModule.objects.all()
        pclass = pClass.objects.all()
        assignedChar = AssChar.objects.all().distinct("AssChar")
        sno = 0
        with open("static/types.json", "r") as file:
            file_data = json.load(file)
            rule_type = file_data["rule_types"]

        return render(
            request,
            "ruledef_edit.html",
            {
                "rule_type": rule_type,
                "results": results,
                "editrec": editrec,
                "supergroup": supergroup,
                "group": group,
                "module": module,
                "pclass": pclass,
                "assignedChar": assignedChar,
                "sno": sno,
            },
        )
    except:
        messages.success(
            request, "Select Appropriate SuperGroup, Group, Module, Class."
        )
        return redirect("ruledef")


def rule_def_edit_edit(request, cid, chid):
    editrec = pClass.objects.get(id=cid)
    results = CharDetails.objects.filter(id=chid)
    assignedChar = (
        CharDetails.objects.filter(id=chid).values("CharName").first().get("CharName")
    )
    pclass_text = editrec.pclass
    # Display Rules
    with open("static/rules.json", "r") as file:
        file_data = json.load(file)
        rules = file_data["rules"]
        for i in range(len(rules)):
            if rules[i]["pclass"] == pclass_text:
                reqd_json = rules[i]
                break
        try:
            x = reqd_json["asschar"]
            asschar_lst = []
            rule_type_lst = []
            rule_refval_lst = []
            rule_extract_lst = []
            rule_logop_lst = []
            lst = []
            for i in range(len(x)):
                asschar_lst.append(x[i]["asschar_name"])
                if x[i]["asschar_name"] == assignedChar:
                    for j in range(len(x[i]["rules_lst"])):
                        lst.append(x[i]["rules_lst"][j])
                        rule_type_lst.append(x[i]["rules_lst"][j]["rule_type"])
                        rule_refval_lst.append(x[i]["rules_lst"][j]["ref_val"])
                        rule_extract_lst.append(x[i]["rules_lst"][j]["extract"])
                        rule_logop_lst.append(x[i]["rules_lst"][j]["logop"])
            print(lst)
            return render(
                request,
                "ruledef_edit_edit.html",
                {
                    "editrec": editrec,
                    "results": results,
                    "assignedChar": assignedChar,
                    "lst": lst,
                },
            )

        except:
            messages.success(
                request,
                "The Selected Assigned Character has no Rules to Edit. Create Rules.",
            )
            return redirect("rule_def_edit", cid=cid)


def update_rule_type(request):
    print("Entered Django update value")
    # rule_value_lst = []
    # rule_type_id = int(request.POST.get('rule_type_id'))-1
    # print(rule_type_id)
    # pclass = request.POST.get('pclass')
    # asschar = request.POST.get('asschar')
    # rule_value_lst_str = request.POST.get('rule_value_lst')
    # rule_value_lst = json.loads(rule_value_lst_str)
    # print(type(rule_value_lst))
    # rule_type = rule_value_lst[0]
    # rule_ref_val = rule_value_lst[1]
    # rule_ref_val.replace('\"', '\\"')

    # if rule_type=="position":
    #     rule_ref_val1 = json.dumps({'key':rule_value_lst[1]})
    #     rule_ref_val2 = json.loads('{"key_val": "Cost", "start_pos": "3", "char_nos": "5"}')
    #     print(rule_value_lst[1])
    #     print(type(rule_value_lst[1]))
    #     print(type(rule_ref_val1))
    #     print(type(rule_ref_val2))
    # rule_ref_val = rule_value_lst[1]
    # rule_extract_val = rule_value_lst[2]
    # rule_logop = rule_value_lst[3]

    # with open("static/rules.json", "r") as file:
    #     file_data = json.load(file)
    # with open("static/rules.json", "w") as file:
    #     print ("Inside with")
    #     rules = file_data["rules"]
    #     for i in range(len(rules)):
    #         #print ("inside for")
    #         if rules[i]['pclass'] == pclass:
    #             #print("inside if")
    #             for j in range(len(rules[i]['asschar'])):
    #                 print("inside for 2")
    #                 if rules[i]['asschar'][j]['asschar_name'] == asschar:
    #                     print(rules[i]['asschar'][j]['rules_lst'][rule_type_id])
    #                     q = rules[i]['asschar'][j]['rules_lst'][rule_type_id]
    #                     q['ref_val'] = rule_ref_val
    #                     q['extract'] = rule_extract_val
    #                     q['logop'] = rule_logop
    #                     print(q)
    #                     json.dump(file_data, file, indent=4, ensure_ascii=False)
    #                     return HttpResponse("")
    # json.dump(file_data, file, indent=4, ensure_ascii=False)
    return HttpResponse("")


def del_rule_type(request):
    print("Entered Delete Django")
    rule_type_id = int(request.POST.get("rule_type_id"))
    pclass = request.POST.get("pclass")
    asschar = request.POST.get("asschar")
    with open("static/rules.json", "r") as file:
        file_data = json.load(file)
    # print("Outside with")
    with open("static/rules.json", "w") as file:
        # print ("Inside with")
        rules = file_data["rules"]
        for i in range(len(rules)):
            # print ("inside for")
            if rules[i]["pclass"] == pclass:
                # print("inside if")
                for j in range(len(rules[i]["asschar"])):
                    # print("inside for 2")
                    if rules[i]["asschar"][j]["asschar_name"] == asschar:
                        # print ("inside if 2")
                        # print(rules[i]['asschar'][j]['rules_lst'][rule_type_id])
                        del rules[i]["asschar"][j]["rules_lst"][rule_type_id]
                        print(len(rules[i]["asschar"][j]["rules_lst"]))
                        print(rules[i]["asschar"][j])
                        if len(rules[i]["asschar"][j]["rules_lst"]) == 0:
                            print("to delete")
                            del rules[i]["asschar"][j]
                        json.dump(file_data, file, indent=4, ensure_ascii=False)
                        break

        # json.dump(file_data, file)
    # with open("static/rules.json", "w") as file:
    return HttpResponse("")


# SAVE RULE DEFINITION AJAX DJANGO -> JSON
def save_rule(request):
    if request.method == "POST":
        supergroup1 = request.POST.get("supergroup")
        supergroup = (
            pSupergroup.objects.filter(id=supergroup1)
            .values("supergroup")
            .first()
            .get("supergroup")
        )
        group1 = request.POST.get("group")
        group = pGroup.objects.filter(id=group1).values("group").first().get("group")
        module1 = request.POST.get("module")
        module = (
            pModule.objects.filter(id=module1).values("module").first().get("module")
        )
        pclass1 = request.POST.get("pclass")
        pclass = (
            pClass.objects.filter(id=pclass1).values("pclass").first().get("pclass")
        )
        assignedChar1 = request.POST.get("assignedChar")
        assignedChar = (
            CharDetails.objects.filter(Charmaster_fk_id=assignedChar1)
            .values("CharName")
            .first()
            .get("CharName")
        )

        ruletype = request.POST.get("ruletype")
        refvalues = request.POST.get("tb_1")

        # json
        data = {
            "supergroup": supergroup,
            "group": group,
            "module": module,
            "pclass": pclass,
            "assignedChar": assignedChar,
            "ruletype": ruletype,
            "refvalues": refvalues,
        }
        base = Path("rule")
        jsonpath = base / ("ruledata.json")
        base.mkdir(exist_ok=True)
        jsondata = jsonpath.write_text(json.dumps(data))
        # json.dumps(data)

        return redirect("rule_def")


def list_param(request):  # Chardef Page
    # params = CharMaster.objects.all()
    params = pClass.objects.all()
    supergroup = pSupergroup.objects.all().distinct("supergroup")
    group = pGroup.objects.all().distinct("group")
    module = pModule.objects.all().distinct("module")
    pclass = pClass.objects.all().distinct("pclass")
    return render(
        request,
        "chardef.html",
        {
            "params": params,
            "supergroup": supergroup,
            "group": group,
            "module": module,
            "pclass": pclass,
        },
    )


def paramdef(request):
    try:
        if request.method == "POST":
            supergroup1 = request.POST["psupergroup"]
            if str(supergroup1).isdigit():
                supergroup = (
                    pSupergroup.objects.filter(id=supergroup1)
                    .values("supergroup")
                    .first()
                    .get("supergroup")
                )
            else:
                supergroup = supergroup1

            group1 = request.POST["pgroup"]
            if str(group1).isdigit():
                group = (
                    pGroup.objects.filter(sid=group1)
                    .values("group")
                    .first()
                    .get("group")
                )
            else:
                group = group1
            module1 = request.POST["pmodule"]
            # print (module1)
            if str(module1).isdigit():
                module = (
                    pModule.objects.filter(gid=module1)
                    .values("module")
                    .first()
                    .get("module")
                )
            else:
                module = module1

            pclass1 = request.POST["pclass"]
            if str(pclass1).isdigit():
                pclass = (
                    pClass.objects.filter(mid=pclass1)
                    .values("pclass")
                    .first()
                    .get("pclass")
                )
            else:
                pclass = pclass1

            s = pSupergroup(supergroup=supergroup)
            if (
                pSupergroup.objects.filter(supergroup=supergroup).values("id").first()
                == None
            ):
                s.save()

            # print("Supergroup already exists")
            sid = pSupergroup.objects.filter(supergroup=supergroup).values("id")
            g = pGroup(group=group, sid_id=sid)
            if pGroup.objects.filter(group=group).values("id").first() == None:
                g.save()

            gid = pGroup.objects.filter(group=group).values("id")
            m = pModule(module=module, gid_id=gid)
            if pModule.objects.filter(module=module).values("id").first() == None:
                m.save()

            mid = pModule.objects.filter(module=module).values("id")
            mname = pModule.objects.filter(module=module).values("module")
            gname = pGroup.objects.filter(group=group).values("group")
            sgname = pSupergroup.objects.filter(supergroup=supergroup).values(
                "supergroup"
            )
            c = pClass(
                pclass=pclass,
                mid_id=mid,
                supergroup=sgname,
                group=gname,
                module=mname,
                gid_id=gid,
                sid_id=sid,
            )
            if pClass.objects.filter(pclass=pclass).values("id").first() == None:
                c.save()
            # else:
            #     messages.success(request, 'The SGMC COMBO Already Exists!')
            #     return redirect('/refresh')

            # x = CharMaster(pSuperGroup=pSuperGroup, pGroup=pGroup,
            #                pModule=pModule, pClass=pClass)
            # x.save()

            return redirect("/refresh")
    except:
        messages.success(request, "Define All the Values")
        return redirect("/refresh")


def del_sg(request):
    supergroup = request.POST["psupergroup"]
    sid = pSupergroup.objects.filter(supergroup=supergroup).values("id").first()
    sg_to_delete = pSupergroup.objects.get(id=sid.get("id"))
    sg_to_delete.delete()
    return redirect("/refresh")


def del_g(request):
    group = request.POST["pgroup"]
    gid = pGroup.objects.filter(group=group).values("id").first()
    g_to_delete = pGroup.objects.get(id=gid.get("id"))
    g_to_delete.delete()
    return redirect("/refresh")


def del_m(request):
    module = request.POST["pmodule"]
    mid = pModule.objects.filter(module=module).values("id").first()
    m_to_delete = pModule.objects.get(id=mid.get("id"))
    m_to_delete.delete()
    return redirect("/refresh")


def list_param_charmap(request):
    params = {"params": CharMaster.objects.all()}

    return render(request, "charmap.html", params)


def del_param(request, id):
    # param_to_delete = CharMaster.objects.get(id=id)
    param_to_delete = pClass.objects.get(id=id)
    param_to_delete.delete()

    return redirect("/refresh")


# PARAMETER DEFINITION STARTS


def parameters(request):
    parameters = ParamDetails.objects.all()
    supergroup = CharMaster.objects.all().distinct("pSuperGroup")
    group = CharMaster.objects.all().distinct("pGroup")
    module = CharMaster.objects.all().distinct("pModule")
    pclass = CharMaster.objects.all().distinct("pClass")
    with open("static/types.json", "r") as file:
        file_data = json.load(file)
        param_types = file_data["param_type"]

    return render(
        request,
        "parameters.html",
        {
            "param_types": param_types,
            "parameters": parameters,
            "supergroup": supergroup,
            "group": group,
            "module": module,
            "pclass": pclass,
        },
    )


def add_parameters(request):
    try:
        if request.method == "POST":
            ptype = request.POST["ptype"]
            pcode = request.POST["pcode"]
            pdesc = request.POST["pdesc"]
            pactivity = request.POST.get("pactivity", False)

            x = ParamDetails(pType=ptype, pCode=pcode, pDesc=pdesc, pActivity=pactivity)
            x.save()

            return redirect("/parameters")
    except:
        messages.success(request, "Select a Valid Parameter")
        return redirect("/parameters")


def del_parameter(request, param_id):
    parameter_to_delete = ParamDetails.objects.get(id=param_id)
    parameter_to_delete.delete()
    return redirect("/parameters")


# PARAMETER DEFINITION ENDS

# CHARACTER DEFINITON STARTS


def char_map_edit(request):
    return render(request, "char_mapping_edit.html")


def char_mapping_s(request):
    return render(request, "char_mapping_s.html")


def abcd(request):
    # print("entered abcd")
    x = request.POST.get("pclass_json")
    fk_obj = pClass.objects.filter(pclass=x).values("id")
    # print("this is fk")
    for i in fk_obj:
        fk_id = i["id"]
    # print(fk_id)
    request.session["fk_id"] = fk_id
    # print(fk_id)
    return HttpResponse("")


def char_mapping(request):  # Character Mapping Page S
    fk = request.session.get("fk_id")
    if request.method == "POST":
        saverecord = CharDetails()
        saverecord.CharName = request.POST.get("assignedChar")
        saverecord.CharNature = request.POST.get("nature")
        saverecord.BaseChar = request.POST.get("basechar")
        saverecord.CharScope = request.POST.get("scope")
        saverecord.CharCategory = request.POST.get("category")
        saverecord.Charmaster_fk_id = fk
        saverecord.Mandatory = request.POST.get("mandatory")
        saverecord.ValueList = request.POST.get("valuelist")
        saverecord.save()
    results = pClass.objects.all().order_by("id")
    supergroup = pSupergroup.objects.all()
    group = pGroup.objects.all()
    module = pModule.objects.all()
    pclass = pClass.objects.all()
    BaseChar = CharDetails.objects.all().distinct("BaseChar")
    assignedChar = AssChar.objects.all().distinct("AssChar")

    # PARAMETER D Y N A M I C
    nature = ParamDetails.objects.filter(pType="Nature", pActivity="True").values(
        "pDesc"
    )
    baseChar = ParamDetails.objects.filter(pType="Base Char", pActivity=True).values(
        "pDesc"
    )
    scope = ParamDetails.objects.filter(pType="Scope", pActivity=True).values("pDesc")
    category = ParamDetails.objects.filter(pType="Category", pActivity=True).values(
        "pDesc"
    )
    valueList = ParamDetails.objects.filter(pType="Value List", pActivity=True).values(
        "pDesc"
    )
    mandatory = ParamDetails.objects.filter(pType="Mandatory", pActivity=True).values(
        "pDesc"
    )
    return render(
        request,
        "char_mapping_s.html",
        {
            "baseChar": baseChar,
            "scope": scope,
            "category": category,
            "valueList": valueList,
            "mandatory": mandatory,
            "nature": nature,
            "results": results,
            "supergroup": supergroup,
            "group": group,
            "module": module,
            "pclass": pclass,
            "assignedChar": assignedChar,
            "BaseChar": BaseChar,
        },
    )


def char_mapping_edit(request, id):
    try:  # Character Mapping Edit Page
        if request.method == "POST":
            saverecord = CharDetails()
            saverecord.CharName = request.POST.get("assignedChar")
            saverecord.CharNature = request.POST.get("nature")
            saverecord.BaseChar = request.POST.get("basechar")
            saverecord.CharScope = request.POST.get("pscope")
            saverecord.CharCategory = request.POST.get("category")
            saverecord.Charmaster_fk_id = id
            saverecord.ValueList = request.POST.get("valuelist")
            saverecord.Mandatory = request.POST.get("mandatory")
            saverecord.save()
        editrec = pClass.objects.get(id=id)
        results = CharDetails.objects.filter(Charmaster_fk=id)
        supergroup = pSupergroup.objects.all()
        group = pGroup.objects.all()
        module = pModule.objects.all()
        pclass = pClass.objects.all()
        assignedChar = AssChar.objects.all().distinct("AssChar")
        BaseChar = CharDetails.objects.all().distinct("BaseChar")

        nature = ParamDetails.objects.filter(pType="Nature", pActivity=True).values(
            "pDesc"
        )
        baseChar = ParamDetails.objects.filter(
            pType="Base Char", pActivity=True
        ).values("pDesc")
        scope = ParamDetails.objects.filter(pType="Scope", pActivity=True).values(
            "pDesc"
        )
        category = ParamDetails.objects.filter(pType="Category", pActivity=True).values(
            "pDesc"
        )
        valueList = ParamDetails.objects.filter(
            pType="Value List", pActivity=True
        ).values("pDesc")
        mandatory = ParamDetails.objects.filter(
            pType="Mandatory", pActivity=True
        ).values("pDesc")
        return render(
            request,
            "char_mapping_edit.html",
            {
                "baseChar": baseChar,
                "scope": scope,
                "category": category,
                "valueList": valueList,
                "mandatory": mandatory,
                "nature": nature,
                "results": results,
                "editrec": editrec,
                "supergroup": supergroup,
                "group": group,
                "module": module,
                "pclass": pclass,
                "assignedChar": assignedChar,
                "BaseChar": BaseChar,
            },
        )
    except:
        messages.success(request, "Select Appropriate Assigned Character")
        return redirect("char_mapping_edit", id=id)


def deleteRecord(request, id, paramid):  # Delete CharDetails record from table
    deleterow = CharDetails.objects.get(id=paramid)
    deleterow.delete()
    return redirect("char_mapping_edit", id=id)


def deletesgmc(request, id):  # Delete CharMaster record from table
    deleterow = CharDetails.objects.get(Charmaster_fk_id=id)
    deleterow.delete()
    return redirect("char_mapping")


# CHARACTER DEFINITON ENDS

# ASSIGN CHARACTER DEFINITION STARTS


def asschardef(request):
    if request.method == "POST":
        assChar = request.POST["asschar"]
        y = AssChar(AssChar=assChar)
        y.save()
    return render(request, "asschardef.html")


# ASSIGN CHARACTER DEFINITION ENDS

# RULE DEFINITION STARTS


def save_json(request):
    if request.method == "POST":
        print("got a post request")

    if request.is_json:  # application/json
        # handle your ajax request here!
        print("got json:", request.json)
        return JsonResponse("YAAAY")  # answer as json
    else:
        # handle your form submit here!
        print(request.form)
    return render("reledef.html")


flag_redirect = 0
# RULE DEFINITION ENDS

# RULE EXECUTION STARTS


def rule_exe(request):
    global flag_redirect
    supergroup = pSupergroup.objects.all().distinct("supergroup")
    group = pGroup.objects.all().distinct("group")
    module = pModule.objects.all().distinct("module")
    pclass = pClass.objects.all().distinct("pclass")
    assignedChar = CharDetails.objects.all().distinct("CharName")
    flag_redirect = request.session.get("flag_redirect")
    print("flag_redirect")
    print(flag_redirect)
    try:
        if request.method == "POST":
            pclassselected = request.POST.get("pclass")
            flag_redirect = 0
            pclass_text = (
                pClass.objects.filter(id=pclassselected)
                .values("pclass")
                .first()
                .get("pclass")
            )
            input_text = request.POST.get("input_text")
            request.session["input_text"] = input_text
            with open("static/rules.json", "r") as file:
                file_data = json.load(file)
            rules = file_data["rules"]
            for i in range(len(rules)):
                if rules[i]["pclass"] == pclass_text:
                    reqd_json = rules[i]
                    break
            x = reqd_json["asschar"]
            asschar_lst = []
            output_lst = []
            for i in range(len(x)):
                asschar_lst.append(x[i]["asschar_name"])
                print(x[i]["rules_lst"])
                rule_output = []
                logop_lst = []
                no_of_rules = len(x[i]["rules_lst"])

                for j in range(len(x[i]["rules_lst"])):
                    ruletype = x[i]["rules_lst"][j]["rule_type"]
                    ref_val = x[i]["rules_lst"][j]["ref_val"]
                    extract_val = x[i]["rules_lst"][j]["extract"]
                    output = apply_rule(ruletype, ref_val, input_text)
                    output_extracted = extract(output, extract_val)
                    rule_output.append(output_extracted)
                    if j < (no_of_rules - 1):
                        logop = x[i]["rules_lst"][j]["logop"]
                        logop_lst.append(logop)
                if len(rule_output) > 1:
                    final_output_lst = while_loop(rule_output, logop_lst)
                    output_lst.append(final_output_lst)
                else:
                    print("inside else block")
                    output_lst.append(rule_output)
            zip_iterator = zip(asschar_lst, output_lst)
            d = dict(zip_iterator)
            final_res = {k: v for k, v in d.items()}
            request.session["final_res"] = final_res
            return redirect("ruleexe/" + str(pclassselected))
    except:
        messages.success(
            request, "Select Appropriate SuperGroup, Group, Module, Class."
        )
        return render(
            request,
            "ruleexe.html",
            {
                "supergroup": supergroup,
                "group": group,
                "module": module,
                "pclass": pclass,
                "assignedChar": assignedChar,
            },
        )
    return render(
        request,
        "ruleexe.html",
        {
            "supergroup": supergroup,
            "group": group,
            "module": module,
            "pclass": pclass,
            "assignedChar": assignedChar,
        },
    )


def rule_exe_edit(request, cid):
    editrec = pClass.objects.get(id=cid)
    results = CharDetails.objects.filter(Charmaster_fk=cid)
    supergroup = pSupergroup.objects.all()
    group = pGroup.objects.all()
    module = pModule.objects.all()
    pclass = pClass.objects.all()
    assignedChar = AssChar.objects.all().distinct("AssChar")
    sno = 0
    input_text = request.session["input_text"]
    final_res = request.session.get("final_res")
    return render(
        request,
        "rule_exe_edit.html",
        {
            "results": results,
            "editrec": editrec,
            "supergroup": supergroup,
            "group": group,
            "module": module,
            "pclass": pclass,
            "assignedChar": assignedChar,
            "sno": sno,
            "final_res": final_res,
            "input_text": input_text,
        },
    )


# RULE PROCESS - SUB FUNCTIONS
# WHILE LOOP FUNCTION TO ITERATE THROUGH
def while_loop(rules, logop):
    while len(rules) > 1:
        rule1_output = rules[0]
        rule2_output = rules[1]
        if len(logop) == 0:
            break
        logop_val = logop[0]
        del logop[0]
        rule_output = logical_operator(rule1_output, rule2_output, logop_val)
        rules[0] = rule_output
        if len(rules) == 1:
            break
        del rules[1]
    return rule_output


# LOGICAL OPERATOR ON MULTIPLE RULE TYPES
def logical_operator(rule1_output, rule2_output, logical_op):
    if logical_op == "AND":
        if len(rule1_output) == 0 or len(rule2_output) == 0:
            return []
        else:
            return rule1_output + rule2_output
    elif logical_op == "OR":
        if len(rule1_output) == 0:
            return rule2_output
        elif len(rule2_output) == 0:
            return rule1_output
        else:
            return rule1_output + rule2_output
    elif logical_op == "NOT":
        if len(rule1_output) == 0 and len(rule2_output) != 0:
            return rule2_output
        elif len(rule2_output) == 0 and len(rule1_output) != 0:
            return rule1_output
        else:
            return []


# EXTRACTION FUNCTION
def extract(rule_output_lst, extract_val):
    if extract_val == "first":
        output = [rule_output_lst[0]]
    elif extract_val == "last":
        output = [rule_output_lst[-1]]
    elif extract_val == "unique":
        output_set = set(rule_output_lst)
        output = list(output_set)
    elif extract_val == "all":
        output = rule_output_lst
    return output


# MATCHER FUNCTION
def matcher(ref_val, input_text):
    output = []
    for i in range(len(ref_val)):
        output.extend(re.findall(ref_val[i], input_text))
    print(output)
    return output


# REGEX FUNCTION
def regex(ref_val, input_text):
    output = []
    print("In the regex func")
    print(ref_val)
    print(input_text)
    matches = re.finditer(ref_val, input_text)
    print(matches)
    for matchNum, match in enumerate(matches, start=1):
        regex_x = "{match}".format(
            matchNum=matchNum, start=match.start(), end=match.end(), match=match.group()
        )
        output.append(regex_x)
    print("Out of the regex Function")
    return output


# FORMAT FUNCTION
def format(ref_val, input_text):
    ref_val = re.compile(ref_val)
    output = re.findall(ref_val, input_text)
    return output


# POSITION FUNCTION
def position(ref_val, input_text):
    key_val = ref_val["key_val"]
    start_pos = int(ref_val["start_pos"])
    char_no = int(ref_val["char_nos"])
    res = [i for i in range(len(input_text)) if input_text.startswith(key_val, i)]
    output_lst = []
    for j in range(len(res)):
        key_val_index = res[j] + len(key_val)
        output_start = key_val_index + start_pos - 1
        output = input_text[output_start : output_start + char_no + 1]
        output_lst.append(output)
    return output_lst


# DEFAULT FUNCTION
def default(ref_val):
    return ref_val


# APPLY RULE FUNCTION
def apply_rule(ruletype, ref_val, input_text):
    output = []
    if ruletype == "Matcher":
        output = matcher(ref_val, input_text)
        if output == []:
            output = ["Not Found"]
        return output
    elif ruletype == "Regex":
        output = regex(ref_val, input_text)
        if output == []:
            output = ["Not Found"]
        return output
    elif ruletype == "Format":
        output = format(ref_val, input_text)
        if output == []:
            output = ["Not Found"]
        return output
    elif ruletype == "Position":
        output = position(ref_val, input_text)
        return output
    else:
        output = default(ref_val)
    return output


def saveinput(request):
    if request.method == "POST":
        pclassselected = request.POST.get("pclass")
        return redirect("ruleexe/" + str(pclassselected))


def save_ruledef(request):
    pClass = request.POST.get("pclass")
    rules_lst = request.POST.get("rules_lst")
    json_obj = json.loads(rules_lst)

    try:
        with open("static/rules.json", "r") as file:
            file_data = json.load(file)

        rules = file_data.get("rules", [])

        for rule in rules:
            if rule["pclass"] == pClass:
                asschar_exists = any(
                    x.get("asschar_name") == json_obj["asschar_name"]
                    for x in rule.get("asschar", [])
                )

                if asschar_exists:
                    # Add the new rule to the existing "asschar"
                    for asschar in rule.get("asschar", []):
                        if asschar.get("asschar_name") == json_obj["asschar_name"]:
                            asschar.setdefault("rules_lst", []).extend(
                                json_obj["rules_lst"]
                            )
                            break
                else:
                    # Add a new "asschar" with the rule
                    rule.setdefault("asschar", []).append(
                        {
                            "asschar_name": json_obj["asschar_name"],
                            "rules_lst": json_obj["rules_lst"],
                        }
                    )

                break
        else:
            print("No matching pClass found in rules")

        with open("static/rules.json", "w") as file:
            json.dump(file_data, file, indent=4, ensure_ascii=False)

        return HttpResponse("The JSON is served!")
    except Exception as e:
        print(f"Error: {e}")
        return HttpResponse("Error occurred while processing the request.")


def save_pclass(request):
    print("Entered django")
    pclass_json = request.POST.get("pclass_json")
    print(pclass_json)
    json_obj = json.loads(pclass_json)
    pclass_value = json_obj["pclass"]
    print(pclass_value)
    flag = 0
    with open("static/rules.json", "r") as file:
        file_data = json.load(file)
    with open("static/rules.json", "w") as file:
        rules = file_data["rules"]
        pclass_name = []
        for i in range(len(rules)):
            pclass_name.append(rules[i]["pclass"])
        print(pclass_name)
        if pclass_value in pclass_name:
            flag = 1
        if flag == 0:
            file_data["rules"].append(json_obj)

            json.dump(file_data, file, indent=4, ensure_ascii=False)
        else:
            json.dump(file_data, file, indent=4, ensure_ascii=False)

    print(json_obj)
    return HttpResponse("The json is served!")


# RULE EXECUTION ENDS
