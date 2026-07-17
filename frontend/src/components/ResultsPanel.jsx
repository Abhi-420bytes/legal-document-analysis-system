// Results display for Legal Document Analysis

const CASE_META = {
  criminal:              { label: 'Criminal Law',           emoji: '🚔', bg: 'bg-red-50',     text: 'text-red-800',    border: 'border-red-300',    bar: 'bg-red-500',    badge: 'bg-red-600'    },
  civil:                 { label: 'Civil Law',              emoji: '⚖️', bg: 'bg-blue-50',    text: 'text-blue-800',   border: 'border-blue-300',   bar: 'bg-blue-500',   badge: 'bg-blue-600'   },
  contract_dispute:      { label: 'Contract Dispute',       emoji: '📝', bg: 'bg-orange-50',  text: 'text-orange-800', border: 'border-orange-300', bar: 'bg-orange-500', badge: 'bg-orange-600' },
  family_law:            { label: 'Family Law',             emoji: '👪', bg: 'bg-pink-50',    text: 'text-pink-800',   border: 'border-pink-300',   bar: 'bg-pink-500',   badge: 'bg-pink-600'   },
  property:              { label: 'Property Law',           emoji: '🏠', bg: 'bg-green-50',   text: 'text-green-800',  border: 'border-green-300',  bar: 'bg-green-500',  badge: 'bg-green-600'  },
  constitutional:        { label: 'Constitutional Law',     emoji: '🏛️', bg: 'bg-purple-50',  text: 'text-purple-800', border: 'border-purple-300', bar: 'bg-purple-500', badge: 'bg-purple-600' },
  intellectual_property: { label: 'Intellectual Property', emoji: '💡', bg: 'bg-teal-50',    text: 'text-teal-800',   border: 'border-teal-300',   bar: 'bg-teal-500',   badge: 'bg-teal-600'   },
  labour:                { label: 'Labour Law',             emoji: '👷', bg: 'bg-yellow-50',  text: 'text-yellow-800', border: 'border-yellow-300', bar: 'bg-yellow-500', badge: 'bg-yellow-600' },
}
const DEFAULT_META = { label: 'Unknown', emoji: '❓', bg: 'bg-gray-50', text: 'text-gray-800', border: 'border-gray-300', bar: 'bg-gray-400', badge: 'bg-gray-500' }

// ── Case Type Card ────────────────────────────────────────────────────────────
function CaseTypeCard({ cls }) {
  const type = cls?.case_type || 'unknown'
  const conf = cls?.confidence || 0
  const meta = CASE_META[type] || DEFAULT_META
  const pct  = Math.round(conf * 100)

  return (
    <div className={`rounded-2xl border-2 p-5 ${meta.bg} ${meta.border}`}>
      <p className="text-xs font-bold uppercase tracking-widest text-gray-400 mb-2">Detected Case Type</p>
      <div className="flex items-center justify-between mb-3">
        <div>
          <span className="text-3xl mr-2">{meta.emoji}</span>
          <span className={`text-xl font-bold ${meta.text}`}>{meta.label}</span>
        </div>
        <span className={`text-white font-bold text-sm px-3 py-1.5 rounded-full ${meta.badge}`}>
          {pct}%
        </span>
      </div>
      <div className="w-full bg-white bg-opacity-60 rounded-full h-2.5 mb-2">
        <div className={`h-2.5 rounded-full transition-all duration-700 ${meta.bar}`} style={{ width: `${pct}%` }} />
      </div>
      {cls?.model && (
        <p className="text-xs text-gray-400 mt-2">Model: <span className="font-medium text-gray-600">{cls.model}</span></p>
      )}
    </div>
  )
}

