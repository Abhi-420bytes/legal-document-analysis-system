import { useState, useRef } from 'react'
import Head from 'next/head'
import ResultsPanel from '../components/ResultsPanel'

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

const MODELS = [
  {
    id: 'model1',
    label: 'BART large-mnli',
    desc: '87.5% accuracy · Zero-shot · Fast',
    endpoint: '/analyze/model1',
    color: 'indigo',
  },
  {
    id: 'inlegal',
    label: 'InLegalBERT',
    desc: 'Indian legal fine-tuned · Best accuracy',
    endpoint: '/analyze/inlegal',
    color: 'emerald',
  },
  {
    id: 'ensemble',
    label: 'Ensemble',
    desc: 'BART × 0.9 + DeBERTa × 0.1',
    endpoint: '/analyze/ensemble',
    color: 'violet',
  },
]

const SAMPLE = `IN THE HIGH COURT OF DELHI AT NEW DELHI
Civil Suit No. 1234 of 2023

Between:
    ABC Constructions Pvt. Ltd.        ... Plaintiff
    Represented by its Director, Mr. Rajesh Kumar

    AND

    XYZ Developers Ltd.                ... Defendant
    Represented by its MD, Ms. Priya Sharma

Date of Filing: 15th January 2023

PLAINT

1. The Plaintiff entered into a contract dated 10th March 2022 with the Defendant
   for construction of residential apartments at Plot No. 45, Sector 18, Noida,
   Uttar Pradesh for a consideration of Rs. 2,50,00,000/-.

2. The Defendant breached the contract by failing to make payment of Rs. 75,00,000/-
   due on 30th September 2022.

3. The Plaintiff seeks compensation under Section 73 of the Indian Contract Act, 1872
   and an injunction restraining the Defendant from alienating the property.

4. Similar cases: AIR 2019 SC 1456, SCC 2020 Del 789`

