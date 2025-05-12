import { createTheme, Theme } from '@mui/material/styles';
import { gridClasses } from '@mui/x-data-grid';

const darkTheme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#90caf9',
    },
    secondary: {
      main: '#f48fb1',
    },
    background: {
      default: '#121212',
      paper: '#1e1e1e',
    },
  },
});

// Расширяем тему для DataGrid
export const themeWithDataGrid = createTheme(darkTheme, {
  components: {
    MuiDataGrid: {
      styleOverrides: {
        root: {
          backgroundColor: darkTheme.palette.background.paper,
          borderColor: darkTheme.palette.divider,
          [`& .${gridClasses.row}`]: {
            '&.Mui-selected': {
              backgroundColor: 'rgba(144, 202, 249, 0.16)',
              '&:hover': {
                backgroundColor: 'rgba(144, 202, 249, 0.24)',
              },
            },
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