// ── All Class Scores ──────────────────────────────────────────────────────────
function ScoresChart({ allScores }) {
  if (!allScores || Object.keys(allScores).length === 0) return null
  const sorted = Object.entries(allScores).sort((a, b) => b[1] - a[1])

  return (
    <div className="bg-white rounded-2xl border border-gray-200 p-5">
      <h3 className="text-sm font-semibold text-gray-700 mb-3">All Class Probabilities</h3>
      <div className="space-y-2">
        {sorted.map(([label, score]) => {
          const meta = CASE_META[label] || DEFAULT_META
          const pct  = Math.round(score * 100)
          return (
            <div key={label} className="flex items-center gap-2">
              <span className="text-xs text-gray-500 w-36 shrink-0 capitalize">{meta.emoji} {label.replace(/_/g, ' ')}</span>
              <div className="flex-1 bg-gray-100 rounded-full h-1.5">
                <div className={`h-1.5 rounded-full ${meta.bar}`} style={{ width: `${pct}%` }} />
              </div>
              <span className="text-xs text-gray-400 w-8 text-right">{pct}%</span>
            </div>
          )
        })}
      </div>
    </div>
  )
}

// ── Entities ─────────────────────────────────────────────────────────────────
const ENTITY_CONFIG = [
  { key: 'persons',          label: 'Persons',          icon: '👤', color: 'bg-blue-100 text-blue-800 border-blue-200'    },
  { key: 'organizations',    label: 'Organizations',    icon: '🏛️', color: 'bg-purple-100 text-purple-800 border-purple-200' },
  { key: 'locations',        label: 'Locations',        icon: '📍', color: 'bg-green-100 text-green-800 border-green-200'  },
  { key: 'dates',            label: 'Dates',            icon: '📅', color: 'bg-yellow-100 text-yellow-800 border-yellow-200' },
  { key: 'legal_sections',   label: 'Legal Sections',   icon: '§',  color: 'bg-red-100 text-red-800 border-red-200'        },
  { key: 'case_citations',   label: 'Case Citations',   icon: '⚖️', color: 'bg-indigo-100 text-indigo-800 border-indigo-200' },
  { key: 'monetary_amounts', label: 'Monetary Amounts', icon: '₹',  color: 'bg-emerald-100 text-emerald-800 border-emerald-200' },
]

