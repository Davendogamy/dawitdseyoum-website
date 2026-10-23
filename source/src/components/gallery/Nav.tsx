'use client'

import { useEffect, useState } from 'react'

export type View = 'home' | 'work' | 'notes' | 'about' | 'prints'

const LINKS: { id: View; label: string }[] = [
  { id: 'work', label: 'The Work' },
  { id: 'notes', label: 'Field Notes' },
  { id: 'about', label: 'About' },
  { id: 'prints', label: 'Prints' },
]

export function Nav({ view, onNav }: { view: View; onNav: (v: View) => void }) {
  const [scrolled, setScrolled] = useState(false)
  const [open, setOpen] = useState(false)

  useEffect(() => {
    const fn = () => setScrolled(window.scrollY > 24)
    window.addEventListener('scroll', fn, { passive: true })
    fn()
    return () => window.removeEventListener('scroll', fn)
  }, [])

  const go = (v: View) => {
    onNav(v)
    setOpen(false)
  }

  return (
    <header
      className={`fixed inset-x-0 top-0 z-40 transition-colors duration-500 ${
        scrolled || open
          ? 'bg-[#0b131b]/92 backdrop-blur-md border-b border-white/5'
          : 'bg-transparent border-b border-transparent'
      }`}
    >
      <div className="mx-auto flex max-w-6xl items-center justify-between px-5 py-4 sm:px-8">
        <button
          onClick={() => go('home')}
          className="group flex items-center gap-2.5 text-left"
          aria-label="Dawit D. Seyoum — home"
        >
          <span className="red-dot inline-block h-1.5 w-1.5 rounded-full bg-[#c5402f]" aria-hidden />
          <span className="font-archival text-[11px] font-medium tracking-[0.32em] text-[#e8e4da] sm:text-xs">
            DAWIT&nbsp;D.&nbsp;SEYOUM
          </span>
        </button>

        {/* desktop */}
        <nav className="hidden items-center gap-8 md:flex" aria-label="Primary">
          {LINKS.map((l) => (
            <button
              key={l.id}
              onClick={() => go(l.id)}
              className={`font-sans-ui text-[13px] tracking-wide transition-colors ${
                view === l.id
                  ? 'text-[#e8e4da] underline decoration-[#c5402f] decoration-1 underline-offset-8'
                  : 'text-[#93a5ad] hover:text-[#e8e4da]'
              }`}
            >
              {l.label}
            </button>
          ))}
        </nav>

        {/* mobile toggle */}
        <button
          className="flex h-10 w-10 items-center justify-center text-[#e8e4da] md:hidden"
          onClick={() => setOpen((o) => !o)}
          aria-expanded={open}
          aria-label={open ? 'Close menu' : 'Open menu'}
        >
          <div className="space-y-1.5">
            <span className={`block h-px w-6 bg-current transition-transform ${open ? 'translate-y-[7px] rotate-45' : ''}`} />
            <span className={`block h-px w-6 bg-current transition-opacity ${open ? 'opacity-0' : ''}`} />
            <span className={`block h-px w-6 bg-current transition-transform ${open ? '-translate-y-[7px] -rotate-45' : ''}`} />
          </div>
        </button>
      </div>

      {/* mobile menu */}
      {open && (
        <nav className="border-t border-white/5 bg-[#0b131b]/97 px-6 py-4 md:hidden" aria-label="Mobile">
          {LINKS.map((l) => (
            <button
              key={l.id}
              onClick={() => go(l.id)}
              className={`block w-full py-3 text-left font-sans-ui text-sm tracking-wide ${
                view === l.id ? 'text-[#e8e4da]' : 'text-[#93a5ad]'
              }`}
            >
              {l.label}
            </button>
          ))}
        </nav>
      )}
    </header>
  )
}
