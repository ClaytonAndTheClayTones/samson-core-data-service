from .phonenumber import PhoneNumber

__all__: list[str]

def country_name_for_number(numobj: PhoneNumber, lang: str, script: str | None = ..., region: str | None = ...) -> str: ...
def _region_display_name(region_code: str, lang: str, script: str | None = ..., region: str | None = ...) -> str: ...
def description_for_valid_number(numobj: PhoneNumber, lang: str, script: str | None = ..., region: str | None = ...) -> str: ...
def description_for_number(numobj: PhoneNumber, lang: str, script: str | None = ..., region: str | None = ...) -> str: ...