export default function Home() {
  const [text, setText] = useState('')
  const [model, setModel] = useState('model1')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState('')
  const [fileName, setFileName] = useState('')
  const [dragOver, setDragOver] = useState(false)
  const fileRef = useRef()

  const selectedModel = MODELS.find(m => m.id === model)

  const callAPI = async (endpoint, body, isFormData = false) => {
    setLoading(true)
    setError('')
    setResult(null)
    try {
      const opts = isFormData
        ? { method: 'POST', body }
        : { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) }
      const resp = await fetch(`${API_BASE}${endpoint}`, opts)
      if (!resp.ok) {
        const err = await resp.json().catch(() => ({}))
        throw new Error(err.detail || `Server error ${resp.status}`)
      }
      setResult(await resp.json())
    } catch (e) {
      setError(e.message || 'Cannot reach backend. Start: uvicorn backend.api.colab_proxy:app --port 8000')
    } finally {
      setLoading(false)
    }
  }

  const handleAnalyze = () => {
    if (!text.trim()) return
    callAPI(selectedModel.endpoint, { text })
  }

  const handleFile = (file) => {
    if (!file) return
    const allowed = ['.pdf', '.docx', '.txt']
    const ext = '.' + file.name.split('.').pop().toLowerCase()
    if (!allowed.includes(ext)) {
      setError(`Unsupported file type "${ext}". Use PDF, DOCX, or TXT.`)
      return
    }
    setFileName(file.name)
    const fd = new FormData()
    fd.append('file', file)
    callAPI('/analyze/file', fd, true)
  }

  const modelBorderClass = {
    indigo: 'border-indigo-500 bg-indigo-50',
    emerald: 'border-emerald-500 bg-emerald-50',
    violet: 'border-violet-500 bg-violet-50',
  }
  const modelDotClass = {
    indigo: 'bg-indigo-500',
    emerald: 'bg-emerald-500',
    violet: 'bg-violet-500',
  }

  return (
    <>
      <Head>
        <title>Legal Document Analysis System</title>
        <meta name="description" content="Multi-Domain Legal Document Context Analysis using Transformer Models" />
        <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>⚖️</text></svg>" />
      </Head>

      <div className="min-h-screen flex flex-col">
        {/* ── Header ── */}
        <header className="bg-gradient-to-r from-indigo-900 to-indigo-800 text-white px-6 py-4 shadow-xl">
          <div className="max-w-7xl mx-auto flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold tracking-tight">⚖️ Legal Document Analysis System</h1>
              <p className="text-indigo-300 text-sm mt-0.5">
                Multi-Domain Legal Context Analysis &amp; Clause Identification · Transformer Models
              </p>
            </div>
            <div className="hidden sm:block text-right text-xs text-indigo-400 space-y-0.5">
              <p className="font-medium text-indigo-300">BTech Semester 6 · NLP Project</p>
              <p>BART · InLegalBERT · DeBERTa-v3-large</p>
            </div>
          </div>
        </header>

        <main className="flex-1 max-w-7xl mx-auto w-full px-4 py-8 space-y-6">

          {/* ── Input Card ── */}
          <div className="bg-white rounded-2xl shadow-sm border border-gray-200 p-6">
            <h2 className="text-base font-semibold text-gray-800 mb-4">Input Legal Document</h2>

            {/* Model selector */}
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 mb-5">
              {MODELS.map(m => (
                <label
                  key={m.id}
                  className={`flex items-start gap-3 p-3 rounded-xl border-2 cursor-pointer transition-all ${
                    model === m.id
                      ? modelBorderClass[m.color]
                      : 'border-gray-200 hover:border-gray-300 bg-white'
                  }`}
                >
                  <input
                    type="radio"
                    name="model"
                    value={m.id}
                    checked={model === m.id}
                    onChange={() => setModel(m.id)}
                    className="mt-1 accent-indigo-600"
                  />
                  <div>
                    <p className="font-semibold text-gray-800 text-sm leading-tight">{m.label}</p>
                    <p className="text-xs text-gray-500 mt-0.5">{m.desc}</p>
                  </div>
                  {model === m.id && (
                    <span className={`ml-auto mt-1 w-2 h-2 rounded-full shrink-0 ${modelDotClass[m.color]}`} />
                  )}
                </label>
              ))}
            </div>

            {/* Textarea */}
            <textarea
              className="w-full h-48 border border-gray-300 rounded-xl p-3 text-sm font-mono resize-none focus:outline-none focus:ring-2 focus:ring-indigo-400 focus:border-transparent placeholder-gray-400"
              placeholder="Paste legal document text here… or upload a PDF / DOCX / TXT below."
              value={text}
              onChange={e => setText(e.target.value)}
            />

            {/* Action bar */}
            <div className="flex flex-wrap items-center gap-3 mt-3">
              <button
                onClick={handleAnalyze}
                disabled={!text.trim() || loading}
                className="bg-indigo-600 hover:bg-indigo-700 disabled:opacity-40 disabled:cursor-not-allowed text-white font-semibold px-6 py-2.5 rounded-xl transition-colors shadow-sm"
              >
                {loading ? (
                  <span className="flex items-center gap-2">
                    <span className="w-4 h-4 border-2 border-white/40 border-t-white rounded-full animate-spin" />
                    Analyzing…
                  </span>
                ) : (
                  '⚖️ Analyze Document'
                )}
              </button>

              <button
                onClick={() => { setText(SAMPLE); setResult(null); setFileName(''); setError('') }}
                className="text-indigo-600 hover:text-indigo-800 text-sm font-medium underline underline-offset-2"
              >
                Load sample
              </button>

              <button
                onClick={() => { setText(''); setResult(null); setFileName(''); setError('') }}
                className="text-gray-400 hover:text-gray-600 text-sm"
              >
                Clear
              </button>

              {/* File drop zone */}
              <div
                className={`flex-1 min-w-[200px] border-2 border-dashed rounded-xl px-4 py-2.5 text-center text-sm cursor-pointer transition-colors ${
                  dragOver
                    ? 'border-indigo-400 bg-indigo-50 text-indigo-600'
                    : 'border-gray-300 text-gray-400 hover:border-indigo-400 hover:text-indigo-500'
                }`}
                onClick={() => fileRef.current.click()}
                onDragOver={e => { e.preventDefault(); setDragOver(true) }}
                onDragLeave={() => setDragOver(false)}
                onDrop={e => {
                  e.preventDefault()
                  setDragOver(false)
                  handleFile(e.dataTransfer.files[0])
                }}
              >
                {fileName
                  ? <span className="text-gray-700 font-medium">📄 {fileName}</span>
                  : '📎 Drop PDF / DOCX / TXT or click to upload'}
              </div>
              <input
                ref={fileRef}
                type="file"
                accept=".pdf,.docx,.txt"
                className="hidden"
                onChange={e => handleFile(e.target.files[0])}
              />
            </div>
          </div>

          {/* ── Error ── */}
          {error && (
            <div className="bg-red-50 border border-red-200 text-red-800 rounded-xl p-4 text-sm flex gap-2">
              <span className="shrink-0">⚠️</span>
              <span>{error}</span>
            </div>
          )}

          {/* ── Loading skeleton ── */}
          {loading && (
            <div className="bg-white rounded-2xl shadow-sm border border-gray-200 p-12 text-center">
              <div className="inline-flex items-center gap-3 text-gray-600">
                <span className="w-8 h-8 border-4 border-indigo-200 border-t-indigo-600 rounded-full animate-spin" />
                <div className="text-left">
                  <p className="font-medium">Analyzing with {selectedModel.label}…</p>
                  <p className="text-xs text-gray-400 mt-0.5">
                    First request may take 30–60 s if Colab is warming up
                  </p>
                </div>
              </div>
            </div>
          )}

          {/* ── Results ── */}
          {result && !loading && <ResultsPanel result={result} />}
        </main>

        <footer className="border-t border-gray-200 bg-white text-center text-xs text-gray-400 py-3">
          Legal Document Analysis System · NLP Project · BART · InLegalBERT · DeBERTa-v3
        </footer>
      </div>
    </>
  )
}
