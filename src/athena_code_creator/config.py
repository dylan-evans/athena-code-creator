import os

import pydantic


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

