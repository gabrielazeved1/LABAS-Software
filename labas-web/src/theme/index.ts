import { createTheme } from "@mui/material/styles";
/*
 * Tema personalizado para o LABAS, inspirado na identidade visual da instituição.
 */
export const theme = createTheme({
  palette: {
    mode: "light",

    primary: {
      main: "#233b1a", // base institucional
      light: "#476546", // variação suave
      dark: "#1a2c14", // versão mais escura
      contrastText: "#FFFFFF",
    },

    secondary: {
      main: "#476546", // apoio visual (cards, elementos secundários)
      light: "#6d8262",
      dark: "#2f4430",
      contrastText: "#FFFFFF",
    },

    success: {
      main: "#2e7d32",
    },

    warning: {
      main: "#ed6c02",
    },

    error: {
      main: "#d32f2f",
    },

    info: {
      main: "#0288d1",
    },

    background: {
      default: "#F5F5F3", // fundo neutro leve
      paper: "#FFFFFF",
    },

    text: {
      primary: "#1F1F1F",
      secondary: "#6d8262", // muted
    },

    divider: "#a7b698",

    grey: {
      300: "#a7b698",
      500: "#6d8262",
    },
  },

  typography: {
    fontFamily: '"Inter", "Roboto", "Arial", sans-serif',

    h4: { fontWeight: 700 },
    h5: { fontWeight: 600 },
    h6: { fontWeight: 600 },

    body1: {
      color: "#1F1F1F",
    },

    body2: {
      color: "#6d8262",
    },
  },

  shape: {
    borderRadius: 8,
  },

  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          textTransform: "none",
          fontWeight: 600,
          borderRadius: 8,
        },
      },
    },

    MuiTableHead: {
      styleOverrides: {
        root: {
          "& th": {
            backgroundColor: "#233b1a",
            color: "#FFFFFF",
            fontWeight: 700,
          },
        },
      },
    },

    MuiTableCell: {
      styleOverrides: {
        root: {
          borderColor: "#a7b698",
        },
      },
    },

    MuiChip: {
      styleOverrides: {
        root: {
          fontWeight: 600,
        },
      },
    },

    MuiOutlinedInput: {
      styleOverrides: {
        root: {
          "& fieldset": {
            borderColor: "#a7b698",
          },
          "&:hover fieldset": {
            borderColor: "#336006",
          },
          "&.Mui-focused fieldset": {
            borderColor: "#233b1a",
          },
        },
      },
    },

    MuiAlert: {
      styleOverrides: {
        standardSuccess: {
          backgroundColor: "#2e7d32",
          color: "#fff",
        },
        standardWarning: {
          backgroundColor: "#ed6c02",
          color: "#fff",
        },
        standardError: {
          backgroundColor: "#d32f2f",
          color: "#fff",
        },
        standardInfo: {
          backgroundColor: "#0288d1",
          color: "#fff",
        },
      },
    },
  },
});
