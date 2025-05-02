from django.contrib import admin
from django.utils.html import format_html
from .models import Beyblade

@admin.register(Beyblade)
class BeybladeAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'image_tag', 'created_at', 'updated_at')  # ←image_tagを追加
    search_fields = ('name', 'type')
    list_filter = ('type',)
    ordering = ('name',)

    # 画像を管理画面一覧でサムネイル表示する
    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 50px; height: 50px;" />', obj.image.url)
        return 'No Image'
    image_tag.short_description = 'Image'