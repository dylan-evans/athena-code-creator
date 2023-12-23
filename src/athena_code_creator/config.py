import os
from pathlib import Path

import pydantic
from openai.types.beta.thread import Thread

USER_CONFIG = Path("~/.config/athena-code-creator/config.json").expanduser()


def load_user_config(path: Path = USER_CONFIG) -> "UserConfig":
    try:
        return UserConfig.model_validate_json(path.read_text())
    except IOError:
        return UserConfig()


def save_user_config(config: "UserConfig", path: Path = USER_CONFIG):
    if not path.parent.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(config.model_dump_json())


class AthenaConfig(pydantic.BaseModel):
    assistant_id: str | None = None
    thread_id: str | None = None

    @classmethod
    def load_config_or_get_defaults(cls, filename: str) -> ("AthenaConfig", bool):
        if os.path.exists(filename):
            with open(filename) as src:
                return cls.model_validate_json(src.read()), True
        return cls(), False

    def save(self, filename: str):
        with open(filename, "w") as dst:
            dst.write(self.model_dump_json())

class Labels(pydantic.BaseModel):
    assistant: dict[str, str] = {}
    thread: dict[str, str] = {}
    run: dict[str, str] = {}


class Cache(pydantic.BaseModel):
    thread: dict[str, Thread] = {}


class UserConfig(pydantic.BaseModel):
    selected_assistant_id: str | None = None
    selected_thread_id: str | None = None
    selected_run_id: str | None = None

    labels: Labels = Labels()
    cache: Cache = Cache()

    def save(self):
        save_user_config(self)
