'use client'

import Image from 'next/image'
import { Quote } from 'lucide-react'
import { SOCIALS } from '@/data/photos'
import type { View } from './Nav'

const FACTS: [string, string][] = [
  ['WORKING', 'Five-year ongoing urban project'],
  ['BASE', 'Milan, Italy · Oxford, United Kingdom'],
  ['CAMERA', 'Nikon Z 6II · vintage manual glass — Vivitar 70–210 macro, Hanimex TA 135mm f/2.8, Photax–Paragon 85–210mm'],
  ['RECOGNITION', "LensCulture Street Photography Award 2025 — selected by the editors for the online Competition Gallery"],
]

export function AboutView({ onNav }: { onNav: (v: View) => void }) {
  return (
    <div className="mx-auto max-w-5xl px-5 pb-24 pt-32 sm:px-8">
      <p className="font-archival text-[10px] tracking-[0.4em] text-[#93a5ad]">ABOUT</p>

      <div className="mt-10 grid gap-14 lg:grid-cols-[300px_1fr]">
        {/* portrait column */}
        <div>
          <div className="relative w-40 overflow-hidden rounded-full ring-1 ring-white/10">
            <Image
              src="/images/avatar.webp"
              alt="Dawit D. Seyoum — portrait"
              width={400}
              height={400}
              className="h-auto w-full"
              sizes="160px"
            />
          </div>
          <h1 className="font-serif-g mt-6 text-3xl font-light text-[#e8e4da]">Dawit D. Seyoum</h1>
          <p className="font-archival mt-2 text-[10px] tracking-[0.25em] text-[#93a5ad]">
            PHOTOGRAPHER · OBSERVER · ALSO KNOWN AS DADASESE69
          </p>

          <blockquote className="mt-8 border-l-2 border-[#c5402f] pl-4">
            <p className="font-serif-g text-lg italic leading-relaxed text-[#e8e4da]/90">
              “I observe, therefore I capture.”
            </p>
          </blockquote>

          <div className="mt-8 space-y-2">
            {SOCIALS.map((s) => (
              <a
                key={s.name}
                href={s.url}
                target="_blank"
                rel="noopener noreferrer"
                className="font-sans-ui block text-[12px] tracking-wide text-[#93a5ad] transition-colors hover:text-[#e8e4da]"
              >
                {s.name} ↗
              </a>
            ))}
          </div>
        </div>

        {/* statement column */}
        <div>
          <h2 className="font-serif-g text-2xl font-light italic text-[#e8e4da] sm:text-3xl">
            On development and environmental resilience
          </h2>

          <div className="font-serif-g mt-7 space-y-6 text-[19px] leading-relaxed text-[#e8e4da]/92">
            <p>
              This is a body of work about the intrinsic, ongoing play between
              development and environmental resilience — photographed over five
              years in one city, and written from its margins. It is a personal,
              reflective record of what the city builds, what it removes, and what
              quietly refuses to leave.
            </p>
            <p>
              Something naturally integrated into its environment tends to sustain
              itself. Something externally managed, optimized, controlled often
              breaks that balance — even when it looks cleaner, more efficient, more
              “advanced.” The photographs keep the ledger: a heron holding its ground
              on a rooftop against the geometry of progress; a tree wrapped in wire;
              water sold back to us in bottles; a crow unable to find a tree to raise
              its young.
            </p>
            <p>
              The captions are not decoration. They are half the work — the moment
              the microphone passes to the city&apos;s non-human residents. The heron
              answers every gaze. The crane asks why we reach for the universe by
              piling stone upon stone. The pigeon comments on how man has convinced
              steps to dress up and roam the streets. Read them slowly.
            </p>
          </div>

          <div className="mt-12 border-t border-white/8 pt-8">
            <dl className="space-y-5">
              {FACTS.map(([k, v]) => (
                <div key={k} className="grid gap-1 sm:grid-cols-[120px_1fr] sm:gap-6">
                  <dt className="font-archival text-[10px] tracking-[0.3em] text-[#c5402f] sm:pt-1">{k}</dt>
                  <dd className="font-sans-ui text-[13px] leading-relaxed text-[#93a5ad]">{v}</dd>
                </div>
              ))}
            </dl>
          </div>

          <div className="mt-12 flex flex-wrap gap-4">
            <button
              onClick={() => onNav('work')}
              className="font-sans-ui border border-white/20 px-6 py-3 text-[13px] tracking-wide text-[#e8e4da] transition-colors hover:border-[#c5402f]"
            >
              See the work
            </button>
            <button
              onClick={() => onNav('prints')}
              className="font-sans-ui px-6 py-3 text-[13px] tracking-wide text-[#93a5ad] transition-colors hover:text-[#e8e4da]"
            >
              Collect a print →
            </button>
          </div>
        </div>
      </div>

      <div className="mt-20 flex items-center gap-3 border-t border-white/8 pt-10 text-[#93a5ad]/60">
        <Quote className="h-4 w-4" aria-hidden />
        <p className="font-serif-g text-sm italic">
          A world without birds, is a world without photographers.
        </p>
      </div>
    </div>
  )
}
