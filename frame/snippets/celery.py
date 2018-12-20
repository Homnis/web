from celery import Celery

app = Celery('snippets', include=["snippets.tasks"])
app.config_from_object("snippets.celeryconfig")

if __name__ == "__main__":
    app.start()
