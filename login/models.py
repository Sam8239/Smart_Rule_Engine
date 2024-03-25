from django.db import connections, models


# Create your models here.
class Country(models.Model):
    CountryCode = models.CharField(primary_key=True, max_length=100)
    CountryName = models.CharField(max_length=100)


class Userdetails(models.Model):
    Username = models.CharField(max_length=100)
    Role = models.CharField(max_length=100, default="User")
    Password = models.CharField(max_length=100)
    CountryCode = models.CharField(max_length=100, default="IN")
    # CountryCode = models.ForeignKey(Country, on_delete=models.CASCADE)


class CharMaster(models.Model):
    CountryCode = models.CharField(max_length=100, default="IN")
    pSuperGroup = models.CharField(max_length=100)
    pGroup = models.CharField(max_length=100)
    pModule = models.CharField(max_length=100)
    pClass = models.CharField(max_length=100)


class ParamDetails(models.Model):
    CountryCode = models.CharField(max_length=100, default="IN")
    pType = models.CharField(max_length=500)
    pCode = models.CharField(max_length=100)
    pDesc = models.CharField(max_length=500)
    pActivity = models.BooleanField(default=True)


class AssChar(models.Model):
    AssChar = models.CharField(max_length=100)
    CountryCode = models.CharField(max_length=100, default="IN")


class pSupergroup(models.Model):
    supergroup = models.CharField(max_length=100)


class pGroup(models.Model):
    group = models.CharField(max_length=100)
    sid = models.ForeignKey(pSupergroup, on_delete=models.CASCADE)


class pModule(models.Model):
    module = models.CharField(max_length=100)
    gid = models.ForeignKey(pGroup, on_delete=models.CASCADE)


class pClass(models.Model):
    pclass = models.CharField(max_length=100)
    mid = models.ForeignKey(pModule, on_delete=models.CASCADE)
    supergroup = models.CharField(max_length=500)
    group = models.CharField(max_length=500)
    module = models.CharField(max_length=500)
    sid = models.ForeignKey(pSupergroup, on_delete=models.CASCADE)
    gid = models.ForeignKey(pGroup, on_delete=models.CASCADE)
    CountryCode = models.CharField(max_length=100, default="IN")


class CharDetails(models.Model):
    CountryCode = models.CharField(max_length=100, default="IN")
    Charmaster_fk = models.ForeignKey(pClass, on_delete=models.CASCADE)
    CharName = models.CharField(max_length=100, default=None)
    CharNature = models.CharField(max_length=100, default=None)
    BaseChar = models.CharField(max_length=100, default=None)
    CharScope = models.CharField(max_length=100, default=None)
    CharCategory = models.CharField(max_length=100, default=None)
    ValueList = models.CharField(max_length=100)
    Mandatory = models.CharField(max_length=100)
    # DefaultValue = models.CharField(max_length=100, default=None)


# class RulesDef(models.Model):
#     supergroup = models.
