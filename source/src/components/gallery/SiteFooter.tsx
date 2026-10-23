'use client'

import { SOCIALS } from '@/data/photos'

export function SiteFooter() {
  return (
    <footer className="mt-auto border-t border-white/5">
      <div className="mx-auto grid max-w-6xl gap-8 px-5 py-12 sm:px-8 md:grid-cols-3">
        <div>
          <p className="font-serif-g text-lg italic leading-relaxed text-[#e8e4da]/80">
            “I observe, therefore I capture.”
          </p>
        </div>
        <div className="font-sans-ui flex flex-wrap items-start gap-x-6 gap-y-2 md:justify-center">
          {SOCIALS.map((s) => (
            <a
              key={s.name}
              href={s.url}
              target="_blank"
              rel="noopener noreferrer"
              className="text-[12px] tracking-wide text-[#93a5ad] transition-colors hover:text-[#e8e4da]"
            >
              {s.name} ↗
            </a>
          ))}
        </div>
        <div className="md:text-right">
          <p className="font-archival text-[10px] tracking-[0.25em] text-[#93a5ad]/70">
            © {new Date().getFullYear()} DAWIT D. SEYOUM
          </p>
          <p className="font-archival mt-2 text-[10px] tracking-[0.25em] text-[#93a5ad]/40">
            ALL RIGHTS RESERVED · EYE IN THE CITY
          </p>
        </div>
      </div>
    </footer>
  )
}
