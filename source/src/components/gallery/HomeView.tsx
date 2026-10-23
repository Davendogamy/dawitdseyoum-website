'use client'

import Image from 'next/image'
import { ArrowDown, Feather } from 'lucide-react'
import { photos } from '@/data/photos'
import type { View } from './Nav'

const HERO_ID = '012-fence-to-face'

export function HomeView({ onNav, onOpen }: { onNav: (v: View) => void; onOpen: (id: string) => void }) {
  const hero = photos.find((p) => p.id === HERO_ID) ?? photos[0]

  return (
    <section className="relative flex min-h-screen flex-col items-center justify-center px-5 pb-32 pt-28 sm:px-8">
      {/* the print on the wall */}
      <button
        onClick={() => onOpen(hero.id)}
        className="print-card group relative block w-full max-w-[min(88vw,30rem)] cursor-pointer overflow-hidden shadow-[0_40px_80px_-30px_rgba(0,0,0,0.8)]"
        aria-label={`Open "${hero.title}" — ${hero.alt.slice(0, 80)}`}
      >
        <Image
          src={hero.src}
          alt={hero.alt || hero.title}
          width={hero.w}
          height={hero.h}
          priority
          className="slow-fade h-auto w-full"
          sizes="(max-width: 640px) 88vw, 30rem"
        />
      </button>

      <p className="fade-up font-archival mt-10 text-[10px] tracking-[0.4em] text-[#93a5ad]" style={{ animationDelay: '0.35s' }}>
        FENCE TO FACE · MILAN · 2026
      </p>

      <h1 className="fade-up font-serif-g mt-6 text-center text-4xl font-light italic text-[#e8e4da] sm:text-5xl md:text-6xl" style={{ animationDelay: '0.5s' }}>
        Dawit D. Seyoum
      </h1>

      <p className="fade-up font-serif-g mt-5 max-w-xl text-center text-lg leading-relaxed text-[#93a5ad] sm:text-xl" style={{ animationDelay: '0.65s' }}>
        “I observe, therefore I capture.”
      </p>

      <p className="fade-up font-sans-ui mt-6 max-w-xl text-center text-[13px] leading-relaxed text-[#93a5ad]/85 sm:text-sm" style={{ animationDelay: '0.8s' }}>
        A five-year photographic meditation on the delicate, ongoing negotiation
        between urban development and environmental resilience — shot in the city,
        written from its margins.
      </p>

      <div className="fade-up mt-10 flex flex-wrap items-center justify-center gap-4" style={{ animationDelay: '0.95s' }}>
        <button
          onClick={() => onNav('work')}
          className="font-sans-ui border border-white/20 px-7 py-3 text-[13px] tracking-wide text-[#e8e4da] transition-colors hover:border-[#c5402f] hover:text-white"
        >
          Enter the collection
        </button>
        <button
          onClick={() => onOpen(hero.id)}
          className="font-sans-ui flex items-center gap-2 px-4 py-3 text-[13px] tracking-wide text-[#93a5ad] transition-colors hover:text-[#e8e4da]"
        >
          <Feather className="h-3.5 w-3.5" aria-hidden />
          Read the first caption
        </button>
      </div>

      <p className="fade-up font-archival mt-12 text-center text-[10px] tracking-[0.25em] text-[#93a5ad]/60" style={{ animationDelay: '1.1s' }}>
        SELECTED BY THE EDITORS · LENSCULTURE STREET PHOTOGRAPHY AWARD 2025
      </p>

      <div className="fade-up absolute bottom-7 flex flex-col items-center gap-2 text-[#93a5ad]/50" style={{ animationDelay: '1.3s' }} aria-hidden>
        <span className="font-archival text-[9px] tracking-[0.35em]">SCROLL</span>
        <ArrowDown className="h-3.5 w-3.5 animate-bounce" />
      </div>
    </section>
  )
}
