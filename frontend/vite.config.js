import { defineConfig } from "vite";
import { EsLinter, linterPlugin } from "vite-plugin-linter";
import react from "@vitejs/plugin-react";

// https://vitejs.dev/config/
export default defineConfig((configEnv) => ({
  base: "/",
  plugins: [
    react(),
    linterPlugin({
      include: ["./src/**/*.js", "./src/**.*jsx"],
      linters: [
        new EsLinter({
          configEnv: configEnv,
          serveOptions: { clearCacheOnStart: true },
        }),
      ],
    }),
  ],
  preview: {
    port: 3000,
    strictPort: true,
  },
  server: {
    port: 3000,
    strictPort: true,
    host: true,
    origin: "http://0.0.0.0:3000",
  },
}));
