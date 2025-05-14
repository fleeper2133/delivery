import { createTheme, Theme } from '@mui/material/styles';
import { gridClasses } from '@mui/x-data-grid';

const darkTheme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#90caf9',
      contrastText: '#000',
    },
    secondary: {
      main: '#f48fb1',
      contrastText: '#000',
    },
    background: {
      default: '#121212',
      paper: '#1e1e1e',
    },
    text: {
      primary: '#ffffff',
      secondary: 'rgba(255, 255, 255, 0.7)',
      disabled: 'rgba(255, 255, 255, 0.5)',
    },
    divider: 'rgba(255, 255, 255, 0.12)',
    action: {
      active: '#ffffff',
      hover: 'rgba(255, 255, 255, 0.08)',
      selected: 'rgba(255, 255, 255, 0.16)',
      disabled: 'rgba(255, 255, 255, 0.3)',
      disabledBackground: 'rgba(255, 255, 255, 0.12)',
    },
  },
  components: {
    MuiAppBar: {
      styleOverrides: {
        root: {
          backgroundColor: '#1e1e1e',
        },
      },
    },
    MuiDrawer: {
      styleOverrides: {
        paper: {
          backgroundColor: '#1e1e1e',
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          backgroundColor: '#1e1e1e',
        },
      },
    },
    MuiPaper: {
      styleOverrides: {
        root: {
          backgroundColor: '#1e1e1e',
        },
      },
    },
    MuiDataGrid: {
      styleOverrides: {
        root: {
          borderColor: 'rgba(255, 255, 255, 0.12)',
          [`& .${gridClasses.row}`]: {
            '&.Mui-selected': {
              backgroundColor: 'rgba(144, 202, 249, 0.16)',
              '&:hover': {
                backgroundColor: 'rgba(144, 202, 249, 0.24)',
              },
            },
            '&:hover': {
              backgroundColor: 'rgba(255, 255, 255, 0.08)',
            },
          },
          [`& .${gridClasses.columnHeaders}`]: {
            backgroundColor: '#1e1e1e',
          },
          [`& .${gridClasses.footerContainer}`]: {
            backgroundColor: '#1e1e1e',
          },
        },
      },
    },
  },
});

// Расширение типов для TypeScript
declare module '@mui/material/styles' {
  interface Components {
    MuiDataGrid?: {
      styleOverrides?: {
        root?: React.CSSProperties & {
          [key: string]: any;
        };
      };
    };
  }
}

export default darkTheme;