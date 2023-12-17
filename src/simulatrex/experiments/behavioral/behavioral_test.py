from simulatrex import TargetAudience


class BehavioralTest:
    def __init__(self, audience: TargetAudience):
        self.audience = audience
        self.tests = []

    def add_conversational_test(self, title: str, questions: list, iterations: int):
        self.tests.append(
            {"title": title, "questions": questions, "iterations": iterations}
        )

    async def run(self):
        # Placeholder for running the test
        results = {"test_results": []}
        agent_responses = []

        async for agent_response in self.audience.run_conversation_test(
            self.tests[0]["questions"], self.tests[0]["iterations"]
        ):
            agent_responses.append(agent_response)
            yield agent_response

    def summarize(self):
        return "Behavioral Test Results: " + str(self.run())
