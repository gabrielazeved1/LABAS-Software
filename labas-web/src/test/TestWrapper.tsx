/**
 * Wrapper de teste padrão do LABAS.
 * Envolve o componente com BrowserRouter + ThemeProvider + AuthContext mockado.
 */
import type { ReactNode } from "react";
import { MemoryRouter } from "react-router-dom";
import { ThemeProvider } from "@mui/material/styles";
import { CssBaseline } from "@mui/material";
import { AuthContext, type AuthContextValue } from "../contexts/AuthContext";
import { SnackbarProvider } from "../contexts/SnackbarContext";
import { theme } from "../theme";

const defaultAuthValue: AuthContextValue = {
  user: null,
  isAuthenticated: false,
  isStaff: false,
  loading: false,
  login: async () => {},
  logout: () => {},
};

interface Props {
  children: ReactNode;
  authValue?: Partial<AuthContextValue>;
  initialPath?: string;
}

export function TestWrapper({
  children,
  authValue = {},
  initialPath = "/",
}: Props) {
  const value: AuthContextValue = { ...defaultAuthValue, ...authValue };

  return (
    <MemoryRouter initialEntries={[initialPath]}>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <SnackbarProvider>
          <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
        </SnackbarProvider>
      </ThemeProvider>
    </MemoryRouter>
  );
}
