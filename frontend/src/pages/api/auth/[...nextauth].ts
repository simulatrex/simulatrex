import NextAuth from "next-auth";
import GoogleProvider from "next-auth/providers/google";

import { logger } from "@/utils/logger";

export default NextAuth({
  pages: {
    signIn: "/auth/signin",
  },
  providers: [
    GoogleProvider({
      clientId: process.env.GOOGLE_CLIENT_ID as string,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET as string,
      authorization: {
        params: {
          prompt: "consent",
          scope: "email",
        },
      },
    }),
  ],
  callbacks: {
    async signIn({ account, profile }) {
      logger.debug("signIn", { account, profile });

      return true;
    },
    async jwt({ token, user }) {
      if (user) {
        /*
         * For adding custom parameters to user in session, we first need to add those parameters
         * in token which then will be available in the `session()` callback
         */
        logger.debug("jwt", { token, user });
      }

      return token;
    },
    async session({ session, token }) {
      if (session.user) {
        // ** Add custom params to user in session which are added in `jwt()` callback via `token` parameter
        logger.debug("session", { session, token });
      }

      return session;
    },
  },
  secret: process.env.NEXTAUTH_SECRET,
  session: {
    maxAge: 30 * 24 * 60 * 60, // 30 days
    strategy: "jwt",
  },
  debug: process.env.NODE_ENV === "development",
});
