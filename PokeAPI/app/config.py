from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = 'PokéAPI'
    poke_parser_url: str | None = None
    poke_api_ofc_url: str | None = None
    DATABASE_URL: str

    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8'
        )


settings = Settings()
