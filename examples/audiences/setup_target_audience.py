import asyncio
import dotenv
from simulatrex import TargetAudience

dotenv.load_dotenv()

audience = (
    TargetAudience(id="Ealry adopters")
    .age_range(25, 40)
    .interests(["technology", "innovation"])
)

print(audience.describe())
