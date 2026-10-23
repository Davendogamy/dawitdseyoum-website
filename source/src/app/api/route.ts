import { NextResponse } from "next/server";

// Statically render this health-check route so the site also builds
// with `output: 'export'` (STATIC_EXPORT=1) for static hosting.
export const dynamic = "force-static";

export async function GET() {
  return NextResponse.json({ message: "Hello, world!" });
}
