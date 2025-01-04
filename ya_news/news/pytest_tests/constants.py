from news.forms import BAD_WORDS

FORM_COMMENT_DATA = {'text': 'Новый текст', }
FORM_COMMENT_BAD_WORDS_DATA = {'text': f'Текст {BAD_WORDS[0]}, еще текст', }

LOGIN_URL_LITERAL = 'users:login'
LOGOUT_URL_LITERAL = 'users:logout'
SIGNUP_URL_LITERAL = 'users:signup'

HOME_URL_LITERAL = 'news:home'
EDIT_URL_LITERAL = 'news:edit'
DELETE_URL_LITERAL = 'news:delete'
DETAIL_URL_LITERAL = 'news:detail'

COMMENT_URL_LITERAL = '#comments'
