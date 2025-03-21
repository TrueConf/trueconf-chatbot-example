import i18n
from app.config import config

i18n.load_path.append("app/locales")
i18n.set("locale",config.bots_language)
i18n.set("filename_format", "{locale}.{format}")

_ = i18n.t