import { BrowserRouter, Routes, Route } from 'react-router-dom';
import LandingPage from './pages/LandingPage';
import UploadingPage from './pages/UploadingPage';
import ResultsPage from './pages/ResultsPage';


function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path='/' element={<LandingPage />} />
        <Route path='/upload' element={<UploadingPage />} />
        <Route path='/results' element={<ResultsPage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;