function EntitiesCard({ entities }) {
  if (!entities) return null

  const hasData = ENTITY_CONFIG.some(({ key }) => {
    const v = entities[key]
    return v && v.length > 0
  })
  if (!hasData) return null

  return (
    <div className="bg-white rounded-2xl border border-gray-200 p-5">
      <h3 className="text-sm font-semibold text-gray-700 mb-4">Detected Entities</h3>
      <div className="space-y-3">
        {ENTITY_CONFIG.map(({ key, label, icon, color }) => {
          const items = entities[key]
          if (!items || items.length === 0) return null
          return (
            <div key={key}>
              <p className="text-xs font-semibold text-gray-400 uppercase tracking-wide mb-1.5">
                {icon} {label}
              </p>
              <div className="flex flex-wrap gap-1.5">
                {items.map((item, i) => {
                  const display = typeof item === 'string' ? item : item.text
                  const score   = typeof item === 'object' && item.score ? `Score: ${Math.round(item.score * 100)}%` : null
                  return (
                    <span
                      key={i}
                      title={score}
                      className={`text-xs px-2 py-1 rounded-lg border font-medium ${color}`}
                    >
                      {display}
                    </span>
                  )
                })}
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}

// ── Clauses ───────────────────────────────────────────────────────────────────
const CLAUSE_META = {
  indemnity:       { icon: '🛡️', label: 'Indemnity'            },
  termination:     { icon: '🔚', label: 'Termination'          },
  arbitration:     { icon: '🤝', label: 'Arbitration'          },
  force_majeure:   { icon: '🌪️', label: 'Force Majeure'        },
  jurisdiction:    { icon: '🏛️', label: 'Jurisdiction'         },
  penalty:         { icon: '💰', label: 'Penalty / Damages'    },
  liability_limit: { icon: '🔒', label: 'Liability Limit'      },
  confidentiality: { icon: '🤫', label: 'Confidentiality'      },
  governing_law:   { icon: '📜', label: 'Governing Law'        },
}

function ClausesCard({ clauses }) {
  if (!clauses || Object.keys(clauses).length === 0) return null

  return (
    <div className="bg-white rounded-2xl border border-gray-200 p-5">
      <h3 className="text-sm font-semibold text-gray-700 mb-4">
        Identified Clauses
        <span className="ml-2 bg-indigo-100 text-indigo-700 text-xs font-bold px-2 py-0.5 rounded-full">
          {Object.keys(clauses).length}
        </span>
      </h3>
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
        {Object.entries(clauses).map(([key, info]) => {
          const meta = CLAUSE_META[key] || { icon: '📋', label: key }
          const conf = info.confidence ? `${Math.round(info.confidence * 100)}%` : null
          return (
            <div key={key} className="bg-gray-50 rounded-xl p-3 border border-gray-100 hover:border-indigo-200 transition-colors">
              <div className="flex items-center justify-between mb-1">
                <span className="text-xs font-semibold text-gray-700">
                  {meta.icon} {meta.label}
                </span>
                {conf && (
                  <span className="text-xs text-gray-400 bg-white border border-gray-200 px-1.5 py-0.5 rounded-md">
                    {conf}
                  </span>
                )}
              </div>
              {info.text && (
                <p className="text-xs text-gray-500 italic line-clamp-2 mt-0.5">
                  &ldquo;{info.text}&rdquo;
                </p>
              )}
            </div>
          )
        })}
      </div>
    </div>
  )
}

// ── Applicable Legal Sections ─────────────────────────────────────────────────
const ACT_COLORS = {
  IPC:           'bg-red-100 text-red-700',
  CPC:           'bg-blue-100 text-blue-700',
  Contract_Act:  'bg-orange-100 text-orange-700',
  Evidence_Act:  'bg-green-100 text-green-700',
  Constitution:  'bg-purple-100 text-purple-700',
}

function SectionsCard({ sections }) {
  if (!sections || sections.length === 0) return null
  return (
    <div className="bg-white rounded-2xl border border-gray-200 p-5">
      <h3 className="text-sm font-semibold text-gray-700 mb-4">
        Applicable Legal Sections
        <span className="ml-2 bg-gray-100 text-gray-600 text-xs font-bold px-2 py-0.5 rounded-full">
          {sections.length}
        </span>
      </h3>
      <div className="overflow-x-auto">
        <table className="w-full text-xs">
          <thead>
            <tr className="border-b border-gray-100">
              <th className="text-left font-semibold text-gray-400 uppercase tracking-wide pb-2 pr-3 w-28">Act</th>
              <th className="text-left font-semibold text-gray-400 uppercase tracking-wide pb-2 pr-3 w-16">§</th>
              <th className="text-left font-semibold text-gray-400 uppercase tracking-wide pb-2 pr-3">Title</th>
              <th className="text-left font-semibold text-gray-400 uppercase tracking-wide pb-2">Description</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-50">
            {sections.map((s, i) => {
              const actColor = ACT_COLORS[s.act] || 'bg-gray-100 text-gray-600'
              return (
                <tr key={i} className="hover:bg-gray-50 transition-colors">
                  <td className="py-2 pr-3">
                    <span className={`font-bold px-1.5 py-0.5 rounded text-xs ${actColor}`}>{s.act}</span>
                  </td>
                  <td className="py-2 pr-3 font-mono font-semibold text-gray-700">{s.section}</td>
                  <td className="py-2 pr-3 font-medium text-gray-800">{s.title}</td>
                  <td className="py-2 text-gray-500 line-clamp-2">{s.description}</td>
                </tr>
              )
            })}
          </tbody>
        </table>
      </div>
    </div>
  )
}

// ── Main ResultsPanel ─────────────────────────────────────────────────────────
function SimilarCasesCard({ cases }) {
  if (!cases || cases.length === 0) return null
  const CASE_META_SMALL = {
    criminal: 'bg-red-100 text-red-700', civil: 'bg-blue-100 text-blue-700',
    contract_dispute: 'bg-orange-100 text-orange-700', family_law: 'bg-pink-100 text-pink-700',
    property: 'bg-green-100 text-green-700', constitutional: 'bg-purple-100 text-purple-700',
    intellectual_property: 'bg-teal-100 text-teal-700', labour: 'bg-yellow-100 text-yellow-700',
  }
  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-5">
      <div className="flex items-center gap-2 mb-3">
        <span className="text-lg">🔍</span>
        <h3 className="text-base font-semibold text-gray-800">Similar Cases</h3>
        <span className="ml-auto text-xs text-gray-400">RAG — ChromaDB vector search</span>
      </div>
      <div className="space-y-3">
        {cases.map((c, i) => (
          <div key={i} className="border border-gray-100 rounded-lg p-3 hover:bg-gray-50">
            <div className="flex items-start justify-between gap-2 mb-1">
              <p className="text-sm font-medium text-gray-800 leading-tight">{c.title || 'Unknown Case'}</p>
              {c.similarity_score && (
                <span className="text-xs text-gray-400 shrink-0">{Math.round(c.similarity_score * 100)}% match</span>
              )}
            </div>
            <div className="flex flex-wrap items-center gap-1.5 mb-1.5">
              <span className="text-xs text-gray-500">{c.court} · {c.year}</span>
              {c.case_type && (
                <span className={`text-xs px-1.5 py-0.5 rounded-full font-medium ${CASE_META_SMALL[c.case_type] || 'bg-gray-100 text-gray-600'}`}>
                  {c.case_type.replace('_', ' ')}
                </span>
              )}
            </div>
            {c.outcome && <p className="text-xs text-emerald-700 font-medium">⚖️ {c.outcome}</p>}
            {c.sections && <p className="text-xs text-indigo-600 mt-0.5">§ {c.sections}</p>}
          </div>
        ))}
      </div>
    </div>
  )
}

function SummaryCard({ summary }) {
  if (!summary) return null
  return (
    <div className="bg-indigo-50 border border-indigo-200 rounded-xl p-5">
      <div className="flex items-center gap-2 mb-3">
        <span className="text-lg">📋</span>
        <h3 className="text-base font-semibold text-indigo-900">Document Summary</h3>
      </div>
      <p className="text-sm text-indigo-800 leading-relaxed">{summary}</p>
    </div>
  )
}

export default function ResultsPanel({ result }) {
  if (!result) return null

  // Colab returns "classification"; local fallback returns "case_type"
  const cls       = result.classification || result.case_type
  const allScores = cls?.all_scores

  const isLocalFallback = result.status === 'local_fallback'
  const endpoint        = result.endpoint_used

  return (
    <div className="space-y-4">
      {/* Status bar */}
      <div className="flex items-center justify-between text-xs text-gray-400">
        <span>
          {isLocalFallback
            ? <span className="text-yellow-600 font-medium">⚠️ Local fallback mode — Colab not connected</span>
            : <span className="text-emerald-600 font-medium">✅ Analysis complete</span>}
        </span>
        {endpoint && (
          <span>
            via <code className="bg-gray-100 px-1.5 py-0.5 rounded text-gray-600">{endpoint}</code>
          </span>
        )}
      </div>

      {isLocalFallback && result.warning && (
        <div className="bg-yellow-50 border border-yellow-200 text-yellow-800 rounded-xl p-3 text-sm">
          {result.warning}
        </div>
      )}

      {/* Summary — full width, always at top */}
      <SummaryCard summary={result.summary} />

      {/* Two-column layout */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">

        {/* Left column: case type + probability bars */}
        <div className="space-y-4">
          <CaseTypeCard cls={cls} />
          <ScoresChart allScores={allScores} />
        </div>

        {/* Right two columns: entities + clauses + sections */}
        <div className="lg:col-span-2 space-y-4">
          <EntitiesCard    entities={result.entities} />
          <ClausesCard     clauses={result.clauses} />
          <SimilarCasesCard cases={result.similar_cases} />
          <SectionsCard    sections={result.applicable_sections} />
        </div>
      </div>
    </div>
  )
}
