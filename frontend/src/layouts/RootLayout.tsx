import { Manrope } from "next/font/google";

const manrope = Manrope({ subsets: ["latin"] });

type RootLayoutProps = {
  children: React.ReactNode;
};

export default function RootLayout({ children }: RootLayoutProps) {
  return (
    <div className={`w-full min-h-screen bg-dark ${manrope.className}`}>
      {children}
    </div>
  );
}
