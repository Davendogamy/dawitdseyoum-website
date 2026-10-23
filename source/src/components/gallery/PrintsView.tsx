'use client'

import { useState } from 'react'
import { Mail, Frame } from 'lucide-react'
import { CONTACT_EMAIL } from '@/data/photos'
import { useToast } from '@/hooks/use-toast'

export function PrintsView() {
  const { toast } = useToast()
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [piece, setPiece] = useState('')
  const [message, setMessage] = useState('')

  const submit = (e: React.FormEvent) => {
    e.preventDefault()
    const subject = encodeURIComponent(`Print enquiry — ${piece || 'the collection'} (${name})`)
    const body = encodeURIComponent(
      `Name: ${name}\nEmail: ${email}\nPiece: ${piece}\n\n${message}\n\n— sent from dawitdseyoum.com`
    )
    window.location.href = `mailto:${CONTACT_EMAIL}?subject=${subject}&body=${body}`
    toast({
      title: 'Enquiry prepared',
      description: 'Your mail client is opening with the enquiry pre-filled.',
    })
  }

  const inputCls =
    'font-sans-ui w-full border border-white/12 bg-white/[0.03] px-4 py-3 text-[14px] text-[#e8e4da] placeholder:text-[#93a5ad]/50 outline-none transition-colors focus:border-[#c5402f]/60'
  const labelCls = 'font-archival mb-2 block text-[10px] tracking-[0.3em] text-[#93a5ad]'

  return (
    <div className="mx-auto max-w-5xl px-5 pb-24 pt-32 sm:px-8">
      <p className="font-archival text-[10px] tracking-[0.4em] text-[#93a5ad]">PRINTS</p>
      <h1 className="font-serif-g mt-4 text-4xl font-light text-[#e8e4da] sm:text-5xl">Collect the work</h1>
      <p className="font-serif-g mt-5 max-w-2xl text-lg leading-relaxed text-[#93a5ad]">
        Every piece in the collection is available as a fine-art A4 print — the
        format the work was made for: archival pigment on matte paper, presented on
        a deep color field with a white mat and the artist&apos;s archival
        reference. Each print is signed and catalogued by hand.
      </p>

      <div className="mt-14 grid gap-14 lg:grid-cols-[1fr_1.1fr]">
        {/* format notes */}
        <div>
          <div className="flex items-start gap-4 border border-white/8 bg-white/[0.02] p-6">
            <Frame className="mt-1 h-5 w-5 shrink-0 text-[#c5402f]" aria-hidden />
            <div>
              <h2 className="font-serif-g text-xl text-[#e8e4da]">The A4 presentation</h2>
              <p className="font-serif-g mt-3 text-[15px] leading-relaxed text-[#93a5ad]">
                The print arrives as you see it here: image set within its mat and
                color field, credit line by the artist. Framing recommendations and
                larger formats are available on request.
              </p>
            </div>
          </div>

          <div className="mt-6 flex items-start gap-4 border border-white/8 bg-white/[0.02] p-6">
            <Mail className="mt-1 h-5 w-5 shrink-0 text-[#c5402f]" aria-hidden />
            <div>
              <h2 className="font-serif-g text-xl text-[#e8e4da]">Enquiries &amp; licensing</h2>
              <p className="font-serif-g mt-3 text-[15px] leading-relaxed text-[#93a5ad]">
                Curators, galleries and publications are welcome. Use the form — it
                opens a pre-filled enquiry to the studio — or reach out through any
                of the social channels listed in the About page.
              </p>
            </div>
          </div>
        </div>

        {/* enquiry form */}
        <form onSubmit={submit} className="border border-white/8 bg-white/[0.02] p-7 sm:p-9">
          <div className="space-y-6">
            <div>
              <label htmlFor="p-name" className={labelCls}>NAME</label>
              <input id="p-name" required value={name} onChange={(e) => setName(e.target.value)}
                placeholder="Your name" className={inputCls} />
            </div>
            <div>
              <label htmlFor="p-email" className={labelCls}>EMAIL</label>
              <input id="p-email" required type="email" value={email} onChange={(e) => setEmail(e.target.value)}
                placeholder="you@example.com" className={inputCls} />
            </div>
            <div>
              <label htmlFor="p-piece" className={labelCls}>PIECE OF INTEREST</label>
              <input id="p-piece" value={piece} onChange={(e) => setPiece(e.target.value)}
                placeholder='e.g. "Fence to face", 2026' className={inputCls} />
            </div>
            <div>
              <label htmlFor="p-msg" className={labelCls}>MESSAGE</label>
              <textarea id="p-msg" rows={5} value={message} onChange={(e) => setMessage(e.target.value)}
                placeholder="Format, framing, delivery — anything on your mind."
                className={`${inputCls} resize-none`} />
            </div>
            <button
              type="submit"
              className="font-sans-ui w-full border border-[#c5402f]/70 bg-[#c5402f]/10 px-6 py-3.5 text-[13px] tracking-wide text-[#e8e4da] transition-colors hover:bg-[#c5402f]/25"
            >
              Send enquiry
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}
