import PrimaryButton from "@/components/PrimaryButton";
import Sidebar from "@/components/Sidebar";
import OnboardingLayout from "@/layouts/OnboardingLayout";
import RootLayout from "@/layouts/RootLayout";

export default function Start() {
  return (
    <RootLayout>
      <OnboardingLayout>
        <div className="w-full flex flex-row">
          <Sidebar />
          <div className="relative w-[80vw] h-[90vh] flex flex-col justify-center px-20 bg-no-repeat bg-center bg-cover bg-start rounded-lg">
            {/* Content */}
            <div className="justfiy-start flex flex-col">
              <h1 className="mb-4 text-8xl text-white">
                Welcome to
                <br />
                Simulatrex
              </h1>
              <p className="mb-8 text-xl text-white">
                Sign up to run your simulation.
              </p>

              <PrimaryButton href="/auth/signin">Start</PrimaryButton>
            </div>

            {/* Progress */}
            <div className="absolute right-4 bottom-4">
              <div className="relative w-16 h-16 bg-white rounded-full">
                <p className="absolute inset-0 flex justify-center items-center text-primary">
                  60%
                </p>
              </div>
            </div>
          </div>
        </div>
      </OnboardingLayout>
    </RootLayout>
  );
}
