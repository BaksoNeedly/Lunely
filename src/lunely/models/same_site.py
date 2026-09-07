from enum import Enum

# I don't really know what are they really do for.
class SameSite(Enum):
    STRICT = "strict"
    LAX = "Lax" # Recommended
    NONE = "None"