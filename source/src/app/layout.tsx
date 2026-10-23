import type { Metadata } from "next";
import { Cormorant_Garamond, Inter, JetBrains_Mono } from "next/font/google";
import "./globals.css";
import { Toaster } from "@/components/ui/toaster";

const serif = Cormorant_Garamond({
  variable: "--font-serif-g",
  subsets: ["latin"],
  weight: ["300", "400", "500", "600", "700"],
  style: ["normal", "italic"],
});

const sans = Inter({
  variable: "--font-sans-ui",
  subsets: ["latin"],
});

const mono = JetBrains_Mono({
  variable: "--font-archival",
  subsets: ["latin"],
  weight: ["400", "500"],
});

export const metadata: Metadata = {
  metadataBase: new URL("https://dawitdseyoum.com"),
  title: "Dawit D. Seyoum — Eye in the City · Fine Art Photography",
  description:
    "Fine art photography by Dawit D. Seyoum (DadaSese69): a five-year meditation on the delicate, ongoing negotiation between urban development and environmental resilience. The Witnesses, The Builders, The Commons — photographic series with written captions from Milan and beyond.",
  keywords: [
    "Dawit D. Seyoum",
    "DadaSese69",
    "Eye in the City",
    "fine art photography",
    "urban nature",
    "environmental resilience",
    "Milan photography",
    "heron",
    "street photography",
    "photography prints",
  ],
  authors: [{ name: "Dawit D. Seyoum" }],
  alternates: { canonical: "/" },
  openGraph: {
    title: "Dawit D. Seyoum — Eye in the City",
    description:
      "A five-year photographic meditation on development and environmental resilience. 'I observe, therefore I capture.'",
    type: "website",
    siteName: "Dawit D. Seyoum",
    url: "https://dawitdseyoum.com",
    images: [
      {
        url: "/og-card.jpg",
        width: 1200,
        height: 630,
        alt: "Dawit D. Seyoum — Eye in the City · fine art photography",
      },
    ],
  },
  twitter: {
    card: "summary_large_image",
    title: "Dawit D. Seyoum — Eye in the City",
    description:
      "Fine art photography: the ongoing play between development and environmental resilience.",
    images: ["/og-card.jpg"],
  },
  robots: { index: true, follow: true },
};

const personSchema = {
  "@context": "https://schema.org",
  "@type": "Person",
  name: "Dawit D. Seyoum",
  alternateName: ["DadaSese69", "Dadasese69"],
  url: "https://dawitdseyoum.com",
  sameAs: [
    "https://bsky.app/profile/dadasese69.bsky.social",
    "https://instagram.com/dadasese69",
    "https://pixelfed.social/dadasese69",
    "https://www.flickr.com/photos/dadasese69",
  ],
  jobTitle: "Fine Art Photographer",
  description:
    "Fine art photographer documenting the interplay between urban development and environmental resilience.",
  knowsAbout: ["Fine art photography", "Street photography", "Urban ecology"],
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body
        className={`${serif.variable} ${sans.variable} ${mono.variable} antialiased`}
      >
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(personSchema) }}
        />
        {children}
        <Toaster />
      </body>
    </html>
  );
}
