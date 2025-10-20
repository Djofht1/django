from django.contrib import admin
from .models import conference, submission 
from .models import submission

# ✅ Enregistrer avec ModelAdmin personnalisé
class SubmissionStackedInline(admin.StackedInline):
    model = submission
    fields = ('title', 'abstract', 'status', 'payed', 'submission_id', 'submission_date')
    readonly_fields = ('submission_id', 'submission_date')
    extra = 1  # Nombre de formulaires vides supplémentaires
# ✅ Inline tabulaire (en tableau horizontal)
class SubmissionTabularInline(admin.TabularInline):
    model = submission
    fields = ('title', 'status', 'user', 'payed')
    extra = 1


@admin.register(conference)
class ConferenceAdmin(admin.ModelAdmin):
    list_display = ("name", "theme", "location", "start_date", "end_date", "duration")
    list_filter = ('theme', 'location', 'start_date') 
    search_fields = ('name', 'Description', 'location') 
    fieldsets = (
        ('Informations générales', {
            'fields': ('name', 'theme', 'Description')
        }),
        ('Logistique', {
            'fields': ('location', 'start_date', 'end_date')
        }),
    )
    ordering = ('start_date',)
    date_hierarchy = 'start_date'
    
    def duration(self, obj):
        return f"{obj.duration()} jours"
    duration.short_description = "Durée (jours)"

    inlines = [SubmissionStackedInline,SubmissionTabularInline]   

@admin.action(description="Marquer  comme payées")
def mark_as_payed(modeladmin, req, queryset):
    queryset.update(payed=True)

@admin.action(description="Marquer comme acceptées")
def mark_as_accepted(modeladmin, req, queryset):
    queryset.update(status='accepted')


@admin.register(submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "user", "conference", "submission_date", "payed", "short_abstract")
    actions=[mark_as_payed,mark_as_accepted]
   
    list_filter = ("status", "payed", "conference", "submission_date")

    # 🔹 Champs recherchables
    search_fields = ("title", "keywords", "user__username")

     # Champs modifiables directement depuis la liste
    list_editable = ("status", "payed")

    readonly_fields = ("submission_id", "submission_date")

    fieldsets = (
        ("Infos generales", {
            "fields": ("submission_id", "title", "abstract", "keywords")
        }),
        ("Fichier et conférence", {
            "fields": ("paper", "conference")
        }),
        ("Suivi", {
            "fields": ("status", "payed", "submission_date", "user")
        }),
    )

    # 🔹 Méthode personnalisée pour tronquer l'abstract
    def short_abstract(self, obj):
        if len(obj.abstract) > 50:
            return obj.abstract[:50] + "..."
        return obj.abstract
    short_abstract.short_description = "Abstract (court)"

   
# Personnalisation de l’interface admin
admin.site.site_header = "Gestion de Conférence"
admin.site.site_title = "Conférence Admin Portal"
admin.site.index_title = "Bienvenue dans le portail d'administration de la conférence"
