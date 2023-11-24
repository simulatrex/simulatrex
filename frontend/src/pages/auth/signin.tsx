import SignupForm from "@/components/Auth/SignupForm";
import OnboardingLayout from "@/layouts/OnboardingLayout";
import RootLayout from "@/layouts/RootLayout";

export default function Signin() {
  return (
    <RootLayout>
      <OnboardingLayout>
        <div className="w-full flex flex-row px-20">
          <div className="w-1/2 flex flex-col justify-center items-start">
            <SignupForm />
          </div>
          <div className="relative w-1/2 h-[90vh] flex flex-col justify-center bg-no-repeat bg-right bg-cover bg-start rounded-lg">
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
