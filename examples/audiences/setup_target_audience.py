from simulatrex.audiences import TargetAudience

# Define a target audience
audience = (
    TargetAudience()
    .age_range(25, 40)
    .interests(["technology", "innovation"])
    .location("North America")
    .income_range(50000, 100000)
)

print(audience.describe())
