from django.apps import AppConfig


class ProjectBstoreConfig(AppConfig):
    name = 'project_bstore'

    def ready(self):
    	import project_bstore.signals
