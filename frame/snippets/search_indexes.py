from haystack import indexes

from .models import Snippet


class SnippetIndex(indexes.SearchIndex, indexes.Indexable):
    # 类名必须为需要检索的Model_name+Index，这里需要检索Snippet，所以创建SnippetIndex
    code = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')
    language = indexes.CharField(model_attr='language')

    def get_model(self):
        return Snippet