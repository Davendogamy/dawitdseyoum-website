'use client'

import { useCallback, useEffect } from 'react'
import Image from 'next/image'
import { motion, AnimatePresence } from 'framer-motion'
import { X, ChevronLeft, ChevronRight, ArrowUpRight } from 'lucide-react'
import { photos, seriesMeta, type Photo } from '@/data/photos'

export interface LightboxState {
  list: Photo[]
  index: number
}

export function Lightbox({
  state,
  onClose,
  onNavigate,
}: {
  state: LightboxState | null
  onClose: () => void
  onNavigate: (s: LightboxState) => void
}) {
  const photo = state ? state.list[state.index] : null

  const go = useCallback(
    (dir: 1 | -1) => {
      if (!state) return
      const next = (state.index + dir + state.list.length) % state.list.length
      onNavigate({ ...state, index: next })
    },
    [state, onNavigate]
  )

  useEffect(() => {
    if (!state) return
    const fn = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose()
      if (e.key === 'ArrowRight') go(1)
      if (e.key === 'ArrowLeft') go(-1)
    }
    window.addEventListener('keydown', fn)
    document.body.style.overflow = 'hidden'
    return () => {
      window.removeEventListener('keydown', fn)
      document.body.style.overflow = ''
    }
  }, [state, onClose, go])

  return (
    <AnimatePresence>
      {state && photo && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          transition={{ duration: 0.3 }}
          className="fixed inset-0 z-50 bg-[#0b131b]/97 backdrop-blur-sm"
          onClick={onClose}
          role="dialog"
          aria-modal="true"
          aria-label={photo.title}
        >
          <div
            className="mx-auto flex h-full max-w-6xl flex-col overflow-hidden lg:flex-row lg:items-stretch lg:gap-10 lg:px-8"
            onClick={(e) => e.stopPropagation()}
          >
            {/* the print */}
            <div className="relative flex min-h-0 flex-1 items-center justify-center px-4 pt-16 lg:pt-20">
              <motion.div
                key={photo.id}
                initial={{ opacity: 0, scale: 0.97 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.45, ease: [0.22, 1, 0.36, 1] }}
                className="relative max-h-full"
              >
                <Image
                  src={photo.src}
                  alt={photo.alt || photo.title}
                  width={photo.w}
                  height={photo.h}
                  priority
                  className="max-h-[52vh] w-auto object-contain shadow-[0_40px_90px_-30px_rgba(0,0,0,0.9)] lg:max-h-[86vh]"
                  sizes="(max-width: 1024px) 92vw, 55vw"
                />
              </motion.div>

              {/* prev / next */}
              <button
                onClick={() => go(-1)}
                className="absolute left-3 top-1/2 flex h-11 w-11 -translate-y-1/2 items-center justify-center rounded-full border border-white/10 bg-[#0b131b]/70 text-[#e8e4da] transition-colors hover:border-[#c5402f] lg:left-6"
                aria-label="Previous work"
              >
                <ChevronLeft className="h-5 w-5" />
              </button>
              <button
                onClick={() => go(1)}
                className="absolute right-3 top-1/2 flex h-11 w-11 -translate-y-1/2 items-center justify-center rounded-full border border-white/10 bg-[#0b131b]/70 text-[#e8e4da] transition-colors hover:border-[#c5402f] lg:right-6"
                aria-label="Next work"
              >
                <ChevronRight className="h-5 w-5" />
              </button>
            </div>

            {/* the wall label */}
            <motion.aside
              key={photo.id + '-label'}
              initial={{ opacity: 0, y: 12 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.45, delay: 0.1 }}
              className="wall-scroll min-h-0 shrink-0 overflow-y-auto border-t border-white/8 px-6 py-6 lg:w-[400px] lg:border-l lg:border-t-0 lg:px-8 lg:py-24"
            >
              <p className="font-archival text-[10px] tracking-[0.35em] text-[#c5402f]">
                {seriesMeta[photo.series].name.toUpperCase()}
              </p>
              <h2 className="font-serif-g mt-3 text-3xl font-light italic leading-tight text-[#e8e4da]">
                {photo.title}
              </h2>
              <p className="font-archival mt-3 text-[10px] leading-relaxed tracking-[0.14em] text-[#93a5ad]/80">
                {photo.fileId || 'ARCHIVE'} · {photo.date} {photo.time ? `· ${photo.time}` : ''}
              </p>

              {photo.caption && (
                <p className="font-serif-g mt-6 whitespace-pre-line text-[17px] leading-relaxed text-[#e8e4da]/95">
                  {photo.caption}
                </p>
              )}

              {photo.alt && photo.alt !== photo.caption && (
                <div className="mt-6 border-t border-white/8 pt-5">
                  <p className="font-archival text-[9px] tracking-[0.3em] text-[#93a5ad]/70">GALLERY NOTE</p>
                  <p className="font-serif-g mt-2 text-sm leading-relaxed text-[#93a5ad]">{photo.alt}</p>
                </div>
              )}

              {photo.tags.length > 0 && (
                <div className="mt-6 flex flex-wrap gap-2">
                  {photo.tags.map((t) => (
                    <span key={t} className="font-archival border border-white/10 px-2 py-1 text-[9px] tracking-wider text-[#93a5ad]/80">
                      #{t}
                    </span>
                  ))}
                </div>
              )}

              <a
                href={photo.bskyUrl}
                target="_blank"
                rel="noopener noreferrer"
                className="font-sans-ui mt-8 inline-flex items-center gap-1.5 text-[12px] tracking-wide text-[#93a5ad] transition-colors hover:text-[#e8e4da]"
              >
                View source post <ArrowUpRight className="h-3.5 w-3.5" aria-hidden />
              </a>

              <p className="font-archival mt-10 text-[10px] tracking-[0.25em] text-[#93a5ad]/50">
                {state.index + 1} / {state.list.length}
              </p>
            </motion.aside>
          </div>

          <button
            onClick={onClose}
            className="absolute right-4 top-4 flex h-11 w-11 items-center justify-center rounded-full border border-white/10 bg-[#0b131b]/70 text-[#e8e4da] transition-colors hover:border-[#c5402f]"
            aria-label="Close"
          >
            <X className="h-5 w-5" />
          </button>
        </motion.div>
      )}
    </AnimatePresence>
  )
}
