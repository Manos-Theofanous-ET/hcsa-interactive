import { defineConfig } from "vite";
import react from "@vitejs/plugin-react-swc";
import tailwind from "@tailwindcss/vite";
import mdx from "@mdx-js/rollup";
import remarkGfm from "remark-gfm";
import path from "node:path";

export default defineConfig({
  plugins: [
    {
      enforce: "pre",
      // remark-gfm enables GitHub-Flavored Markdown tables, strikethrough,
      // task lists, and autolinks — without it, MDX renders `| col | col |`
      // as raw text and the whole chapter reads as a wall of pipes.
      ...mdx({
        providerImportSource: "@mdx-js/react",
        remarkPlugins: [remarkGfm],
      }),
    },
    react(),
    tailwind(),
  ],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
      "@content": path.resolve(__dirname, "./content"),
    },
  },
  server: {
    port: Number(process.env.PORT ?? 5173),
    strictPort: true,
    fs: {
      // Allow the dev server's /@fs/ route to read from the parent
      // workspace (one directory above hcsa-interactive). This is required
      // for the Chrome-extension Claude audit session to read sibling
      // blender-automation/* files (CLAUDE.md, hcsa_web_export.py,
      // WEB_ASSET_BRIEF.md, etc.) via direct file URL. Dev-only read
      // access; nothing ships in the production bundle.
      allow: [path.resolve(__dirname, "..")],
    },
  },
  build: {
    target: "es2022",
    sourcemap: true,
    rollupOptions: {
      output: {
        manualChunks: {
          three: ["three"],
          r3f: ["@react-three/fiber", "@react-three/drei", "@react-three/postprocessing"],
          gsap: ["gsap"],
        },
      },
    },
  },
});
