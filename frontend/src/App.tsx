import { BrowserRouter, Routes, Route } from 'react-router-dom'
import StartPage from './pages/StartPage'
import InterviewSetupPage from './pages/InterviewSetupPage'
import InterviewPage from './pages/InterviewPage'
import ResultPage from './pages/ResultPage'

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<StartPage />} />
        <Route path="/interview/new" element={<InterviewSetupPage />} />
        <Route path="/interview/:sessionId" element={<InterviewPage />} />
        <Route path="/interview/:sessionId/result" element={<ResultPage />} />
      </Routes>
    </BrowserRouter>
  )
}
