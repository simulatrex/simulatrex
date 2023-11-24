import OnboardingLayout from "@/layouts/OnboardingLayout";
import RootLayout from "@/layouts/RootLayout";
import SimulationBuilderLayout from "@/layouts/SimulationBuilderLayout";

export default function Home() {
  return (
    <RootLayout>
      <SimulationBuilderLayout>{/* ... */}</SimulationBuilderLayout>
    </RootLayout>
  );
}
