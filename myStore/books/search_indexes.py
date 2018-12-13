from haystack import indexes
from books.models import Books


class BooksIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    # # 对pdname和description字段进行索引
    # pdname = indexes.CharField(model_attr='pdname')
    #
    # description = indexes.CharField(model_attr='description')

    def get_model(self):
        return Books

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
