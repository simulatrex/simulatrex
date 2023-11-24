export const logger = {
  debug: (...args: any[]) => {
    if (
      process.env.NODE_ENV === "development" ||
      process.env.NODE_ENV === "test"
    ) {
      console.info(...args);
    }
  },
  error: (...args: any[]) => {
    if (
      process.env.NODE_ENV === "development" ||
      process.env.NODE_ENV === "test"
    ) {
      console.error(...args);
    }
  },
  info: (...args: any[]) => {
    console.info(...args);
  },
};
