import { useNavigate } from 'react-router-dom'

const features = [
  {
    icon: '🎯',
    title: 'Personalized Questions',
    description:
      'Career IQ reads your resume and the job description to generate questions that are actually relevant to you — not generic ones you can find anywhere.',
  },
  {
    icon: '📊',
    title: 'Instant, Scored Feedback',
    description:
      'Every answer gets a score and detailed feedback. You\'ll know exactly what you got right, where you fell short, and how to improve.',
  },
  {
    icon: '🔁',
    title: 'Adaptive Follow-ups',
    description:
      'If your answer needs more depth, Career IQ follows up — just like a real interviewer would. It keeps the conversation going until you\'ve shown what you know.',
  },
  {
    icon: '🧠',
    title: 'Weakness Memory',
    description:
      'Patterns in your answers are tracked across sessions. Over time, Career IQ builds a picture of where you consistently struggle — so you can fix it.',
  },
]

export default function StartPage() {
  const navigate = useNavigate()

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col">

      {/* Nav */}
      <nav className="px-12 py-6 flex items-center border-b border-slate-200 bg-white">
        <span className="text-xl font-semibold tracking-tight text-slate-900">Career IQ</span>
      </nav>

      {/* Hero */}
      <section className="flex flex-col items-center justify-center px-6 pt-28 pb-24 text-center">
        <span className="animate-fade-up inline-block mb-5 px-4 py-1.5 text-sm font-medium text-violet-700 bg-violet-50 rounded-full border border-violet-200">
          AI-Powered SWE Interview Coach
        </span>

        <h1 className="animate-fade-up delay-100 text-5xl font-bold tracking-tight text-slate-900 max-w-2xl leading-tight">
          Practice interviews that actually prepare you
        </h1>

        <p className="animate-fade-up delay-200 mt-6 text-lg text-slate-500 max-w-lg leading-relaxed">
          Paste your resume and a job description. Career IQ takes it from there — questions, feedback, and long-term coaching built around you.
        </p>

        <button
          onClick={() => navigate('/interview/new')}
          className="animate-fade-up delay-300 mt-12 px-10 py-4 bg-violet-600 hover:bg-violet-700 text-white text-base font-semibold rounded-xl shadow-sm transition-colors duration-150 cursor-pointer"
        >
          Start Interview →
        </button>
      </section>

      {/* Divider */}
      <div className="w-full border-t border-slate-200" />

      {/* Features */}
      <section className="flex flex-col items-center px-6 py-24 gap-20">
        {features.map((f, i) => (
          <div
            key={f.title}
            className={`animate-fade-up delay-${(i + 1) * 100} flex flex-col items-center text-center max-w-xl`}
          >
            <span className="text-4xl mb-5">{f.icon}</span>
            <h3 className="text-xl font-semibold text-slate-900 mb-3">{f.title}</h3>
            <p className="text-base text-slate-500 leading-relaxed">{f.description}</p>
          </div>
        ))}
      </section>

      {/* CTA */}
      <section className="flex flex-col items-center px-6 py-24 border-t border-slate-200 text-center">
        <h2 className="animate-fade-up text-3xl font-bold text-slate-900 mb-4">Ready to get started?</h2>
        <p className="animate-fade-up delay-100 text-slate-500 mb-10 max-w-sm leading-relaxed">
          One session is all it takes to see where you stand.
        </p>
        <button
          onClick={() => navigate('/interview/new')}
          className="animate-fade-up delay-200 px-10 py-4 bg-violet-600 hover:bg-violet-700 text-white text-base font-semibold rounded-xl shadow-sm transition-colors duration-150 cursor-pointer"
        >
          Start Interview →
        </button>
      </section>

      {/* Footer */}
      <footer className="py-8 text-center text-sm text-slate-400 border-t border-slate-200">
        Career IQ © {new Date().getFullYear()}
      </footer>

    </div>
  )
}
