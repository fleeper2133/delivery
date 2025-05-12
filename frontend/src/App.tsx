import { ThemeProvider } from '@mui/material/styles';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import { themeWithDataGrid } from './theme';
import LoginPage from './pages/LoginPage';
import ReportPage from './pages/ReportPage';

function App() {
  return (
    <ThemeProvider theme={themeWithDataGrid}>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<LoginPage />} />
          <Route path="/report" element={<ReportPage />} />
        </Routes>
      </BrowserRouter>
    </ThemeProvider>
  );
}

export default App;