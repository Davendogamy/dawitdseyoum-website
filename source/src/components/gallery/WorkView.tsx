'use client'

import Image from 'next/image'
import { motion } from 'framer-motion'
import { photos, seriesMeta, type Photo, type SeriesId } from '@/data/photos'

const ORDER: SeriesId[] = ['witnesses', 'builders', 'commons']

function Wall({ series, onOpen }: { series: SeriesId; onOpen: (id: string) => void }) {
  const meta = seriesMeta[series]
  const items = photos.filter((p) => p.series === series)

  return (
    <section className="px-5 py-20 sm:px-8" style={{ backgroundColor: meta.bg }}>
      <div className="mx-auto max-w-6xl">
        <div className="mb-12 max-w-2xl">
          <p className="font-archival text-[10px] tracking-[0.4em] text-[#c5402f]">
            {series.toUpperCase()} · {items.length} WORKS
          </p>
          <h2 className="font-serif-g mt-4 text-4xl font-light text-[#e8e4da] sm:text-5xl">{meta.name}</h2>
          <p className="font-serif-g mt-2 text-xl italic text-[#93a5ad]">{meta.tagline}</p>
          <p className="font-serif-g mt-6 text-[17px] leading-relaxed text-[#93a5ad]/90">{meta.note}</p>
        </div>

        <div className="columns-1 gap-7 sm:columns-2 lg:columns-3">
          {items.map((p: Photo, i: number) => (
            <motion.figure
              key={p.id}
              initial={{ opacity: 0, y: 16 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, margin: '0px 0px -40px 0px' }}
              transition={{ duration: 0.6, delay: (i % 3) * 0.08 }}
              className="mb-9 break-inside-avoid"
            >
              <button
                onClick={() => onOpen(p.id)}
                className="print-card group block w-full text-left shadow-[0_24px_50px_-24px_rgba(0,0,0,0.75)] ring-1 ring-white/5"
                aria-label={`Open "${p.title}"`}
              >
                <Image
                  src={p.src}
                  alt={p.alt || p.title}
                  width={p.w}
                  height={p.h}
                  className="h-auto w-full"
                  sizes="(max-width: 640px) 92vw, (max-width: 1024px) 45vw, 30vw"
                />
              </button>
              <figcaption className="mt-3 flex items-baseline justify-between gap-3">
                <span className="font-serif-g truncate text-[15px] italic text-[#e8e4da]/85">{p.title}</span>
                <span className="font-archival shrink-0 text-[10px] tracking-wider text-[#93a5ad]/70">
                  {p.date.slice(0, 4)}
                </span>
              </figcaption>
            </motion.figure>
          ))}
        </div>
      </div>
    </section>
  )
}

export function WorkView({ onOpen }: { onOpen: (id: string) => void }) {
  return (
    <div>
      <div className="px-5 pb-4 pt-32 sm:px-8">
        <div className="mx-auto max-w-6xl">
          <p className="font-archival text-[10px] tracking-[0.4em] text-[#93a5ad]">THE COLLECTION</p>
          <h1 className="font-serif-g mt-4 text-4xl font-light text-[#e8e4da] sm:text-5xl">The Work</h1>
          <p className="font-serif-g mt-5 max-w-2xl text-lg leading-relaxed text-[#93a5ad]">
            Eighty-nine pieces, organized by motif rather than chronology. Every
            photograph carries its written wall label — title, archival reference,
            and the caption the work was made with. Click any print to read it.
          </p>
        </div>
      </div>
      {ORDER.map((s) => (
        <Wall key={s} series={s} onOpen={onOpen} />
      ))}
    </div>
  )
}
