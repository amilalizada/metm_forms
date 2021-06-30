from django.contrib import admin

from Forms.models import *
from django.utils.safestring import mark_safe
import json
# admin.site.register(Fields)
# admin.site.register(Values)
# admin.site.register(Emails)

@admin.register(Values)
class ValueAdmin(admin.ModelAdmin):
    list_display = ('fields','value',)
    search_fields = ('fields','value',)
    list_filter = ('fields','value',)
    fieldsets = (
        ('Information', {
            'description': 'Əsas Sahə',
            'classes': ('collapse',),
            'fields': ('field','value',)
        }),
    )

@admin.register(SecondValues)
class CompletedFormsAdmin(admin.ModelAdmin):
    list_display = ('forms',)
    # search_fields = ('forms','datas',)
    list_filter = ('forms','datas',)
    save_on_top = True
    
    fields = ('forms','custom_field')
    readonly_fields = ('custom_field',)

    def custom_field(self):
        # print(obj.details)
        details = json.loads(self.details)
        # print(obj.details,'aaaaaaaaaaaaaaaaa',type(obj.details))
        html_a = ''
        print(html_a,'bbbbbbbbbbbbbbbbbbbbbbbbbbbb')
        for key,value in details.items():
            # print(key,'keyyy')
            # print(value,'valueeee')
            html_a +="""
                <table>
                    <tr>
                    <td>%s</td>
                    <td>%s</td>
                    </tr>
                </table>
            """ %(key , value)
        print(html_a,'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
        return mark_safe(html_a)

@admin.register(Emails)
class EmailsAdmin(admin.ModelAdmin):
    list_display = ('forms','email',)
    search_fields = ('forms','email',)
    list_filter = ('forms','email',)
    save_on_top = True
    fieldsets = (
        ('Information', {
            'description': 'Əsas Sahə',
            'classes': ('collapse',),
            'fields': ('form','email',)
        }),
    )

class FieldsInline(admin.TabularInline):
    model = Fields
    extra = 0


class EmailInline(admin.TabularInline):
    model = Emails
    extra = 0


@admin.register(Forms)
class FormsAdmin(admin.ModelAdmin):
    list_display = ('name','created_at','updated_at','is_published')
    search_fields = ('name','created_at','is_published')
    list_filter = ('name','created_at','is_published')
    save_on_top = True
    fieldsets = (
        ('Information', {
            'description': 'Əsas Sahə',
            'classes': ('collapse',),
            'fields': ('name','is_published',)
        }),
      
    )
    inlines = [FieldsInline,EmailInline]

@admin.register(Fields)
class FieldsAdmin(admin.ModelAdmin):
    list_display = ('form','label','types','requirement',)
    search_fields = ('form','label','types','requirement',)
    list_filter = ('form','label','types','requirement',)
    save_on_top = True
    fieldsets = (
        ('Information', {
            'description': 'Əsas Sahə',
            'classes': ('collapse',),
            'fields': ('form','label','types','requirement','is_published',)
        }),
    )
   
