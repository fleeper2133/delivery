import { ThemeProvider } from '@mui/material/styles';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import darkTheme from './theme';
import LoginPage from './pages/LoginPage';
import ReportPage from './pages/ReportPage';
import { GlobalStyles } from '@mui/material';

function App() {
  return (
    <ThemeProvider theme={darkTheme}>
      <GlobalStyles styles={{
        body: {
          backgroundColor: '#121212',
          color: '#ffffff',
          margin: 0,
          padding: 0,
        }
      }} />
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
