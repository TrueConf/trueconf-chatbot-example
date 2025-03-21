import os
import tomllib
import json
import subprocess
from llama_cpp import Llama

import logging

logger = logging.getLogger("chat_bot")


CONFIG_PY_PATH = "config_models.py"
CONFIG_JSON_PATH = "config.json"
CONFIG_TOML_PATH = "config.toml"

# Генерируем config.py только если его нет
if not os.path.exists(CONFIG_PY_PATH):
    # Конвертируем TOML → JSON
    with open(CONFIG_TOML_PATH, "rb") as f:
        data = tomllib.load(f)

    with open(CONFIG_JSON_PATH, "w") as f:
        json.dump(data, f, indent=4)

    # Генерация Pydantic-моделей
    subprocess.run(
        [
            "datamodel-codegen",
            "--input",
            CONFIG_JSON_PATH,
            "--input-file-type",
            "json",
            "--output",
            CONFIG_PY_PATH,
            "--class-name",
            "Models",
        ],
        check=True,
    )

    # Удаляем временный JSON-файл
    os.remove(CONFIG_JSON_PATH)


with open("config.toml", "rb") as f:
    data = tomllib.load(f)


from config_models import Models
config = Models.model_validate(data)

from app.localization import _

logger.info(_("logger.info.loading_llm"))


try:
    llm = Llama(
        model_path=f"{config.gpt_bot.llama.local_dir}/{config.gpt_bot.llama.filename}",
        n_gpu_layers=config.gpt_bot.llama.n_gpu_layers,
        n_ctx=config.gpt_bot.llama.n_ctx
    )
except ValueError as e:
    try:
        llm = Llama.from_pretrained(
            repo_id=config.gpt_bot.llama.repo_id,
            filename=config.gpt_bot.llama.filename,
            n_ctx=config.gpt_bot.llama.n_ctx,
            n_gpu_layers=config.gpt_bot.llama.n_gpu_layers,
            local_dir = config.gpt_bot.llama.local_dir)
    except Exception:
        logger.error("%s", e, exc_info=True)
        raise
else:
    logger.info(_("logger.info.loaded_llm"))
