from django.contrib import admin
from .models import TeamModels

class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'creator', 'is_delete')  # 表示するフィールドを指定
    search_fields = ('name', 'description')  # 検索可能なフィールド
    filter_horizontal = ('members',)  # ManyToManyFieldのフィルタリングを水平に表示

    # 詳細表示ページのカスタマイズ
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'creator', 'is_delete')
        }),
        ('Members', {
            'fields': ('members',)
        }),
    )

admin.site.register(TeamModels, TeamAdmin)