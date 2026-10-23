import type { NextConfig } from "next";

// Default: standalone server build (used by the managed preview and `npm start`).
// STATIC_EXPORT=1 npm run build  →  a fully static site emitted to ./out,
// hostable on any static host (Netlify Drop, Cloudflare Pages, GitHub Pages…).
const isStaticExport = process.env.STATIC_EXPORT === "1";

const nextConfig: NextConfig = {
  ...(isStaticExport
    ? { output: "export" as const, images: { unoptimized: true } }
    : { output: "standalone" as const }),
  typescript: {
    ignoreBuildErrors: true,
  },
  reactStrictMode: false,
};

export default nextConfig;
