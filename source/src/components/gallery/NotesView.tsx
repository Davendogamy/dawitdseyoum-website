'use client'

import { Leaf, PenLine } from 'lucide-react'

export function NotesView() {
  return (
    <div className="mx-auto max-w-3xl px-5 pb-24 pt-32 sm:px-8">
      <p className="font-archival text-[10px] tracking-[0.4em] text-[#93a5ad]">FIELD NOTES</p>
      <h1 className="font-serif-g mt-4 text-4xl font-light text-[#e8e4da] sm:text-5xl">
        Written from the margins
      </h1>
      <p className="font-serif-g mt-5 text-lg leading-relaxed text-[#93a5ad]">
        Short philosophical entries — personal, observational, grounded in what the
        city actually does. The photographs watch; the notes think.
      </p>

      <article className="fade-up mt-16 border-t border-white/8 pt-12">
        <p className="font-archival text-[10px] tracking-[0.3em] text-[#93a5ad]/70">
          NOTE No. 1 · APRIL 2026
        </p>
        <h2 className="font-serif-g mt-4 text-3xl font-light italic text-[#e8e4da]">
          The tree wrapped in wire
        </h2>
        <div className="font-serif-g mt-8 space-y-6 text-[19px] leading-relaxed text-[#e8e4da]/95">
          <p>
            The tree wrapped in wire vs the bird at its base. That something
            naturally integrated into its environment tends to sustain itself.
          </p>
          <p>
            And something externally managed, optimized, or controlled often breaks
            that balance — even if it looks cleaner, more efficient, more
            “advanced.”
          </p>
        </div>
        <p className="font-archival mt-8 flex items-center gap-2 text-[10px] tracking-[0.25em] text-[#c5402f]">
          <Leaf className="h-3.5 w-3.5" aria-hidden /> FROM THE ARCHIVE · DADASESE69
        </p>
      </article>

      <article className="mt-16 border-t border-dashed border-white/12 pt-12">
        <div className="flex items-center gap-3">
          <PenLine className="h-4 w-4 text-[#93a5ad]" aria-hidden />
          <h2 className="font-serif-g text-2xl font-light italic text-[#93a5ad]">
            Further notes are being typeset
          </h2>
        </div>
        <p className="font-serif-g mt-4 max-w-xl text-[15px] leading-relaxed text-[#93a5ad]/80">
          Entries on witnessing, on the price of rain, on the crow who could not
          find a tree — the written companions to the collection — will appear here
          as they are prepared for publication.
        </p>
      </article>
    </div>
  )
}
