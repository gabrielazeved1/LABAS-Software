// src/components/layout/AppShell.tsx
import Box from "@mui/material/Box";
import Toolbar from "@mui/material/Toolbar";
import type { ReactNode } from "react";
import AppHeader from "./AppHeader";
import AppSidebar from "./AppSidebar";

const SIDEBAR_WIDTH = 220;

interface Props {
  children: ReactNode;
}

/**
 * Shell principal da aplicação autenticada.
 *
 * Monta a estrutura: Sidebar fixa | Header fixo | Área de conteúdo rolável.
 * Todas as rotas protegidas devem ser renderizadas como filhas deste componente.
 *
 * Layout:
 * ┌──────────┬──────────────────────────┐
 * │          │  AppHeader               │
 * │ Sidebar  ├──────────────────────────┤
 * │          │  {children}              │
 * └──────────┴──────────────────────────┘
 */
export default function AppShell({ children }: Props) {
  return (
    <Box sx={{ display: "flex" }}>
      <AppHeader sidebarWidth={SIDEBAR_WIDTH} />
      <AppSidebar width={SIDEBAR_WIDTH} />

      {/* Área de conteúdo principal */}
      <Box
        component="main"
        sx={{
          flexGrow: 1,
          p: 3,
          bgcolor: "background.default",
          minHeight: "100vh",
        }}
      >
        {/* Espaço reservado para o AppHeader fixo não sobrepor o conteúdo */}
        <Toolbar />
        {children}
      </Box>
    </Box>
  );
}
