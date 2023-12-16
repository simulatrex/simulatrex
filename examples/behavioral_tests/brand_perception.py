from simulatrex import TargetAudience
from simulatrex.experiments import BehavioralTest

# Initialize a behavioral test
audience = (
    TargetAudience()
    .age_range(25, 40)
    .interests(["technology", "innovation"])
    .location("North America")
    .income_range(50000, 100000)
)

behavioural_test = BehavioralTest(target_audience=audience)

# Define conversational tests
behavioural_test.add_conversational_test(
    "Brand Perception",
    questions=["What comes to mind when you think of our brand?"],
    iterations=100,
)

# Run the test
results = behavioural_test.run()
print(results.summarize())

df = results.get_data()

# Plot the results
import seaborn as sns

sns.set_theme(style="whitegrid")
ax = sns.barplot(x="question", y="score", data=df)
ax.set_title("Brand Perception")
ax.set_ylabel("Score")
ax.set_xlabel("Question")
