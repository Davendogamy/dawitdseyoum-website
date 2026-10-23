'use client'

import { useCallback, useState } from 'react'
import { AnimatePresence, motion } from 'framer-motion'
import { photos } from '@/data/photos'
import { Nav, type View } from '@/components/gallery/Nav'
import { HomeView } from '@/components/gallery/HomeView'
import { WorkView } from '@/components/gallery/WorkView'
import { NotesView } from '@/components/gallery/NotesView'
import { AboutView } from '@/components/gallery/AboutView'
import { PrintsView } from '@/components/gallery/PrintsView'
import { SiteFooter } from '@/components/gallery/SiteFooter'
import { Lightbox, type LightboxState } from '@/components/gallery/Lightbox'

export default function Page() {
  const [view, setView] = useState<View>('home')
  const [lightbox, setLightbox] = useState<LightboxState | null>(null)

  const nav = useCallback((v: View) => {
    setView(v)
    window.scrollTo({ top: 0, behavior: 'instant' as ScrollBehavior })
  }, [])

  /** open a piece; scope the list to its series so arrows stay in-series,
   *  except the homepage hero which walks the entire collection */
  const openById = useCallback((id: string, scope: 'all' | 'series' = 'series') => {
    const idx = photos.findIndex((p) => p.id === id)
    if (idx < 0) return
    const photo = photos[idx]
    const list = scope === 'all' ? photos : photos.filter((p) => p.series === photo.series)
    setLightbox({ list, index: list.findIndex((p) => p.id === id) })
  }, [])

  return (
    <div className="flex min-h-screen flex-col bg-[#0b131b]">
      <Nav view={view} onNav={nav} />

      <main className="flex-1">
        <AnimatePresence mode="wait">
          <motion.div
            key={view}
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.35 }}
          >
            {view === 'home' && (
              <HomeView onNav={nav} onOpen={(id) => openById(id, 'all')} />
            )}
            {view === 'work' && <WorkView onOpen={(id) => openById(id, 'series')} />}
            {view === 'notes' && <NotesView />}
            {view === 'about' && <AboutView onNav={nav} />}
            {view === 'prints' && <PrintsView />}
          </motion.div>
        </AnimatePresence>
      </main>

      <SiteFooter />

      <Lightbox
        state={lightbox}
        onClose={() => setLightbox(null)}
        onNavigate={setLightbox}
      />
    </div>
  )
}
